# Ethan Sue & TJ first project November 2024
#
# Vinicunca
#
#

import gradio as gr
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

# 1. Initialization - Load Data and Set Up Embedder
url = 'https://raw.githubusercontent.com/hamzafarooq/maven-mlsystem-design-cohort-1/main/data/miami_hotels.csv'
df = pd.read_csv(url)

# Combine relevant columns
df["combined"] = "name: " + df.title.str.strip() + "; review: " + df.review.str.strip()
df_combined = df.copy()
df_combined['combined'] = df_combined['combined'].str.lower()

# Load embedding model and move to GPU if available
embedder = SentenceTransformer('all-mpnet-base-v2')
if torch.cuda.is_available():
    embedder = embedder.to('cuda')

# Create embeddings for all hotels once at the start
df["embedding"] = df.combined.apply(lambda x: embedder.encode(x))

# 2. Define the Search Function for Gradio
def gradio_search(query):
    # Set the number of results to display
    n = 15

    # Embed the user query
    query_embedding = embedder.encode(query)

    # Calculate similarity
    df["similarity"] = df.embedding.apply(lambda x: util.cos_sim(x, query_embedding).item())

    # Sort by similarity and return the top 'n' results
    results = df.sort_values("similarity", ascending=False).head(n)
    resultlist = []

    # Collect results in a simple format
    for r in results.index:
        resultlist.append({
            "name": results.title[r],
            "score": results.similarity[r],
            "rating": results.rating[r],
            "review": results.review[r]
        })
    return resultlist

# 3. Set up the Gradio Interface
iface = gr.Interface(
    fn=gradio_search,
    inputs="text",
    outputs="json",
    title="Hotel Recommendation Search",
    description="Enter your hotel preferences to find matching hotels!"
)

# 4. Run the App
if __name__ == "__main__":
    iface.launch()