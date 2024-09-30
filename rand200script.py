# %%
import pandas as pd
import numpy as np
from dataRetrieval import namelist

# %%
for x in namelist:
    filename = x
    df = pd.read_csv(filename)
    random200 = df.sample(n=200, random_state=101)
    newfile = "rand200-" + filename + ".csv"
    df.to_csv(newfile, index = False)



# %%
