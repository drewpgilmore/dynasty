#! /env/bin python3
# results.py -- script for retrieving weekly scores

from scores import getLeague, getScores
import pandas as pd

league = getLeague(2022)
week = int(input('Week: '))
data = getScores(league.year, week)

df = pd.DataFrame(
    data=data.values(),
    index=data.keys(),
    columns=['Proj. Points'] if week == league.current_week else ['Points']
)

print(df)
