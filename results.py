#! /env/bin python3
# results.py -- script for retrieving weekly scores

from scores import Dynasty
import pandas as pd

league = Dynasty(year=2022)
week = int(input('Week: '))
data = league.weekScores(week=week)

df = pd.DataFrame(
    data=data.values(),
    index=data.keys(),
    columns=['Proj. Points'] if week == league.current_week else ['Points']
)

print(df)
