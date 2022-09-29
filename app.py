#! /usr/bin/env python3
# app.py - Used to render data to web page

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

# flask app
app = Flask(__name__)

# import functionality from scores.py
from scores import getLeague, getScores, getScoreboard
league = getLeague(2022)
year = league.year
current_week = league.current_week

thisWeeksScores = getScores(year,current_week)

# homepage
@app.route('/')
def index(): 
    """Home page will default to current week"""
    context = {
        'scores': thisWeeksScores,
        'week': current_week
    }
    
    return render_template('index.html',**context)
    #return f'Made it to homepage! Fetching scores from {year} Week {current_week} \n {thisWeeksScores}'

@app.route('/scoreboard', methods=('GET', 'POST'))
def scoreboard():
    """Render scoreboard for current season"""

    if request.form.get("scoreboard-week") is None:
        week = current_week
    else:
        week = int(request.form.get("scoreboard-week"))

    return redirect(url_for("updateScoreboard", week=week))

@app.route('/scoreboard/week<int:week>')
def updateScoreboard(week):
    """Change scoreboard throughWeek"""

    scoreboardTable = getScoreboard(year, week)
    columns = scoreboardTable.columns
    teams = scoreboardTable.index

    context = {
        "year": year,
        "week": week,
        "currentWeek": current_week,
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
        week = league.current_week
    else:
        year = int(request.form.get('year_select'))
        week = int(request.form.get('week_select'))

    return redirect(url_for('postScores', year=year, week=week))
    #return f'Fetching scores from {year} Week {week}'

@app.route('/archive/<int:year>Week<int:week>')
def postScores(year, week):
    """Get year and week inputs from /archive and return archived scoreboard"""

    scores = getScores(year, week)
    context = {
        "scores": scores,
        "year": year,
        "week": week
    }

    return render_template("archive.html", **context)

if __name__ == "__main__":
    app.run(debug=True,threaded=True)