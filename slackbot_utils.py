import slack 
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.bot_env'
load_dotenv(dotenv_path=env_path)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


def sendMessage(channel='#bot-test', text='') -> None: 
    """Sends markdown formatted message to given channel"""
    message = {
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': text
                }
            }
        ]
    }
    client.chat_postMessage(channel=channel, **message)
    return None
