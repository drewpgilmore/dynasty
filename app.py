#! /usr/bin/env python3
# app.py - Used to return scores to webpage

from flask import Flask, render_template, redirect

import pandas as pd
import numpy as np
import espn_api.football

app = Flask(__name__)