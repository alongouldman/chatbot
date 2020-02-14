# TODO: rename to bot and remove the other one
import logging
from typing import Tuple, List
from uuid import uuid4

from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, InlineQueryResultArticle,
                      InputTextMessageContent)
from telegram.ext import (Updater, MessageHandler, Filters,
                          ConversationHandler, CallbackContext, run_async, InlineQueryHandler, CommandHandler,
                          CallbackQueryHandler)
from telegram.utils.helpers import escape_markdown
from telegram.utils.promise import Promise

from bot_utils import get_bot_token, extract_number, get_message_date
from consts import ASK_USER_FOR_CATEGORY, ASK_USER_FOR_DESCRIPTION, NO_DESCRIPTION, FORGET_CATEGORY, \
	FORGET_CATEGORY_MESSAGE, CHOOSE_CATEGORY, LOAD_MORE_CATEGORIES, LOADING_CATEGORIES, PLEASE_CHOOSE_CATEGORY, \
	CATEGORY_NOT_FOUND_PLEASE_CHOOSE_ANOTHER, CATEGORY_MISSING, EXPENSE_SAVED_SUCCESSFULLY
from models import Category, ensure_db_connection, CategoryType, Expense, TelegramGroup
from spreadsheet import add_to_sheet


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# for the conversation handler
DESCRIPTION = 1


@run_async
@ensure_db_connection
def get_or_create_group(chat_id: int, user_id: int) -> Promise:
	chat_id = str(chat_id)
	user_id = str(user_id)
	group = TelegramGroup.objects(telegram_chat_id=chat_id).first()
	if not group:
		group = TelegramGroup(telegram_chat_id=chat_id)
	# add user to group ids, blocking
	add_user_to_group(group, user_id)
	group.save()
	return group


def add_user_to_group(group, user_id):
	if user_id not in group.user_ids:
		group.user_ids.append(user_id)
		logging.info(f"user {user_id} is added to group {group.telegram_chat_id}")


def error(update, context):
	"""Log Errors caused by Updates."""
	logger.error('Update "%s" caused error "%s"', update, context.error)
	try:
		bot: Bot = update.callback_query.bot
		chat_id = update.callback_query.message.chat_id
	except AttributeError:
		try:
			bot: Bot = update.message.bot
			chat_id = update.message.chat_id
		except AttributeError:
			logger.error('Update "%s" is from inline query, no chat to send error to', update)
			return
	bot.send_message(chat_id, f"en error occurred: {context.error}, stopping conversation")


def query_has_only_amount(query):
	return len(query.strip().split(' ')) == 1


@run_async
@ensure_db_connection
def get_all_categories() -> Promise:
	logger.info("getting categories from db")
	categories = Category.objects()
	if not categories:
		Category.init_categories()
		categories = Category.objects()

	# remove unknown category - this will be used for bank scraper
	categories = [c for c in categories if c.type != CategoryType.UNKNOWN]
	return categories


def get_matching_categories(category_from_user, categories_promise) -> List[str]:
	all_categories = categories_promise.result()
	matching_categories = []
	for cat in all_categories:
		if category_from_user in cat.name:
			matching_categories.append(cat.name)
	if not matching_categories:
		matching_categories = [CATEGORY_NOT_FOUND_PLEASE_CHOOSE_ANOTHER]

	return matching_categories


def get_query_results(amount: float, matching_categories: list):
	results = []

	for category in matching_categories:
		# input message content
		message = f"{amount}, {category}"
		input_message_content = InputTextMessageContent(message)

		# description
		article = InlineQueryResultArticle(
			id=uuid4(),
			title=str(amount),
			description=category,
			input_message_content=input_message_content)
		results.append(article)
	return results


def handle_inline_query(update, context):
	"""Handle the inline query."""
	# get categories already from db
	if 'categories_promise' not in context.user_data:
		context.user_data['categories_promise'] = get_all_categories()

	query = update.inline_query.query
	if not query:
		return

	# the query can be:
	#   1. only amount
	#   2. amount and category
	amount = extract_number(query)
	if not query_has_only_amount(query):
		_, category = query.split(' ', 1)
		matching_categories = get_matching_categories(category.strip(), context.user_data['categories_promise'])

	else:
		matching_categories = get_matching_categories("", context.user_data['categories_promise'])  # this will get all categories

	results = get_query_results(amount, matching_categories)
	update.inline_query.answer(results, cache_time=0)


def get_amount_and_category_ask_about_description(update, context):
	
	if 'group_promise' not in context.user_data:
		context.user_data['group_promise'] = get_or_create_group(update.effective_chat.id, update.effective_user.id)

	# get categories already from db, in case for some reason we dont have them already
	if 'categories_promise' not in context.user_data:
		context.user_data['categories_promise'] = get_all_categories()
		
	message = update.message.text
	logging.info(f"got message: {message}")
	try:
		amount, category_name = [item.strip() for item in message.split(',')]
	except ValueError:  # too many values to unpack
		update.message.reply_text(CATEGORY_MISSING)
		return
	expense = Expense()
	amount = extract_number(amount)
	expense.amount = amount
	expense.date = get_message_date(update.message)

	all_categories = context.user_data['categories_promise'].result()
	category = next((cat for cat in all_categories if cat.name == category_name), None)
	if not category:
		update.message.reply_text(CATEGORY_NOT_FOUND_PLEASE_CHOOSE_ANOTHER)
		return

	expense.amount = understand_if_expense_is_credit_or_debit(category, expense)

	expense.category = category
	group = context.user_data['group_promise'].result()
	expense.telegram_group = group

	context.user_data['expense'] = expense

	button_row = [InlineKeyboardButton(NO_DESCRIPTION, callback_data=NO_DESCRIPTION)]
	update.message.reply_text(ASK_USER_FOR_DESCRIPTION, reply_markup=InlineKeyboardMarkup([button_row]))

	return DESCRIPTION


def skip_description_and_save_expense(update, context):
	logger.info("skipping description")
	save_expense(context.user_data['expense'])
	update.effective_chat.send_message(EXPENSE_SAVED_SUCCESSFULLY)
	return ConversationHandler.END


def get_description_and_save_expense(update, context):
	description = update.message.text
	logger.info(f"got description: {description}")
	context.user_data['expense'].description = description
	save_expense(context.user_data['expense'])
	update.message.reply_text(EXPENSE_SAVED_SUCCESSFULLY)
	return ConversationHandler.END


def save_expense(expense: Expense) -> None:
	logger.info(f"saving expense: {expense}")
	expense.save()
	# also save to spreadsheet. this is temporary, until I add the UI
	add_to_sheet(expense)


def understand_if_expense_is_credit_or_debit(category, expense):
	# understand if expense is credit or debit
	if category.type == CategoryType.INCOME:
		if expense.amount < 0:
			return expense.amount * -1  # makes it positive
	elif expense.amount > 0:
		return expense.amount * -1  # makes it negative
	return expense.amount


def cancel(update, context):
	logger.info(f"canceling {context.user_data.get('expense', '')}")
	return ConversationHandler.END


def main():
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(get_bot_token(), use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	conv_handler = ConversationHandler(
		entry_points=[
			MessageHandler(Filters.text, get_amount_and_category_ask_about_description)],

		states={
			DESCRIPTION: [MessageHandler(Filters.text, get_description_and_save_expense),
						  CallbackQueryHandler(skip_description_and_save_expense, pattern=f"^{NO_DESCRIPTION}$")]
		},

		fallbacks=[CommandHandler('cancel', cancel)],
		conversation_timeout=1000,
	)

	dp.add_handler(conv_handler)


	# TODO:
	# make category an Enum hard coded, so it will be faster. also migrations can be easier.
	# migrate investment category to have prefix "investment"

	dp.add_handler(InlineQueryHandler(handle_inline_query))

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	logger.info("starting bot")
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
	main()
