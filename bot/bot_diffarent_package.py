# TODO: rename to bot and remove the other one
import logging
from typing import List

from telegram import (ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler, CallbackContext, run_async, CallbackQueryHandler)
from telegram.utils.promise import Promise

from bot_utils import get_bot_token, extract_number
# ================ Bot massages ================
from models import Category, ensure_db_connection, CategoryType, Expense

ASK_USER_FOR_CATEGORY = """
איזה קטגוריה ההוצאה?
שים לב - אם זוהי קטגוריה חד פעמית, לחץ על "אל תזכור את הקטגוריה".
"""

ASK_USER_FOR_DESCRIPTION = """
על מה היתה ההוצאה? (לא קטגוריה, אלא פירוט).
אם אין פירוט מלבד שם הקטגוריה, לחץ על "אין פירוט".
"""

NO_DESCRIPTION = "אין פירוט"

FORGET_CATEGORY = "forget_category"

FORGET_CATEGORY_MESSAGE = "אל תזכור את הקטגוריה"

AMOUNT, CATEGORY, DESCRIPTION = range(3)

# ==============================================


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@run_async
@ensure_db_connection
def get_categories() -> Promise:
	categories = Category.objects()
	logger.info("got categories from db")
	return categories


def get_amount_and_ask_about_description(update: Update, context: CallbackContext):
	# get the categories now and save for later, for better speed
	categories: Promise = get_categories()
	context.chat_data['categories_promise'] = categories

	amount = extract_number(update.message.text)
	logger.info(f"amount is {amount}")
	expense = Expense(amount=amount)
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


def ask_about_categories(update: Update, context: CallbackContext, is_callback: bool = False):
	if is_callback:
		bot: Bot = update.callback_query.bot
		chat_id = update.callback_query.message.chat_id
	else:
		bot: Bot = update.message.bot
		chat_id = update.message.chat_id
		
	# message about not remember category
	if context.chat_data.get(FORGET_CATEGORY) is None:
		context.chat_data[FORGET_CATEGORY] = False
	massage = FORGET_CATEGORY_MESSAGE
	if context.chat_data[FORGET_CATEGORY]:
		massage = massage + " ✔"
	button = InlineKeyboardButton(massage, callback_data=FORGET_CATEGORY)
	
	bot.send_message(chat_id, ASK_USER_FOR_CATEGORY, reply_markup=InlineKeyboardMarkup([[button]]))

	categories = context.chat_data['categories_promise'].result()  # get the calculated results of the promise
	categories = [c for c in categories]
	categories.sort(key=lambda cat: len(cat.expenses), reverse=True)
	reply_keyboard = []
	row = []
	for category in categories[:10]:
		row.append(InlineKeyboardButton(category.name, callback_data=str(category.id)))
		if len(row) == 2:
			reply_keyboard.append(row)
			row = []

	if row:
		reply_keyboard.append(row)

	reply_markup = InlineKeyboardMarkup(reply_keyboard)
	bot.send_message(chat_id, "בחר קטגוריה ", reply_markup=reply_markup)
	return CATEGORY


def skip_description_and_ask_about_category(update, context):
	logger.info("skipping description")
	return ask_about_categories(update, context, is_callback=True)


def get_category_and_save_expense(update, context):
	callback_data = update.callback_query.data
	if callback_data == FORGET_CATEGORY:
		context.chat_data[FORGET_CATEGORY] = not context.chat_data[FORGET_CATEGORY]
		return ask_about_categories(update, context, is_callback=True)


def error(update, context):
	"""Log Errors caused by Updates."""
	logger.warning('Update "%s" caused error "%s"', update, context.error)


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

			CATEGORY: [CallbackQueryHandler(get_category_and_save_expense, pattern=f"^{FORGET_CATEGORY}$")]
		},

		fallbacks=[CommandHandler('cancel', cancel)]
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
