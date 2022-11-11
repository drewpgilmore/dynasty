#! /env/bin python3
# scores.py - fetches league data for given week

import pandas as pd
from espn_api.football import League
from config import LEAGUE_ID, ESPN_S2, SWID

class Dynasty(League):
    """Building on espn_api.football League to add ED-specific functions for scoring"""
    def __init__(self, league_id=LEAGUE_ID, year=None, espn_s2=ESPN_S2, swid=SWID):
        League.__init__(self, league_id, year, espn_s2, swid)

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
            scoreList += self.matchupScores(matchup, projected) 
        scores = {stat[0]: stat[1] for stat in scoreList}
        scores = dict(sorted(scores.items(),key=lambda x:x[1],reverse=True))
        return scores

    def pointsFor(self, team, throughWeek:int) -> float:
        """Requires team object, not just team.team_name"""
        total = 0
        for i in range(throughWeek):
            total += team.scores[i]
        if throughWeek == self.current_week:
            total += self.weekScores(week=self.current_week)[team.team_name]
        else:
            total += 0
        return total

    def lineupScores(self, team, week:int) -> dict:
        """Returns dict of teams starting lineup with actual or projected points"""
        pass

    def seasonScoreboard(self, throughWeek:int):
        dicts = [self.weekScores(week=i) for i in range(1,throughWeek+1)]
        cols = [f'Week {i}' if i < self.current_week else f'Week {i} (Proj.)' for i in range(1,throughWeek+1)]
        df = pd.DataFrame(dicts,index=cols)
        scoreboard = df.transpose()
        scoreboard = scoreboard.rank()
        scoreboard['Total'] = scoreboard.sum(axis=1)
        scoreboard['Points For'] = 0
        for team in self.teams:
            scoreboard.loc[team.team_name,'Points For'] = self.pointsFor(team, throughWeek=throughWeek)
        scoreboard = scoreboard.sort_values(by=['Total', 'Points For'],ascending=False)
        return scoreboard