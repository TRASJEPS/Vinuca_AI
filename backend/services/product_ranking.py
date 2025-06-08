
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import numpy as np
from pathlib import Path
import ast

def convert_embedding(x):
    if isinstance(x, str):
        try:
            # Convert the string representation of the list into an actual list
            return np.array(ast.literal_eval(x))  # Use numpy array for better handling
        except Exception as e:
            print(f"Error converting embedding: {e}")
            return None  # Handle error if needed
    return x  # If it's already in a correct format, return as is

# Define the Ranking Function
def product_ranking(query):
    # Get the directory where the current script is located
    script_dir = Path(__file__).parent
    # Go up one level to project root, then into data
    pkl_path = script_dir.parent / "data" / "product_embeddings.pkl"

    # Check if file exists
    if pkl_path.exists():
        print(f"File found at: {pkl_path}")
    else:
        print(f"File not found at: {pkl_path}")
    
    # Load the DataFrame from the pickle file
    df = pd.read_pickle(pkl_path)

    # Convert the embedding column to numpy arrays using the convert_embedding function
    df['embedding'] = df['embedding'].apply(convert_embedding)
    
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
