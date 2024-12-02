
# %% googleplayscraper
# resources:
# https://serpapi.com/google-play-product-api
# 

# %%
from google_play_scraper import app
from google_play_scraper import Sort, reviews_all
import pandas as pd
import numpy as np

# %%
import string
def string_to_integer(input_str):
    # Remove punctuation from the string
    cleaned_str = input_str.translate(str.maketrans('', '', string.punctuation))
    # Convert the cleaned string to an integer
    try:
        return int(cleaned_str)
    except ValueError:
        raise ValueError("The input string does not contain a valid integer after removing punctuation.")

import re

def clean_filename(filename):
    # Define a regex pattern for characters not allowed in filenames
    invalid_chars = r'[\/:*?"<>|]'
    # Replace invalid characters with an underscore
    cleaned_filename = re.sub(invalid_chars, '_', filename)
    cleaned_filename = cleaned_filename.replace("_", "-")
    cleaned_filename = cleaned_filename.replace(" ", "-")
    cleaned_filename = cleaned_filename.lower()
    return cleaned_filename

# %% [markdown]
# reviews_all function returns all of reviews from app. If you want to set the count to infinity while using the reviews function, you can use the reviews_all function.
# 
# :bulb: Because of the Google Play Store limit (up to 200 reviews can be fetched at a time), http requests are generated as long as the number of app reviews is divided by 200. For example, targeting an app like Pokémon GO makes tens of thousands of http requests.

# %%
from google_play_scraper import search

#app search
result = search(
    "Montessori",
    lang="en",  # defaults to 'en'
    country="us",  # defaults to 'us'
    n_hits=30  # defaults to 30 (= Google's maximum)
)

# %%
appIds = []
for x in result:
    appIds.append(x['appId'])

# %%
#we use this function if we want total reviews period
applist = []
namelist = []
for idx in range(0, len(result)):
    if len(applist) == 5:
        break
    print(f"{idx} ------------------")
    print(result[idx]['title'])
    print(result[idx]['score'])
    print(result[idx]['installs'])
    print(result[idx]['appId'])
    
    if (result[idx]['score'] > 3.0) and (string_to_integer(result[idx]['installs']) > 3000):
        applist.append(result[idx]['appId'])
        namelist.append(result[idx]['title'])
    
            

# %%
namelist

# %%
applist
"""
# %%
#we use this function if we want reviews retrieved with api
applist = []
namelist = []
for idx in range(0, len(result)):
    if len(applist) == 5:
        break
    print(f"{idx} ------------------")
    print(result[idx]['title'])
    print(result[idx]['score'])
    print(result[idx]['installs'])
    print(result[idx]['appId'])
    
    reviews = reviews_all(
        result[idx]['appId'],
        sleep_milliseconds=0, # defaults to 0
        lang='en', # defaults to 'en'
        country='us', # defaults to 'us'
        sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
    )
    print(len(reviews))
    review_count = len(reviews)
    
    
    if (result[idx]['score'] > 3.0) and ((review_count) > 3000):
        applist.append(result[idx]['appId'])
        namelist.append(result[idx]['title'])

# %%
namelist

# %%
applist
"""
fileNameList = []
# %%
#adds all the reviews to a dataframe
for idx in range(0, len(applist)):
    app_df = pd.DataFrame()
    result = reviews_all(
        applist[idx],
        sleep_milliseconds=0, # defaults to 0
        lang='en', # defaults to 'en'
        country='us', # defaults to 'us'
        sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
    )
    for review in result:
        developerResponse = review
        date = review['at']
        userName = review['userName']
        reviewText = review['content']
        score = review['score']
        #can't get title
        #can't get isEdited
        review_df = pd.DataFrame({'developerResponse': [developerResponse],  'date': [date], 'review': [reviewText], 
                                   'score': [score], 'userName': [userName],})
        fileName = "final/g-" + clean_filename(namelist[idx])
        review_df['IOS'] = 0
        review_df['Name'] = clean_filename(namelist[idx])
        app_df = pd.concat([app_df, review_df], ignore_index = True)
    fileNameList.append(fileName)
    app_df.to_csv(fileName + ".csv", index = False)
    #rand200 = app_df.sample(n=100, random_state=101, replace = True)
    #rand200.to_csv("rand200/googleplayscraper-" + clean_filename(namelist[idx]), index = False)

# %% [markdown]
#  - date
#  - json response (developerResponse)
#  - review text (review)
#  - rating
#  - isEdited
#  - userName
#  - title

# %%



