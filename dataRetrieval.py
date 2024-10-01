# %% [markdown]
# resources:
# https://serpapi.com/google-play-product-api
# 

# %%
import pandas as pd
import numpy as np

# %%
api_key = ""

# %%
import re
import string

def convert_suffix_to_int(input_string):
    # Remove punctuation
    no_punctuation = re.sub(r'[^\d\.KM]', '', input_string)
    
    # Handle suffixes
    if 'K' in no_punctuation:
        cleaned_string = float(no_punctuation.replace('K', '')) * 1_000
    elif 'M' in no_punctuation:
        cleaned_string = float(no_punctuation.replace('M', '')) * 1_000_000
    else:
        cleaned_string = float(no_punctuation)
    
    return int(cleaned_string)

# %%
#test query without api key
from serpapi import GoogleSearch
search = GoogleSearch({})
location_list = search.get_location("Austin", 3)
print(location_list)

# %% [markdown]
# # first will do a basic search on google for montessori android apps

# %% [markdown]
# query = GoogleSearch({"q": "montessori android apps", "serp_api_key": "993a18cf42cc984ff4528c90423e91aac2ffdba1a683630b6c9d90a85686f42e"})

# %% [markdown]
# search_result = query.get_dictionary()
# print()

# %% [markdown]
# #getting the most popular results from google search
# search_result = query.get_dictionary()
# #print(search_result)
# list_of_apps = []
# for x in range(0, len(search_result.get('organic_results'))):
#     search_id = search_result.get('organic_results')[x]['title']
#     print(search_id)
#     list_of_apps.append(search_id)
# 

# %% [markdown]
# # use this list of apps to then get a product_id

# %%
#taking app name and querying the highlight to get app review count
params = {
  "engine": "google_play",
  "q": 'montessori apps',
  "api_key": api_key
}

search = GoogleSearch(params)
app_name_results = search.get_dict()

# %%
applist = []
namelist = []
parseInt = 0

# %%
app_name_results

# %%
app_name_results['organic_results'][0]['items']

# %%
app_df = pd.DataFrame(app_name_results['organic_results'][0]['items'])

# %%
download_qual = 1000
rating_qual = 2.5
review_qual = 1000


while len(applist) < 5 and parseInt < len(app_name_results['organic_results'][0]['items']):
    product_id = app_name_results['organic_results'][0]['items'][parseInt]['product_id']
    params = {
          "engine": "google_play_product",
          "store": "apps",
          "product_id": product_id,
          #"hl": "en",
          "api_key": api_key
        }
    #no need for english parameter we want to check for qualifications first
    search = GoogleSearch(params)
    review_check_results = search.get_dict()
    name = app_name_results['organic_results'][0]['items'][parseInt]['title']
    
    #checking values
    try:
        download_count = (convert_suffix_to_int(review_check_results['product_info']['downloads']))
        rating_count = (review_check_results['product_info']['rating'])
        review_count = (review_check_results['product_info']['reviews'])
    except:
        errorString = "missing info on " + name
        print(errorString)
        continue;
    else:
        if review_count > review_qual and download_count > download_qual and rating_count > rating_qual:
            applist.append(product_id)
            namelist.append(app_name_results['organic_results'][0]['items'][parseInt]['title'])
        else:
            errorString = name + " failed to meet qualifications"
            print(errorString)
    finally:
        parseInt = parseInt + 1

# %%
review_check_results

# %%
applist

# %%
namelist

# %% [markdown]
# # same search but changes the parameter "all_reviews" to true, as the downloads, rewiews and ratings parameters are omitted with the call

# %%
for x in range(0, len(applist)):
    params = {
      "engine": "google_play_product",
      "store": "apps",
      "product_id": applist[x],
      "all_reviews": "true",
      #"hl": "en",
      "api_key": api_key,
      "num": "199"
    }
    #initializing
    search = GoogleSearch(params)
    all_reviews = search.get_dict()
    next_page_token = all_reviews['serpapi_pagination']['next_page_token']
    df = pd.DataFrame(all_reviews['reviews'])
    
    while True:
        try:
            all_reviews['serpapi_pagination']
        except:
            print("no more pages")
            break;
        else:
            params = {
              "engine": "google_play_product",
              "store": "apps",
              "product_id": product_id,
              "all_reviews": "true",
              #"page": "2",
              "num": "199",
              #"hl": "en",
              "next_page_token": next_page_token,
              "api_key": api_key
            }
            search = GoogleSearch(params)
            all_reviews = search.get_dict()
            try:
                all_reviews['serpapi_pagination']
            except:
                break;
            else:
                next_page_token = all_reviews['serpapi_pagination']['next_page_token']
            finally:
                new_df = pd.DataFrame(all_reviews['reviews'])
                df = pd.concat([df, new_df], ignore_index=True)
        finally:
            print("Execution completed.")

    name1 = namelist[x]
    name1 = name1 + ".csv"
    name1
    df.to_csv(name1, index = False)
    

# %%
all_reviews

# %%
import math
reviews_per_page = len(all_reviews['reviews'])
total_pages = int(math.ceil(review_count / reviews_per_page))
print("total pages: ", end="")
print(total_pages)

# %% [markdown]
# #things I still want to do:
#  - filter by english reviews?
#  - sentiment analysis
#   - put reviews into a dataframe

# %% [markdown]
#  - consider making a function that checks until there is no "next_page_token", so that we can call the "hl":"en" parameter
#  - we can use the dates to also make better judgements on the reviews

# %%
#that series will be appended to the dataframe with the same parameters Olivia has
#we want to filter out the author's reviews
#must convert date to something readable

# %%
namelist


