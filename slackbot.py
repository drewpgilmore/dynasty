import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from scores import Dynasty

env_path = Path('.') / '.bot_env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
league = Dynasty(year=2022)
week = 17
scores = league.weekScores(week)

def scoreUpdate(c, memo):
    finalists = ['Drew', 'Cal', 'Marcus', 'Cody']
    client.chat_postMessage(channel=c, text=f'{memo}:')
    
    
    # scores update
    # for team, score in scores.items(): 
    #     if team in finalists: 
    #         msg = f'{team}: {score}'
    #         client.chat_postMessage(channel=c, text=msg)

    for team in finalists: 
        score = scores[team]
        lineup = league.weekLineup(team, week)
        msg = f'{team}: {score}'
        client.chat_postMessage(channel=c, text=msg)
        for player in lineup: 
            playerName = player[0]
            playerPos = player[1]['Pos']
            playerScore = player[1]['Points']
            msg = f"  {playerPos} {playerName} : {playerScore}\n"
            client.chat_postMessage(channel=c, text=msg)


def championshipUpdate():
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

    client.chat_postMessage(channel='#ed', **header)
    for team, score in revisedScores.items(): 
        if team in finalists: 
            buff = 10 - len(team)
            #m = f'{team}{"." * buff}{score:.2f}' # with whitespace buffer
            rank = list(revisedScores.keys()).index(team)
            text = f'{emojis[rank]} *{team}: {score:.2f}*'
            message = {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]}
            client.chat_postMessage(channel='#ed', **message)

    return None

championshipUpdate()


#scoreUpdate('#bot-test', 'Championship Lineups')

#print(scores)

#msg = f'2015 Week {week} Scores: {str(scores)}'
#msg = 'Not Cal, thank you for the request\nOxford Dictionary defines "likely" as: such as well might happen or be true; probable.'
#client.chat_postMessage(channel='#random', text=msg)




# def alertLeague(channel:str='#random', message:str=''): 
#     client.chat_postMessage(channel=channel, message=message)

# alertLeague(channel='#random', message="Please do not disparage me")


# line = 'RB/WR/TE Kennth Walker III'
# line2 = 'QB Pat Mahommes'
# maxl = max([len(line), len(line2)]) + 1



# for l in [line, line2]: 
#     space = maxl - len(l)
#     buffer = ' ' * space
#     m = f'{l}{buffer}10.0'
#     print(m)

# print(len(line))


m = {
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Championship Scores"
            }
        },
                {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Sample message\n*bold text here*\n# more text here"
            }
        }
    ]
    
}
#client.chat_postMessage(channel='#bot-test', **m)