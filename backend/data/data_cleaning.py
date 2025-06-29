from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

def data_cleaning():
    print("started data cleaning")
    # 1. Initialization - Load Data and Set Up model
    # Change this file to the relevant data
    path = '../../_Data-20241116T221029Z-001/Data/Cleaned Data/Combined Cleaned Data.csv'
    df = pd.read_csv(path)

    # Combine relevant columns for vectorization
    # Change as necessary based on CSV columns 
    df["combined"] = (
        "Product Name: " + df.Product_Name.str.strip()+"; Brand: " + df.Brand.str.strip() 
        + "; Category: " + df.Product_Category.str.strip()
        + "; Details: " + df.Product_Details.str.strip()
        + "; Ingredients: " + df.Ingredients.str.strip()
        + "; Price: " + df["Cleaned Price"].str.strip()
        # +"; desc: "+ df.text.str.strip()
    )

    # Ensure the 'combined' column has no NaN or invalid values
    df['combined'] = df['combined'].fillna('')
    df['combined'] = df['combined'].astype(str)
    df_combined = df.copy()
    df_combined['combined'] = df_combined['combined'].str.lower() # check if lower and uppercase affects it. Make sure this works with brands with unique names (e.g. RUCA/bareMinerals)

    # model to create embeddings for our data file
    # Currently using L6 for vector embedding - six layers in transformer architecture 
    model = SentenceTransformer('all-MiniLM-L6-v2')
    """if torch.cuda.is_available():
        model = model.to('cuda')"""

    # Create embeddings for all products once at the start
    df['embeddings'] = df['combined'].apply(lambda x: model.encode(x))
    df["embedding"] = df.combined.apply(lambda x: model.encode(x))
    df = df[df['embedding'].notnull()]

    df.to_pickle("./product_embeddings.pkl") # Transform your dataframe to a pickle file, which is a byte stream file used to save a dataframe's state across sections.
    print("")
    print("")
    print(df.columns)
    print("")
    print("Data cleaning has finished and pickle file created!")
    print("")
    print("")
    
data_cleaning()