import logging
import os

from environs import Env
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

from dialog_flow_helpers import detect_intent_text
from telegram_helpers import TelegramLogsHandler

logger = logging.getLogger()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я — бот поддержки издательства \"Игра Глаголов\"\nЧем я могу помочь?"
    )


def process_dialogue(update: Update, context: CallbackContext):
    text = update.message.text
    project_id = context.bot_data["project_id"]
    reply_text = detect_intent_text(text, project_id, update.effective_chat.id).query_result.fulfillment_text
    update.message.reply_text(reply_text)


def main():
    env = Env()
    env.read_env()

    telegram_token = env.str("TELEGRAM_BOT_TOKEN")
    telegram_logging_token = env.str("TELEGRAM_LOGGING_BOT_TOKEN")
    project_id = env.str("PROJECT_ID")
    tg_user_id = env.str("TELEGRAM_USER_ID")
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id

    updater = Updater(telegram_token)
    dp = updater.dispatcher

    log_level = env.log_level("LOGGING_LEVEL", logging.WARNING)
    logger.setLevel(level=log_level)
    logger_bot = Updater(telegram_logging_token).dispatcher.bot
    logger.addHandler(TelegramLogsHandler(logger_bot, tg_user_id))

    dp.bot_data["project_id"] = project_id
    dp.update_persistence()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_dialogue))

    updater.start_polling()


if __name__ == '__main__':
    main()
