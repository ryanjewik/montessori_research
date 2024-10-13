# %%
import pandas as pd
import numpy as np
#from dataRetrieval import namelist

# %%
'''
for x in namelist:
    filename = x
    df = pd.read_csv(filename)
    random200 = df.sample(n=200, random_state=101)
    newfile = "rand200-" + filename
    random200.to_csv(newfile, index = False)
'''
filename = "Montessori Preschool, kids 3-7.csv"
df = pd.read_csv(filename)
random200 = df.sample(n=200, random_state=101)
newfile = "rand200-" + filename
random200.to_csv(newfile, index = False)

filename = "Khan Academy Kids.csv"
df = pd.read_csv(filename)
random200 = df.sample(n=200, random_state=101)
newfile = "rand200-" + filename
random200.to_csv(newfile, index = False)


filename = "Preschool Games For Kids.csv"
df = pd.read_csv(filename)
random200 = df.sample(n=200, random_state=101)
newfile = "rand200-" + filename
random200.to_csv(newfile, index = False)



# %%
