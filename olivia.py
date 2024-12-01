from app_store_scraper import AppStore
import pandas as pd
import random
namelist = []
idlist = []
namelist.append("pok-pok-montessori-preschool")
idlist.append("1550204730")
namelist.append("toddler-games-for-2-year-olds")
idlist.append("571421198")
namelist.append("montessori-preschool-kids-3-7")
idlist.append("1138436619")
namelist.append("khan-academy-kids")
idlist.append("1378467217")
namelist.append("abc-kids-tracing-phonics")
idlist.append("1112482869")


namelist.append("preschool-games-for-kids")
idlist.append("996232516")
namelist.append("kids-math-games")
idlist.append("1565484251")

for idx in range(0,7):
    # Initialize the scraper with the app name and country code
    # app = AppStore(country="us", app_name="pok-pok-montessori-preschool", app_id="1550204730")
    # app = AppStore(country="us", app_name="toddler-games-for-2-year-olds", app_id="571421198")
    # app = AppStore(country="us", app_name="montessori-preschool-kids-3-7", app_id="1138436619")
    # app = AppStore(country="us", app_name="khan-academy-kids", app_id="1378467217")
    app = AppStore(country="us", app_name=namelist[idx], app_id=idlist[idx])
    # Scrape reviews
    app.review(how_many=1000)  # Scrape a large number of reviews to filter from
    # Convert the reviews to a DataFrame
    reviews_df = pd.DataFrame(app.reviews)
    # Convert the date to a datetime format for filtering
    reviews_df['date'] = pd.to_datetime(reviews_df['date'])
    # Filter reviews from the last 5 years
    filtered_df = reviews_df[reviews_df['date'] >= pd.Timestamp.now() - pd.DateOffset(years=5)]
    
    filtered_df.to_csv(f"final/olivia-{namelist[idx]}.csv", index=False)


"""
# Determine the number of reviews to sample
num_reviews_to_sample = min(200, len(filtered_df))
# Randomly sample reviews from the filtered DataFrame
random_sample_df = filtered_df.sample(n=num_reviews_to_sample, random_state=42)  # Set a random_state for reproducibility
# Save to CSV
random_sample_df.to_csv("random_200_app_reviews.csv", index=False)
# Display the first few rows of the sampled DataFrame
print(random_sample_df.head())
"""