import pandas as pd
import requests
import re

url = "https://raw.githubusercontent.com/TRASJEPS/Vinicunca_AI_Project1/refs/heads/main/_Data-20241116T221029Z-001/Data/Cleaned%20Data/Combined%20Cleaned%20Data.csv"
df = pd.read_csv(url)
for p_link in df['Product_Link']:
    p_id = re.findall("(?<=-)\\w+", p_link)[-1]
    print("pimprod: ", p_id)

    # fill in base reviews url using id attribute
    #for i in range(5):
    start_i = 5

    # get json data

    reviews_url = f"https://display.powerreviews.com/m/6406/l/en_US/product/{p_id}/reviews?paging.from={start_i}&paging.size=5&filters=&search=&sort=Newest&image_only=false&page_locale=en_US&_noconfig=true&apikey=daa0f241-c242-4483-afb7-4449942d1a2b"
    review_data = requests.get(reviews_url).json()
    print (review_data)