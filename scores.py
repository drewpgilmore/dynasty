#! /usr/bin/env python3
# scores.py - fetches league data for given week

import pandas as pd
import numpy as np
import time

from espn_api.football import League
import config

ED = League(
    league_id = league_id,
    year = 2022,
    espn_s2=espn_s2
    swid=swid
)

