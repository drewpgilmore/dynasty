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
            year (int): season year
        Reurns:
            league (class): League object
    """

    # init league with inputs from config
    from config import LEAGUE_ID, ESPN_S2, SWID
    try: 
        league = League(
            league_id=LEAGUE_ID,
            year=year,
            espn_s2=ESPN_S2,
            swid=SWID
        )
    except Exception as err:
        print(err)

    return league

def getScores(year, week):
    """Return dict of teams and scores for week.

    Keyword arguments:
    year (int): season year for league init
    week (int): season week #

    Returns:
    scores (dict): dict of teams & scores in {"Team A": 100, ... } format
    """
    scores = {}
    league = getLeague(year)

    # 2021 onward uses box_scores instead of scoreboard
    if year >= 2021:
        scoreboard = league.box_scores(week=week)
    else:
        scoreboard = league.scoreboard(week=week)

    # extract team names and point totals from each matchup within box score or scoreboard
    for matchup in scoreboard:
        if week < league.current_week: # check if selected week is actual or projected
            scores[matchup.home_team.team_name] = matchup.home_score
            if matchup.away_team != 0: # handle bye weeks for seasons with odd number of teams
                scores[matchup.away_team.team_name] = matchup.away_score
        else: # extract projected scores from current or future weeks
            scores[matchup.home_team.team_name] = matchup.home_projected
            if matchup.away_team != 0:
                scores[matchup.away_team.team_name] = matchup.away_projected

    # sort by points descending for single week archive display
    scores = dict(sorted(scores.items(),key=lambda x:x[1],reverse=True))

    return scores

def getPoints(data, team): # return fantasy team's points for week
    """Return team's points based on league scoreboard. 

    Keyword arguments: 
    data (dict): dict of teams and scores sorted by score, defined by getScores
    team (str): fantasy team name
    
    Returns:
    points (int): points to be displayed on scoreboard
    """
    limit = len(data) # max points team can earn is equal to number of teams in league
    points = int(limit - list(data.keys()).index(team))

    return points

def getScoreboard(year, throughWeek):
    """Return scoreboard dataframe through selected week.

    Keyword Arguments:
    year (int): season year for league init
    throughWeek (int): season week # SHOULD NOT EXCEED CURRENT WEEK

    Returns:
    scoreboard (df): pandas df with team points for each week, total, and points for columns
    """
    league = getLeague(year)
    teams = [team.team_name for team in league.teams]

    scoreboard = pd.DataFrame(
        index=teams,
        columns=[f'Week {i}' for i in range(1,throughWeek+1)] + ['Total', 'Points For']
    )

    scoreboard['Points For'] = 0

    for i in range(1,throughWeek+1):
        for team in teams:
            data = getScores(year,i)
            scoreboard.loc[team,f'Week {i}'] = getPoints(data,team)
            scoreboard.loc[team, 'Points For'] += data[team]

        if i == league.current_week:
            scoreboard.rename(columns={f'Week {i}': f'Week {i} (Proj.)'}, inplace=True)
    
    scoreboard['Total'] = scoreboard.sum(axis=1) - scoreboard['Points For']
    scoreboard['Total'].astype(int, copy=False)    
    return scoreboard.sort_values(by=['Total', 'Points For'], ascending=False)

# get list of teams players and scores
def getLineupScores(lineup): 
    """Returns dict of teams lineup with player name and score.

    Keyword arguments:
    lineup (array): list of Player objects from home_lineup or away_lineup within Matchup object

    Returns:
    lineupScores (dict): dict of lineup with names and scores
    """

    lineupScores = {}


    return lineupScores # testing func with just list of players