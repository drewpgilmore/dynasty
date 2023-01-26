#! /usr/bin python3
# app.py - Used to render data to web page

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from scores import Dynasty, firstName, newScoreboard
import pandas as pd

# flask app
app = Flask(__name__)

# initiate league with current week
league = Dynasty(year=2022)
currentWeek = 14 # keep current week as last week of regular season
currentScores = league.weekScores(week=currentWeek)
currentScoreboard = league.seasonScoreboard(throughWeek=currentWeek)


# homepage
@app.route('/')
def index(): 
    """Home page will default to current week"""
    context = {
        'scores': currentScores,
        'year': league.year,
        'week': currentWeek
    }
    
    return render_template('index.html',**context)


@app.route('/scoreboard', methods=('GET', 'POST'))
def scoreboard():
    """Render scoreboard for current season"""

    if request.form.get("scoreboard-week") is None:
        week = currentWeek
    else:
        week = int(request.form.get("scoreboard-week"))

    return redirect(url_for("updateScoreboard", week=week))


@app.route('/scoreboard/week<int:week>')
def updateScoreboard(week):
    """Change scoreboard throughWeek"""

    if week == currentWeek:
        scoreboardTable = currentScoreboard
    else: 
        scoreboardTable = newScoreboard(league, currentScoreboard, week)
    
    columns = scoreboardTable.columns
    teams = scoreboardTable.index

    context = {
        "year": league.year,
        "week": week,
        "currentWeek": currentWeek,
        "scoreboardTable": scoreboardTable,
        "columns": columns
    }

    #return scoreboardTable.to_html()
    return render_template("scoreboard.html", **context)


@app.route('/archive', methods=('GET', 'POST'))
def archive():
    """Takes year and week from form and renders scores, should default to current week"""

    if request.form.get('year_select') is None:
        year = league.year
        week = currentWeek
    else:
        year = int(request.form.get('year_select'))
        week = int(request.form.get('week_select'))

    return redirect(url_for('postScores', year=year, week=week))


@app.route('/archive/week<int:week>_<int:year>')
def postScores(year, week):
    """Get year and week inputs from /archive and return archived scoreboard"""
    league = Dynasty(year=year)
    scores = league.weekScores(week=week)
    context = {
        "scores": scores,
        "year": year,
        "week": week
    }
    return render_template("archive.html", **context)


@app.route('/lineup/<string:owner>/week<int:week>_<int:year>')
def displayLineup(owner, year, week): 
    league = Dynasty(year=year)
    try: 
        lineupScores = league.weekLineup(owner, week)
    except AttributeError: 
        return render_template("error.html")
        
    totalPoints = league.weekScores(week)[owner]
    context = {
        "owner": owner,
        "lineup": lineupScores,
        "total": totalPoints
    }
    return render_template("lineup.html", **context)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)