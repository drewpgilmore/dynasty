#! /usr/bin python3
# app.py - Used to render data to web page

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from scores import Dynasty, firstName, newScoreboard
import pandas as pd
import json
from sample_league import alias 
import requests

# Flask app
app = Flask(__name__)

# Initiate league with current week
current_season = 2022
league = Dynasty(year=current_season)
last_reg_week = 14 # keep current week as last week of regular season
current_week = min([last_reg_week, league.current_week])
current_scores = league.weekScores(week=current_week)
current_scoreboard = league.seasonScoreboard(throughWeek=current_week)


# About
@app.route('/')
def index():
    """Landing page containing info about the app"""
    return render_template("index.html")

@app.route('/info')
def info():
    """Longer description about how the scoreboard works"""
    return render_template("info.html")

# League home
@app.route('/league/<int:league_id>')
def league(league_id:int):
    """Takes user to specified league page"""
    url = 'https://espn.com'
    response = requests.get(url)
    swid = response.cookies.get('SWID')
    
    league = Dynasty(
        league_id=league_id,
        year=current_season,
        swid=swid
    )

    current_scores = league.weekScores(week=14)
    return current_scores


@app.route('/scores')
def scores(): 
    """Display projected points for current week"""
    context = {
        'league_name': alias['league_name'],
        'alias': alias,
        'scores': current_scores,
        'year': current_season,
        'week': current_week
    }
    return render_template('scores.html',**context)


@app.route('/scoreboard', methods=('GET', 'POST'))
def scoreboard():
    """Render scoreboard for current season"""
    league = Dynasty(year=current_season)
    if request.form.get("scoreboard-week") is None:
        week = current_week
    else:
        week = int(request.form.get("scoreboard-week"))
    context = {
        'alias': alias,
        'week': week
    }
    return redirect(url_for("updateScoreboard", **context))


@app.route('/scoreboard/week<int:week>')
def updateScoreboard(week):
    """Change scoreboard throughWeek"""
    if week == current_week:
        scoreboard_table = current_scoreboard
    else: 
        league = Dynasty(year=current_season)
        scoreboard_table = newScoreboard(league, current_scoreboard, week)
    columns = scoreboard_table.columns
    teams = scoreboard_table.index
    context = {
        "alias": alias,
        "year": current_season,
        "week": week,
        "currentWeek": current_week,
        "scoreboardTable": scoreboard_table,
        "columns": columns
    }
    return render_template("scoreboard.html", **context)


@app.route('/archive', methods=('GET', 'POST'))
def archive():
    """Takes year and week from form and renders scores, should default to current week"""
    if request.form.get('year_select') is not None:
        year = int(request.form.get('year_select'))
        week = int(request.form.get('week_select'))
        return redirect(url_for('postScores', year=year, week=week, alias=alias))
    else:
        return redirect(url_for('postScores', year=current_season, week=current_week, alias=alias))


@app.route('/archive/<int:year>/<int:week>')
def postScores(year, week):
    """Get year and week inputs from /archive and return archived scoreboard"""
    league = Dynasty(year=year)
    scores = league.weekScores(week=week)
    context = {
        "alias": alias,
        "scores": scores,
        "year": year,
        "week": week
    }
    return render_template("archive.html", **context)


@app.route('/lineup/<string:owner>/week<int:week>_<int:year>')
def displayLineup(owner, year, week): 
    """Displays starting lineup"""
    league = Dynasty(year=year)
    try: 
        lineupScores = league.weekLineup(owner, week)
    except AttributeError: 
        return render_template("error.html", alias=alias)
    totalPoints = league.weekScores(week)[owner]
    context = {
        "alias": alias,
        "week": week,
        "owner": owner,
        "lineup": lineupScores,
        "total": totalPoints
    }
    return render_template("lineup.html", **context)


# API endpoints
@app.route('/player/<string:player>')
def playerData(player): 
    player_info = league.player_info(player).stats
    data = json.dumps(player_info)
    return data


@app.route('/league_id=<int:league_id>')
def leagueHome(league_id):
    """Returns other league pages"""
    league = Dynasty(league_id=league_id, year=2022)
    current_scores = league.weekScores(week=current_week)
    current_scoreboard = league.seasonScoreboard(throughWeek=current_week)
    return current_scoreboard.to_html()


if __name__ == "__main__":
    app.run(debug=True, threaded=True)