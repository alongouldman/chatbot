# TODO: rename to bot and remove the other one
import logging
from collections import defaultdict
from typing import List, Tuple

from bson.son import SON
from telegram import (ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler, CallbackContext, run_async, CallbackQueryHandler)
from telegram.utils.promise import Promise

from bot_utils import get_bot_token, extract_number, get_message_date
# ================ Bot massages ================
from models import Category, ensure_db_connection, CategoryType, Expense, TelegramGroup
from spreadsheet import add_to_sheet

ASK_USER_FOR_CATEGORY = """
איזה קטגוריה ההוצאה?
שים לב - אם זוהי קטגוריה חד פעמית, לחץ על "אל תזכור את הקטגוריה".
"""

ASK_USER_FOR_DESCRIPTION = """
על מה היתה ההוצאה? (לא קטגוריה, אלא פירוט).
אם אין פירוט מלבד שם הקטגוריה, לחץ על "אין פירוט".
"""

NO_DESCRIPTION = "אין פירוט"

FORGET_CATEGORY = "change_forget_category_button"

FORGET_CATEGORY_MESSAGE = "אל תזכור את הקטגוריה"

CHOOSE_CATEGORY = "בחר קטגוריה"

LOAD_MORE_CATEGORIES = "עוד קטגוריות..."

LOADING_CATEGORIES = "טוען קטגוריות..........."

AMOUNT, CATEGORY, DESCRIPTION = range(3)

# ==============================================


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@run_async
@ensure_db_connection
def get_categories(telegram_group: Promise) -> Promise:
	logger.info("getting categories from db")
	categories = Category.objects()  # TODO: filter unknown category
	if not categories:
		Category.init_categories()
		categories = Category.objects() # TODO: filter unknown category

	categories = [c for c in categories if c.type != CategoryType.UNKNOWN]  # remove unknown category - this will be used for bank scraper
	# TODO: filter only relevant expenses!
	pipeline = [
		{"$match": {'telegram_group': telegram_group.result().telegram_chat_id}},
		{"$group": {"_id": "$category", "count": {"$sum": 1}}}
	]
	categories_count = list(Expense.objects().aggregate(pipeline))
	categories_count = {count['_id']: count['count'] for count in categories_count}
	categories.sort(key=lambda c: categories_count.get(c.name, 0), reverse=True)
	return categories


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


def get_amount_and_ask_about_description(update: Update, context: CallbackContext):
	# get the categories now and save for later, for better speed
	group: Promise = get_or_create_group(update.message.chat_id, update.message.from_user.id)
	categories: Promise = get_categories(group)
	context.chat_data['categories_promise'] = categories
	context.chat_data['telegram_group_promise'] = group

	amount = extract_number(update.message.text)
	logger.info(f"amount is {amount}")
	expense = Expense(amount=amount)
	expense.date = get_message_date(update.message) 
	context.chat_data['expense'] = expense

	button_row = [InlineKeyboardButton(NO_DESCRIPTION, callback_data=NO_DESCRIPTION)]
	update.message.reply_text(ASK_USER_FOR_DESCRIPTION, reply_markup=InlineKeyboardMarkup([button_row]))

	return DESCRIPTION


def get_description_and_ask_about_category(update, context):
	# this could be the second time we get to here, so skip if it is
	if not context.chat_data['expense'].description:
		description = update.message.text
		logger.info(f"got description: {description}")
		context.chat_data['expense'].description = description

	return ask_about_categories(update, context)


def get_categories_markup(categories: list, add_load_more_categories_button=False) -> Tuple[InlineKeyboardMarkup, list]:
	reply_keyboard = []
	row = []
	for category in categories:
		row.append(InlineKeyboardButton(category.name, callback_data=category.name))
		if len(row) == 2:
			reply_keyboard.append(row)
			row = []

	if row:
		reply_keyboard.append(row)

	if add_load_more_categories_button:
		reply_keyboard.append([InlineKeyboardButton(LOAD_MORE_CATEGORIES, callback_data=LOAD_MORE_CATEGORIES)])
	reply_markup = InlineKeyboardMarkup(reply_keyboard)
	return reply_markup


def ask_about_categories(update: Update, context: CallbackContext, is_callback: bool = False):
	if is_callback:
		bot: Bot = update.callback_query.bot
		chat_id = update.callback_query.message.chat_id
	else:
		bot: Bot = update.message.bot
		chat_id = update.message.chat_id
		
	# message about not remember category
	massage = FORGET_CATEGORY_MESSAGE
	button = InlineKeyboardButton(massage, callback_data=FORGET_CATEGORY)
	bot.send_message(chat_id, ASK_USER_FOR_CATEGORY, reply_markup=InlineKeyboardMarkup([[button]]))

	message = bot.send_message(chat_id, LOADING_CATEGORIES)
	categories = context.chat_data['categories_promise'].result()  # get the calculated results of the promise
	context.chat_data['all_categories'] = categories
	reply_markup = get_categories_markup(categories[:10], add_load_more_categories_button=True)
	context.chat_data['displayed_categories'] = categories[:10]
	message.edit_text(CHOOSE_CATEGORY, reply_markup=reply_markup)
	return CATEGORY


def skip_description_and_ask_about_category(update, context):
	logger.info("skipping description")
	return ask_about_categories(update, context, is_callback=True)


def change_forget_category_button(update, context):
	# message about not remember category
	massage = FORGET_CATEGORY_MESSAGE
	if context.chat_data[FORGET_CATEGORY]:
		massage = massage + " ✔"
	button = InlineKeyboardButton(massage, callback_data=FORGET_CATEGORY)
	update.callback_query.message.edit_text(ASK_USER_FOR_CATEGORY, reply_markup=InlineKeyboardMarkup([[button]]))


def handle_forget_category(update, context):
	if context.chat_data.get(FORGET_CATEGORY) is None:
		context.chat_data[FORGET_CATEGORY] = True
	else:
		context.chat_data[FORGET_CATEGORY] = not context.chat_data[FORGET_CATEGORY]
	logging.info(f"remembering category: {context.chat_data[FORGET_CATEGORY]}")
	change_forget_category_button(update, context)
	context.chat_data['expense'].remember_category = not context.chat_data[FORGET_CATEGORY]  # "not" because the field is saves as "remember" and not "forget"
	return CATEGORY


def handle_load_more_categories(update, context):
	logging.info("loading more categories")
	displayed_categories = context.chat_data['displayed_categories']
	all_categories = context.chat_data['all_categories']
	not_displayed_categories = [c for c in all_categories if c not in displayed_categories]
	load_more = True if len(not_displayed_categories) > 10 else False
	# load another 10
	categories_to_display = displayed_categories + not_displayed_categories[:10]
	reply_markup = get_categories_markup(categories_to_display, add_load_more_categories_button=load_more)
	context.chat_data['displayed_categories'] = categories_to_display
	update.callback_query.message.edit_text(CHOOSE_CATEGORY, reply_markup=reply_markup)
	return CATEGORY


def get_category_and_save_expense(update, context):
	category_name = update.callback_query.data
	logging.info(f"got category: {category_name}")
	expense = context.chat_data['expense']
	categories = context.chat_data['all_categories']
	category = next(cat for cat in categories if cat.name == category_name)

	# understand if expense is credit or debit
	if category.type == CategoryType.INCOME:
		if expense.amount < 0:
			expense.amount = expense.amount * -1  # makes it positive
	elif expense.amount > 0:
		expense.amount = expense.amount * -1  # makes it negative

	expense.category = category

	group = context.chat_data['telegram_group_promise'].result()
	expense.telegram_group = group
	expense.save()

	logger.info(f"saving expense: {expense} to category {category} in group {group}")
	update.callback_query.bot.send_message(update.callback_query.message.chat_id, "ההוצאה הוזנה בהצלחה")

	# also save to spreadsheet. this is temporary, until I add the UI
	add_to_sheet(expense)
	return ConversationHandler.END


def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)
	try:
		bot: Bot = update.callback_query.bot
		chat_id = update.callback_query.message.chat_id
	except AttributeError:
		bot: Bot = update.message.bot
		chat_id = update.message.chat_id
	bot.send_message(chat_id, f"en error occurred: {context.error}, stopping conversation")
	return ConversationHandler.END


def cancel(update, context):
	logger.info(f"canceling {context.chat_data.get('expense', '')}")
	return ConversationHandler.END


def main():
	# Create the Updater and pass it your bot's token.
	# Make sure to set use_context=True to use the new context based callbacks
	# Post version 12 this will no longer be necessary
	updater = Updater(get_bot_token(), use_context=True)

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
	conv_handler = ConversationHandler(
		entry_points=[
			MessageHandler(Filters.regex(r'(\b[-+]?[0-9]+\.?[0-9]*\b)'), get_amount_and_ask_about_description)],

		states={
			DESCRIPTION: [MessageHandler(Filters.text, get_description_and_ask_about_category),
						  CallbackQueryHandler(skip_description_and_ask_about_category, pattern=f"^{NO_DESCRIPTION}$")],

			CATEGORY: [CallbackQueryHandler(handle_forget_category, pattern=f"^{FORGET_CATEGORY}$"),
			           CallbackQueryHandler(handle_load_more_categories, pattern=f"^{LOAD_MORE_CATEGORIES}$"),
			           CallbackQueryHandler(get_category_and_save_expense)]
		},

		fallbacks=[CommandHandler('cancel', cancel)],
		conversation_timeout=1000,
		allow_reentry=True
	)

	dp.add_handler(conv_handler)

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
