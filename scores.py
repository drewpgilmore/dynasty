#! /env/bin python3
# scores.py - fetches league data for given week

import pandas as pd
from espn_api.football import League
from config import LEAGUE_ID, ESPN_S2, SWID

def getLeague(year: int) -> League:
    """Creates league instance for given year"""
    # init league with inputs from config
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

def getScores(year: int, week: int) -> dict: 
    """Return dict of teams and scores for week."""
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

def getPoints(year: int, week: int) -> dict: # return fantasy team's points for week
    """Return team's points based on league scoreboard."""
    points = {}
    scores = getScores(year, week)
    limit = len(scores) # max points team can earn is equal to number of teams in league
    teams = list(scores.keys())
    points = {team: int(limit - teams.index(team)) for team in teams}
    return points

def getScoreboard(year: int, throughWeek: int) -> pd.DataFrame:
    """Return scoreboard dataframe through selected week."""
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
    scoreboard['Total'] = scoreboard['Total'].astype(int)    
    scoreboard['Points For'] = scoreboard['Points For'].round(decimals=2)
    scoreboard = scoreboard.sort_values(by=['Total', 'Points For'], ascending=False)
    return scoreboard

def getLineupScores(lineup): 
    """Returns dict of teams lineup with player name and score"""
    lineupScores = {}
    return lineupScores # testing func with just list of players

class Dynasty(League):
    def matchupScores(self, matchup, projected=False) -> list:
        """Takes matchup and returns list of team, score tuples"""
        scoreList = [
            (matchup.home_team.team_name, matchup.home_score if not projected else matchup.home_projected),
            (matchup.away_team.team_name, matchup.away_score if not projected else matchup.away_projected) if matchup.away_team != 0 else None
        ]
        return scoreList

    def weekScores(self, week:int) -> dict:
        """Returns dict of teams and scores"""
        if self.year >= 2021:
            # years prior to 2021 do not use box_scores
            scoreboard = self.box_scores(week=week)
        else:
            scoreboard = self.scoreboard(week=week)
        
        scoreList = []
        for matchup in scoreboard:
            projected = True if week == self.current_week else False
            scoreList += self.matchupScores(matchup,projected) 

        return scoreList

ed = Dynasty(year=2022)
sl = ed.weekScores(week=9)
print(sl)

    