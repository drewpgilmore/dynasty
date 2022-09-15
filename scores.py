#! /usr/bin/env python3
# scores.py - fetches league data for given week

from tkinter import scrolledtext
import pandas as pd
import numpy as np
import time

from espn_api.football import League
from config import LEAGUE_ID, ESPN_S2, SWID

def getLeague(year):
    """Creates league object for given year"""
    league = League(
        league_id=LEAGUE_ID,
        year=year,
        espn_s2=ESPN_S2,
        swid=SWID
    )

    return league

def getScores(year, week):
    """Returns dict of teams and scores from box scores"""
    league = getLeague(year)
    if year >= 2021:
        scoreboard = league.box_scores(week=week)
    else:
        scoreboard = league.scoreboard(week=week)
        
    scores = {}
    for matchup in scoreboard:
        scores[matchup.home_team.team_name] = matchup.home_score
        if matchup.away_team != 0:
            scores[matchup.away_team.team_name] = matchup.away_score

    scoresSorted = dict(sorted(scores.items(),key=lambda x:x[1],reverse=True))

    return scoresSorted

def displayScores(year, week):
    scores = getScores(year, week)
    df = pd.DataFrame(
        data=scores.values(), 
        index=scores.keys(), 
        columns=['Score']
    )
    sorted_data = df.sort_values(by='Score', ascending=False)
    sorted_html = sorted_data.to_html(
        justify='left',
        table_id='scoreboard'
    )

    return sorted_data
    #return sorted_data.to_html()