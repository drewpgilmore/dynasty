#! /env/bin python3
# results.py -- script for retrieving weekly scores

from scores import Dynasty
import pandas as pd
import sys

week = int(sys.argv[1])
print(f'Loading Week {week} Scores...')
league = Dynasty(year=2022)
data = league.weekScores(week=week)

df = pd.DataFrame(
    data=data.values(),
    index=data.keys(),
    columns=['Proj. Points'] if week == league.current_week else ['Points']
)

print(df)
