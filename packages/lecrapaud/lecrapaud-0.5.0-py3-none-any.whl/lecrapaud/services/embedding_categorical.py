import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer

# Sample DataFrame with categorical features
data = pd.DataFrame(
    {
        "SECTOR": ["Tech", "Finance", "Health", "Education", "Retail"],
        "SUBINDUSTRY": [
            "Software",
            "Banking",
            "Pharmaceuticals",
            "Online Education",
            "E-commerce",
        ],
        "LOCATION": ["USA", "UK", "Germany", "India", "Brazil"],
    }
)

# Step 1: Load a pre-trained Word2Vec-like model from Hugging Face (Sentence Transformer)
# This model generates dense vector representations (embeddings) of text
model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

# Step 2: Use the model to generate embeddings for each categorical feature
# We'll generate embeddings for each category in SECTOR, SUBINDUSTRY, and LOCATION


def get_embeddings(text_column):
    """Function to generate embeddings for a given text column."""
    return np.array([model.encode(text) for text in text_column])


# Generate embeddings for the categorical features
sector_embeddings = get_embeddings(data["SECTOR"])
subindustry_embeddings = get_embeddings(data["SUBINDUSTRY"])
location_embeddings = get_embeddings(data["LOCATION"])


# Step 3: Reduce dimensionality using PCA to k dimensions
def reduce_dimensionality(embeddings, k):
    """Function to reduce dimensionality of embeddings using PCA."""
    pca = PCA(n_components=k)
    return pca.fit_transform(embeddings)


# Set k (number of dimensions after PCA)
k = 3  # Reduce to 3 dimensions

# Apply PCA to reduce dimensionality of the embeddings
reduced_sector_embeddings = reduce_dimensionality(sector_embeddings, k)
reduced_subindustry_embeddings = reduce_dimensionality(subindustry_embeddings, k)
reduced_location_embeddings = reduce_dimensionality(location_embeddings, k)

# Step 4: Combine the reduced embeddings back into the DataFrame
# Create new DataFrames for the reduced embeddings
sector_df = pd.DataFrame(
    reduced_sector_embeddings, columns=[f"SECTOR_PC{i+1}" for i in range(k)]
)
subindustry_df = pd.DataFrame(
    reduced_subindustry_embeddings, columns=[f"SUBINDUSTRY_PC{i+1}" for i in range(k)]
)
location_df = pd.DataFrame(
    reduced_location_embeddings, columns=[f"LOCATION_PC{i+1}" for i in range(k)]
)

# Concatenate the reduced embeddings with the original data (if needed)
encoded_data = pd.concat([sector_df, subindustry_df, location_df], axis=1)

# Display the resulting DataFrame with reduced embeddings
print(encoded_data)
