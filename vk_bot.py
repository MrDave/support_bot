import logging
import random

import vk_api as vk
from environs import Env
from google.cloud import dialogflow
from telegram.ext import Updater
from vk_api.longpoll import VkLongPoll, VkEventType

from telegram_bot import TelegramLogsHandler

logger = logging.getLogger()


def detect_intent_text(text, project_id, session_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="RU")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback


def flow_dialogue(event, vk_api, project_id):
    user_id = event.user_id
    text = event.text
    reply_text, is_fallback = detect_intent_text(text, project_id, user_id)
    if not is_fallback:
        vk_api.messages.send(
            user_id=user_id,
            message=reply_text,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()

    vk_token = env.str("VK_GROUP_TOKEN")
    project_id = env.str("PROJECT_ID")
    telegram_logging_token = env.str("TELEGRAM_LOGGING_BOT_TOKEN")
    tg_user_id = env.str("TELEGRAM_USER_ID")

    log_level = env.log_level("LOGGING_LEVEL", logging.WARNING)
    logger.setLevel(level=log_level)
    logger_bot = Updater(telegram_logging_token).dispatcher.bot
    logger.addHandler(TelegramLogsHandler(logger_bot, tg_user_id))

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    flow_dialogue(event, vk_api, project_id)
        except Exception as e:
            logger.exception(f"Бот поддержки VK упал с ошибкой:\n")
            continue


if __name__ == '__main__':
    main()
