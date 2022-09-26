import pandas as pd
from scores import getScoreboard

week = int(input('Through Week: '))

df = getScoreboard(2022, week)

print()