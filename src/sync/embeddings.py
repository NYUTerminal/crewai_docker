import os
import faiss
import json
import numpy as np
from crewai_tools import TXTSearchTool
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import litellm

# --- Step 1: Configure Custom LLM ---
custom_llm = litellm.Model(
    model="gpt-4",
    api_base="https://your-custom-llm-api.com/v1",
    api_key=os.getenv("CUSTOM_LLM_API_KEY")
)


# --- Step 2: Read the input file ---
def load_text_data(file_path):
    """Loads text data and returns a list of (id, text)."""
    data = []
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                data.append((parts[0], parts[1]))  # (company_id, description)
    return data


file_path = "companies.txt"
data = load_text_data(file_path)

# --- Step 3: Compute Embeddings and Store in FAISS ---
embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=os.getenv("OPENAI_API_KEY"))


def build_faiss_index(data):
    """Creates a FAISS index from the company descriptions."""
    texts = [text for _, text in data]
    embeddings = embedding_model.embed_documents(texts)

    # Convert to numpy array
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index, data


faiss_index, indexed_data = build_faiss_index(data)


# --- Step 4: Custom TXTSearchTool Using FAISS ---
class CustomTXTSearchTool(TXTSearchTool):
    def __init__(self, faiss_index, data, embedding_model):
        self.faiss_index = faiss_index
        self.data = data
        self.embedding_model = embedding_model

    def search(self, query, top_k=3):
        """Finds the most relevant company descriptions based on similarity search."""
        query_embedding = np.array([self.embedding_model.embed_query(query)])
        distances, indices = self.faiss_index.search(query_embedding, top_k)

        # Retrieve the matched descriptions
        results = [self.data[idx][1] for idx in indices[0] if idx < len(self.data)]
        return results


custom_txt_tool = CustomTXTSearchTool(faiss_index, indexed_data, embedding_model)

# --- Step 5: Define Agents ---

# Agent to retrieve relevant industry data using embeddings
text_extractor_agent = Agent(
    name="Text Extractor",
    description="Finds relevant company descriptions using embedding-based similarity search.",
    llm=custom_llm,
    tools=[custom_txt_tool],
    verbose=True
)

# Agent to classify industry based on retrieved data
industry_classifier_agent = Agent(
    name="Industry Classifier",
    description="Classifies businesses into industry codes based on retrieved text.",
    llm=custom_llm,
    tools=[],
    verbose=True
)

# --- Step 6: Define Tasks ---

# Search for relevant business information
text_extraction_task = Task(
    description="Find similar business descriptions using embeddings and classify the industry.",
    agent=text_extractor_agent,
    expected_output="Relevant industry-related company descriptions."
)

# Classify the industry
classification_task = Task(
    description="Determine the industry code based on retrieved text.",
    agent=industry_classifier_agent,
    expected_output="Industry classification code."
)

# --- Step 7: Create Crew and Execute ---
crew = Crew(agents=[text_extractor_agent, industry_classifier_agent], tasks=[text_extraction_task, classification_task])

# Example Query
query = "Identify the industry of a software company building AI applications."
retrieved_text = custom_txt_tool.search(query, top_k=3)

# Classify the retrieved text
industry_code = custom_llm.chat(
    messages=[{"role": "user",
               "content": f"Classify this company based on the following extracted text:\n\n{retrieved_text}"}]
)["choices"][0]["message"]["content"]

print(f"Industry Code: {industry_code}")
