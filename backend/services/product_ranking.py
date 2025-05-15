
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch


# Define the Ranking Function
def product_ranking(query, df):
    # define the model to use
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Set the number of results to display
    n = 15
    
    # Embed the user query
    query_embedding = model.encode(query.message)

    # Calculate similarity
    df["similarity"] = df.embedding.apply(lambda x: util.cos_sim(x, query_embedding).item())

    # Sort by similarity and return the top 'n' results
    results = df.sort_values("similarity", ascending=False).head(n)
    resultlist = []

    # Collect results in a simple format
    for r in results.index:
        resultlist.append({
            "Product Name": results.Product_Name[r],
            "Score": results.similarity[r],
            "Category": results.Product_Category[r],
            "Price": results["Cleaned Price"][r],
            "Details": results.Product_Details[r],
            "Ingredients": results.Ingredients[r],
            "Product Link": results.Product_Link[r]
        })
    return resultlist
