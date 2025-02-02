import pandas as pd
import requests
import re
import sys


def fetch_reviews():
    url = "https://raw.githubusercontent.com/TRASJEPS/Vinicunca_AI_Project1/refs/heads/main/_Data-20241116T221029Z-001/Data/Cleaned%20Data/Combined%20Cleaned%20Data.csv"
    df = pd.read_csv(url)

    all_reviews = pd.DataFrame()
    #all_review_summaries = None
    index = 0
    for p_link in df['Product_Link']:
        p_id = re.findall("(?<=-)\\w+", p_link)[-1]
        print(index, "pimprod: ", p_id)
        index+=1
        
        page_size = 25 # max limit for ulta reviews is 25
        pages = 4
        p_reviews = reviews_per_product(p_id, page_size, pages)
        
        if all_reviews.empty: # check if all_reviews contains data
            all_reviews = p_reviews
        else:
            # add reviews to list of all reivews
            all_reviews = pd.concat([all_reviews, p_reviews], axis=0, ignore_index=True)
        
    print(all_reviews)

    # convert all reviews to csv
    all_reviews.to_csv("all_reviews.csv", index=False)

def reviews_per_product(p_id, size, pages):
    p_reviews = pd.DataFrame()
    # get 25 reviews at a time
    for i in range(pages):
        index = i*size
        # specify endpoint for the reviewurls
        reviews_url = f"https://display.powerreviews.com/m/6406/l/en_US/product/{p_id}/reviews?paging.from={index}&paging.size={size}&filters=&search=&sort=Newest&image_only=false&page_locale=en_US&_noconfig=true&apikey=daa0f241-c242-4483-afb7-4449942d1a2b"
        
        # get json data
        response = requests.get(reviews_url)
        review_data = None

        # make sure that a valid response is returned
        if response.status_code == 200:
            # get data for the reviews
            review_data = response.json()['results'][0]['reviews']
            reviews
            
            # set the data for the data frame
            df = pd.DataFrame(review_data)

            # add a column with the p_id for all data
            df.insert(0, 'Product ID', p_id)
        else:
            print("Error:", response.status_code)
            sys.exit()

        if df.empty: # check if df contains data
            p_reviews = df
        else:
            # add reviews to list of all reivews
            p_reviews = pd.concat([p_reviews, df], axis=0, ignore_index=True)

    return p_reviews

# run the function
fetch_reviews()