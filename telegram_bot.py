import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

logging.basicConfig(
    filename="telegram_bot.log",
    format="%(asctime)s %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
    level=logging.WARNING
)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Я — бот поддержки издательства \"Игра Глаголов\"\nЧем я могу помочь?"
    )


def flow_dialogue(update: Update, context: CallbackContext):
    text = update.message.text
    project_id = context.bot_data["project_id"]
    reply_text = detect_intent_text(text, project_id, update.effective_chat.id)
    update.message.reply_text(reply_text)


def detect_intent_text(text, project_id, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="RU")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text


def main():
    env = Env()
    env.read_env()

    telegram_token = env.str("TELEGRAM_BOT_TOKEN")
    project_id = env.str("PROJECT_ID")

    updater = Updater(telegram_token)
    dp = updater.dispatcher

    dp.bot_data["project_id"] = project_id
    dp.update_persistence()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, flow_dialogue))

    updater.start_polling()


if __name__ == '__main__':
    main()
