#! /usr/bin/env python3
# app.py - Used to render data to web page

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

# flask app
app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)

# app routes
@app.route("/")
def index(): 
    # render live scoreboard with team & total points
    # from scores import getScores
    # scores = getScores()
    return render_template('index.html')

@app.route("/chronicle")
def chronicle(): 
    # render web version of chronicle
    return render_template("chronicle.html")

