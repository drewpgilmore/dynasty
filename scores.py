#! /env/bin python3
# scores.py - fetches league data for given week

import pandas as pd
import numpy as np
import time

from espn_api.football import League


def getLeague(year):
    """
    Returns League object defined in espn_api
        Parameters:
            year (int): year for desired season
        Reurns:
            league (class): League object
    """
    
    # init league with inputs from config
    from config import LEAGUE_ID, ESPN_S2, SWID
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
    
    # 2021 onward uses box_scores instead of scoreboard
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

def getProjected(year, week):
    """Returns dict of teams and projected scores"""
    league = getLeague(year)
    scoreboard = league.box_scores(week=week)
    scores = {}
    for matchup in scoreboard:
        scores[matchup.home_team.team_name] = matchup.home_projected
        if matchup.away_team != 0:
            scores[matchup.away_team.team_name] = matchup.away_projected

    projScoresSorted = dict(sorted(scores.items(),key=lambda x:x[1],reverse=True))
    return projScoresSorted

def getRank(data, team):
    """
    Returns teams rank for week defined in getScores. 
        Parameters:
            data (dict): Sorted dict from getScores
            team (string): Team name
        Returns: 
            rank (int): Team's rank to be appended to scoreboard
    """
    rank = 10 - list(data.keys()).index(team)

    return rank

def getScoreboard(year, throughWeek):
    """
    Returns scoreboard dataframe 
        Parameters:
            year (int): Current year
            throughWeek (in): Most recent completed week
        Returns 
            scoreboard (dataframe): Table with weekly scores and cumulative total
    """
    league = getLeague(year)
    teams = [team.team_name for team in league.teams]
    
    scoreboard = pd.DataFrame(
        index=teams,
        columns=[f'Week {i}' for i in range(1,throughWeek+1)]
    )

    for i in range(1,throughWeek+1):
        data = getScores(year,i)
        for team in teams:
            scoreboard.loc[team,f'Week {i}'] = getRank(data,team)

    scoreboard['Total'] = scoreboard.sum(axis=1)
    return scoreboard.sort_values(by='Total', ascending=False)

print(getScoreboard(2022,2))
    