#! /env/bin python3
# scores.py - does all the work getting data from the API and transforming it to fit scoreboard

import pandas as pd
from espn_api.football import League
from config import LEAGUE_ID, ESPN_S2, SWID

def firstName(owner: str) -> str:
    """Extracts first name of team owner and title cases it"""
    name = owner.split(' ')
    firstName = name[0].title()
    return firstName

class Dynasty(League):
    """Building on espn_api.football League to add ED-specific functions for scoring"""
    def __init__(self, league_id=LEAGUE_ID, year=None, espn_s2=ESPN_S2, swid=SWID):
        League.__init__(self, league_id, year, espn_s2, swid)

    def matchupScores(self, matchup, projected=False) -> list:
        """Takes matchup and returns list of team, score tuples"""
        scoreList = [
            (firstName(matchup.home_team.owner), matchup.home_score if not projected else matchup.home_projected),
            (firstName(matchup.away_team.owner), matchup.away_score if not projected else matchup.away_projected) if matchup.away_team != 0 else None
        ]
        return scoreList

    def weekScores(self, week:int) -> dict:
        """Returns dict of teams and scores"""
        if self.year >= 2021:
            scoreboard = self.box_scores(week=week)
        else:
            # years prior to 2021 use .scoreboard instead of .box_scores
            scoreboard = self.scoreboard(week=week)
        scoreList = []
        for matchup in scoreboard:
            projected = True if week == self.current_week else False
            scoreList += self.matchupScores(matchup, projected) 
        scores = {stat[0]: stat[1] for stat in scoreList}
        scores = dict(sorted(scores.items(),key=lambda x:x[1],reverse=True))
        return scores

    def pointsFor(self, team, throughWeek:int) -> float:
        """Returns float of total points scored.
        Requires team object, not just team.owner
        throughWeek should NOT exceed current week
        """
        total = 0
        for i in range(throughWeek):
            total += team.scores[i]
        if throughWeek == self.current_week:
            total += self.weekScores(week=self.current_week)[firstName(team.owner)]
        else:
            total += 0
        return total

    def lineupScores(self, team, week:int) -> dict:
        """Returns dict of teams starting lineup with actual or projected points"""
        pass

    def seasonScoreboard(self, throughWeek:int):
        """Generates dataframe object of scoreboard through given week
        df.index (str): team owner
        df.columns (str): ['Week 1', ... 'Week <Current Week> (Proj.)', 'Total' (int), 'Points For' (float)]
        """
        dicts = [self.weekScores(week=i) for i in range(1,throughWeek+1)]
        cols = [f'Week {i}' if i < self.current_week else f'Week {i} (Proj.)' for i in range(1,throughWeek+1)]
        df = pd.DataFrame(dicts,index=cols)
        scoreboard = df.transpose()
        scoreboard = scoreboard.rank().astype(int)
        scoreboard['Total'] = scoreboard.sum(axis=1).astype(int)
        scoreboard['Points For'] = 0
        for team in self.teams:
            scoreboard.loc[firstName(team.owner),'Points For'] = self.pointsFor(team, throughWeek=throughWeek)
        scoreboard['Points For'] = scoreboard['Points For'].map('{:,.2f}'.format)
        scoreboard = scoreboard.sort_values(by=['Total', 'Points For'],ascending=False)
        return scoreboard

def newScoreboard(league, scoreboard, throughWeek):
    cols = [f'Week {i}' for i in range(1,throughWeek + 1)]
    updated = scoreboard[cols]
    updated['Total'] = updated.sum(axis=1)
    updated['Points For'] = 0
    for team in league.teams:
        updated.loc[firstName(team.owner),'Points For'] = league.pointsFor(team, throughWeek=throughWeek)
    updated['Points For'] = updated['Points For'].map('{:,.2f}'.format)
    updated = updated.sort_values(by=['Total', 'Points For'],ascending=False)
    return updated