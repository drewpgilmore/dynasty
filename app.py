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
currentScoreboard = getScoreboard(year,current_week-1)
projectedScoreboard = getScoreboard(year,current_week)

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

@app.route('/scoreboard')
def scoreboard():
    """Render scoreboard for current season"""
    scoreboardTable = projectedScoreboard
    columns = scoreboardTable.columns
    teams = projectedScoreboard.index
    
    context = {
        "scoreboardTable": scoreboardTable,
        "columns": columns
    }

    return render_template("scoreboard.html",**context)

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