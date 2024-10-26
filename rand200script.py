# %%
import pandas as pd
#from dataRetrieval import namelist
from appscraper import fileNameList, namelist
# %%
'''
for x in namelist:
    filename = x
    df = pd.read_csv(filename)
    random200 = df.sample(n=200, random_state=101)
    newfile = "rand200-" + filename
    random200.to_csv(newfile, index = False)
'''

for idx in range(0, len(fileNameList)):
    filename = fileNameList[idx]
    df = pd.read_csv(filename + '.csv')
    random200 = df.sample(n=100, random_state=101, replace=True)
    newfile =   "rand200/googleplayscaper-" + namelist[idx]
    random200.to_csv(newfile, index = False)




# %%
