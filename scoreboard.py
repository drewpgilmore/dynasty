import pandas as pd
import scores

week = int(input('Through Week: '))
method = input('proj or actual? ')

df = pd.DataFrame(
    data=data.values(), 
    index=data.keys(),
    columns=['Proj. Points'] if method == 'proj' else ['Points']
) 