#! /env/bin python3
# scores.py - does all the work getting data from the API and transforming it to fit scoreboard

import pandas as pd
from espn_api.football import League
from config import LEAGUE_ID, ESPN_S2, SWID


def firstName(owner: str) -> str:
    name = owner.split(' ')
    firstName = name[0].title()
    return firstName


class Dynasty(League):
    """Building on espn_api.football League 
    to add ED-specific functions for scoring
    """
    def __init__(self, league_id=LEAGUE_ID, year=None, espn_s2=ESPN_S2, swid=SWID):
        League.__init__(self, league_id, year, espn_s2, swid)
        self.current_season = 2023
        self.positionRank = {
            'QB': 0,
            'RB': 1,
            'WR': 2,
            'TE': 3,
            'RB/WR/TE': 4,
            'D/ST': 5,
            'K': 6
        }
        self.owner_map = {
            member['id']: member['firstName'] for member in self.members
        }



    def isProjected(self, week: int) -> bool: 
        if self.year == self.current_season and week == self.current_week:
            return True
        else:
            return False


    def get_owner_name(self, member: str) -> str: 
        for team in self.members: 
            if team['id'] == member: 
                return team['firstName'].title()
        
        return ''


    def getScore(self, matchup: object, week: int) -> tuple: 
        """Returns (home score, away score)
        Checks if year/week is actual or projected
        """
        if self.isProjected(week):
            homeScore = matchup.home_projected
            awayScore = matchup.away_projected
        else: 
            homeScore = matchup.home_score
            awayScore = matchup.away_score
        
        return (homeScore, awayScore)

    def weeklyMatchups(self, week: int) -> list[object]:
        """Returns list of matchups"""
        # .scoreboard used prior to 2021
        try: 
            matchups = self.box_scores(week)
        except: 
            matchups = self.scoreboard(week)

        return matchups

    def weekScores(self, week:int) -> dict:
        """Returns dict of teams and scores"""
        matchups = self.weeklyMatchups(week)
        scores = {}
        for matchup in matchups: 
            try: 
                #awayTeam = self.get_owner_name(matchup.away_team.owners[0])
                awayTeam = matchup.away_team.owners[0]['firstName'].title()
                scores[awayTeam] = self.getScore(matchup, week)[1]
            except Exception: 
                # seasons with 9 teams will have blank away box scores
                pass
            finally: 
                #homeTeam = self.get_owner_name(matchup.home_team.owners[0])
                homeTeam = matchup.home_team.owners[0]['firstName'].title()
                scores[homeTeam] = self.getScore(matchup, week)[0]

        scores = dict(sorted(scores.items(), 
                            key=lambda x:x[1], 
                            reverse=True))
        return scores

    def pointsFor(self, team: object, throughWeek:int) -> float:
        """Returns float of total points scored.
        team (object): Team object defined under espn_api.football
        throughWeek (int): Should not exceed current week (will return 0's)
        """
        total = 0
        for i in range(throughWeek):
            try:
                total += team.scores[i]
            except IndexError: 
                total += 0

        if throughWeek == self.current_week:
            #owner_name = self.get_owner_name(team.owners[0])
            owner_name = team.owners[0]['firstName'].title()
            total += self.weekScores(week=self.current_week)[owner_name]
        else:
            total += 0
        return total

    def seasonScoreboard(self, throughWeek:int):
        """Generates dataframe object of scoreboard through given week
        df.index (str): team owner
        df.columns (str): ['Week 1', ... 'Week <Current Week> (Proj.)',
        'Total' (int), 'Points For' (float)]
        """
        dicts = [self.weekScores(week=i) for i in range(1,throughWeek+1)]
        cols = [
            f'Week {i}' if i < self.current_week
            else f'Week {i} (Proj.)' 
            for i in range(1,throughWeek+1)
        ]
        df = pd.DataFrame(dicts,index=cols)
        scoreboard = df.transpose().rank().astype(int)
        #scoreboard = scoreboard.rank().astype(int)
        scoreboard['Total'] = scoreboard.sum(axis=1).astype(int)
        scoreboard['Points For'] = 0
        for team in self.teams:
            teamPoints = self.pointsFor(team, throughWeek=throughWeek)
            owner_name = self.get_owner_name(team.owners[0])
            scoreboard.loc[owner_name,'Points For'] = teamPoints
        scoreboard['Points For'] = scoreboard['Points For'].map('{:,.2f}'.format)
        scoreboard = scoreboard.sort_values(by=['Total', 'Points For'],ascending=False)
        return scoreboard.dropna(how='any')
    
    def lineupScores(self, boxScore: object, projected: bool = False) -> dict:
        """Returns lineup scores for given week"""
        def getLineup(lineup: list[object], projected=False) -> dict:
            """Returns starting players and their points"""
            eligible = [player for player in lineup if player.slot_position not in ['BE', 'IR']]
            results = {
                player.name: {
                    'Pos': player.slot_position,
                    'Points': player.projected_points if projected else player.points
                }
                for player in eligible
            }
            return results
        scores = {}
        for matchup in boxScore:
            scores[firstName(matchup.home_team.owner)] = getLineup(matchup.home_lineup, projected=projected)
            scores[firstName(matchup.away_team.owner)] = getLineup(matchup.away_lineup, projected=projected)
        return scores

    def weekLineup(self, owner: str, week: int) -> dict:
        """Returns dict of lineup scores for given owner on given week"""
        scores = {}
        matchups = self.weeklyMatchups(week)
        projected = self.isProjected(week)
        scores = self.lineupScores(boxScore=matchups, projected=projected)
        teamScores = scores[owner]
        teamScores = sorted(teamScores.items(), 
                            key=lambda x: self.positionRank[x[1]['Pos']])
        return teamScores


def newScoreboard(league, scoreboard, throughWeek):
    """Takes current scoreboard and truncates
    it to given throughWeek.
    scorebard (df): derived from Dynasty.seasonScoreboard
    throughWeek (int): 
    """
    cols = [f'Week {i}' 
            for i in range(1,throughWeek + 1)]
    updated = scoreboard[cols]
    updated['Total'] = updated.sum(axis=1)
    updated['Points For'] = 0
    for team in league.teams:
        owner_name = league.get_owner_name(team.owners[0]['id'])
        updated.loc[owner_name,'Points For'] = (
            league.pointsFor(team, throughWeek=throughWeek)
        )
    updated['Points For'] = updated['Points For'].map('{:,.2f}'.format)
    updated = updated.sort_values(by=['Total', 'Points For'],ascending=False)
    return updated