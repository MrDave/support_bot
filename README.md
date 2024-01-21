# Game of Verbs support bot
Support bot for Game of Verbs with DialogueFlow at its core

## How to install
Python should already be installed. This project is tested on Python 3.11. You may use other versions as you will, but YMMV.

Clone the repo / download code

Using virtual environment [virtualenv/venv](https://docs.python.org/3/library/venv.html) is recommended for project isolation.

Install requirements:
```commandline
pip install -r requirements.txt
```

Set up environmental variables.  
Create `.env` file in root folder and write down the following variables:
- `TELEGRAM_BOT_TOKEN` - Access token of your bot. You get one from [BotFather Telegram bot](https://t.me/BotFather) when you create a bot.
- `VK_GROUP_TOKEN` - Access token of your VK group. Get it from the group's settings.
- `PROJECT_ID` - Google Cloud project's ID
- `GOOGLE_APPLICATION_CREDENTIALS` - Filepath to `credentials.json` of your Google Cloud project. See below how to get it.
- `DIALOG_FLOW_API_KEY` - DialogueFlow's access token. See below how to get it.


### Setting up Google Project

[Main article here](https://cloud.google.com/dialogflow/es/docs/quick/setup)

To work with DialogueFlow, you'll need a [Google Cloud](https://cloud.google.com/) project and a [DialogueFlow](https://dialogflow.cloud.google.com/) project.
Follow the article above to set everything up, but the main points are:
- Make a Google Cloud project (or select an existing one)
- Make sure DialogFlow's API is enabled
- Make a DialogueFlow project, write your Google Cloud's project ID into appropriate field in DF's settings
- Use Google Cloud CLI to authenticate and create `credentials.json` file
- Create DialogueFlow API key, using [instructions](https://cloud.google.com/docs/authentication/api-keys#python)

#### Creating DialogueFlow API key
To create API key use a helper script `create_api_key.py`
```commandline
python create_api_key.py your_key_name
```

For details and options see the [official instructions](https://cloud.google.com/docs/authentication/api-keys#python)

## Teaching DialogueFlow

For DialogueFlow to be able to respond to users' messages it must be taught intents. While it can be done manually in DF project's dashboard, you can use `create_intent.py` script if you have a JSON file with training phrases
JSON file's structure should like this:
```json
{
    "Name of the intent": {
        "questions": [
            "User expression 1",
            "User expression 2",
            "User expression 3",
            "..."
        ],
        "answer": "Text of the answer"
    }
}
```

In this case run the script `create_intent.py`:
```commandline
python create_intent.py filepath/to/phrases/file.json
```

## How to use

Telegram and VK bots are separate and should be launched by executing `telegram_bot.py` and `vk_bot.py`

```commandline
python telegram_bot.py  # launches Telegram bot
python vk_bot.py  # launches VK bot
```

For Telegram bot to be able to send messages, send it a `/start` command

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
