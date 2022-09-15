#! /usr/bin/env python3
# app.py - Used to render data to web page

from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

# flask app
app = Flask(__name__)
 
# homepage
@app.route('/')
def index(): 
    """Pull scores from selected year and week"""
    return render_template('index.html')
    

@app.route('/archive', methods=['GET', 'POST'])
def archive():
    """Takes year and week from form and renders scores"""
    year = int(request.form.get('year_select'))
    week = int(request.form.get('week_select'))

    from scores import getScores
    s = getScores(year,week)
    context = {
        "scores": s,
        "year": year
    }
    return render_template("archive.html", **context)

if __name__ == "__main__":
    app.run(debug=True)