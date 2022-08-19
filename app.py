#! /usr/bin/env python3
# app.py - Used to render data to web page

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)