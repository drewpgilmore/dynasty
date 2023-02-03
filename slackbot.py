import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from scores import Dynasty
from slackbot_utils import sendMessage

env_path = Path('.') / '.bot_env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
league = Dynasty(year=2022)


def championshipUpdate(channel):
    league = Dynasty(year=2022)
    finalists = ['Drew', 'Cal', 'Marcus', 'Cody']
    emojis = [':one:', ':two:', ':three:', ':four:']
    missingPlayers = {
        "Josh Allen": 0,
        "Joe Mixon": 0, 
        "Stefon Diggs": 0,
        "Joe Burrow": 0,
        "Ja'Marr Chase": 0,
        "Dawson Knox": 0
    }
    
    # get missing players week 18 scores and add them to week 17
    week17Scores = league.weekScores(17)
    for team in finalists: 
        lineup = league.weekLineup(team, 18)
        for player in lineup: 
            if player[0] in missingPlayers.keys(): 
                playerScore = round(player[1]['Points'],0)
                missingPlayers[player[0]] = playerScore
                week17Scores[team] += playerScore
            else: 
                continue

    revisedScores = dict(sorted(week17Scores.items(), 
                        key=lambda x:x[1], 
                        reverse=True))

    header = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":mardi-gras-parrot: Championship Scores (Projected) :mardi-gras-parrot:"
                }
            },
            {
                "type": "divider"
            }
        ]
    }

    client.chat_postMessage(channel=channel, **header)
    for team, score in revisedScores.items(): 
        if team in finalists: 
            rank = list(revisedScores.keys()).index(team)
            text = f'{emojis[rank]} *{team}: {score:.2f}*'
            message = {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]}
            client.chat_postMessage(channel=channel, **message)

    return missingPlayers

championshipUpdate("#bot-test")