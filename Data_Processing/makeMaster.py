import os

import pandas as pd
import numpy as np

from functions import getFormatted, write_to_master

dirs = './../Data/'
filename = 'Master.csv'


files = os.listdir(dirs)
files.remove('Append.csv')

for i, f in enumerate(files):  
    df = pd.read_csv(f'{dirs}Chunk_{i+1}.csv')
    print(f'Starting Chunk_{i+1}.csv')
    dx, lx = getFormatted(df)
    print(f'Number of Formatted Rows: {lx}')
    print('-'*10)
    write_to_master(dirs, filename, dx)
