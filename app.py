#! /usr/bin/env python3
# app.py - Used to render data to web page

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

# flask app
app = Flask(__name__)
 
# homepage
@app.route('/')
def index(): 
    # render live scoreboard with team & total points
    # from scores import getScores
    # scores = getScores()
    return render_template('index.html')

# scores
from scores import displayScores
@app.route('/scores')
def chronicle(): 
    
    return displayScores(2019, 5)

# archive
@app.route('/archive')
def archive(year, week):
    pass

if __name__ == "__main__":
    app.run(debug=True)

