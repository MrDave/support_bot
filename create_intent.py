import argparse
import json
import logging

from environs import Env
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
    level=logging.WARNING
)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)

        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="name of JSON file with training phrases")
    args = parser.parse_args()

    project_id = env.str("PROJECT_ID")

    with open(args.filename) as file:
        payload = file.read()
    training_phrases = json.loads(payload)

    for intent, values in training_phrases.items():
        questions, answer = values.values()
        print(questions, answer)
        try:
            create_intent(project_id, intent, questions, (answer,))
        except InvalidArgument as error:
            logging.error(error)
            continue


if __name__ == '__main__':
    main()
