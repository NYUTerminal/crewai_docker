import os
import faiss
import json
import numpy as np
from crewai_tools import TXTSearchTool
from langchain.embeddings import OpenAIEmbeddings
import litellm

def load_embeddings(file_path):
    """Loads industry embeddings from a JSON file and prepares for FAISS indexing."""
    with open(file_path, "r") as file:
        industry_data = json.load(file)

    data = []
    embeddings = []

    for item in industry_data:
        for record in item.get("data", []):  # Extract from nested "data" key
            industry_id = record.get("id")
            industry_desc = record.get("content")
            embedding = record.get("embedding")

            if industry_id and industry_desc and embedding:
                data.append((industry_id, industry_desc))  # Store (ID, description)
                embeddings.append(embedding)

    # Convert to numpy array (ensure embeddings are float32)
    embeddings_array = np.array(embeddings, dtype="float32")

    return data, embeddings_array


def build_faiss_index(file_path):
    """Creates and returns a FAISS index from the industry embeddings."""
    data, embeddings_array = load_embeddings(file_path)

    # Create FAISS index
    embedding_dim = embeddings_array.shape[1]  # 768 dimensions
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings_array)

    return index, data


# Load the FAISS index
file_path = "industry-embeddings-mxs-jina-embeddings-v2-base-en.json"
faiss_index, indexed_data = build_faiss_index(file_path)


# --- Custom TXTSearchTool Using FAISS ---
class CustomTXTSearchTool(TXTSearchTool):
    def __init__(self, faiss_index, data):
        self.faiss_index = faiss_index
        self.data = data

    def get_embeddings(self, text):
        """Generate embedding for a query using OpenAI embeddings."""
        embedding_response = litellm.embedding(
            model="text-embedding-ada-002",
            input=text
        )
        return np.array([embedding_response["data"][0]["embedding"]], dtype="float32")

    def search(self, query, top_k=3):
        """Finds the most relevant company descriptions based on FAISS similarity search."""
        query_embedding = self.get_embeddings(query)

        # Perform FAISS search
        distances, indices = self.faiss_index.search(query_embedding, top_k)

        # Retrieve the matched descriptions
        results = [self.data[idx][1] for idx in indices[0] if idx < len(self.data)]
        return results


# Instantiate the tool
custom_txt_tool = CustomTXTSearchTool(faiss_index, indexed_data)

# Example Query
query = "Identify the industry of a software company building AI applications."
retrieved_text = custom_txt_tool.search(query, top_k=3)

print("🔍 Retrieved Industry Descriptions:", retrieved_text)
