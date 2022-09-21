from scores import *
import pandas as pd

week = int(input("Week: "))

league = getLeague(2022)
method = input('proj or actual? ')

if method == 'proj':
    data = getProjected(2022, week)
else:
    data = getScores(2022, week)

df = pd.DataFrame(
    data=data.values(), 
    index=data.keys(),
    columns=['Proj. Points'] if method == 'proj' else ['Points']
)
 
print(df)