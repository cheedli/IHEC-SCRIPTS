import os
import faiss
import json
import numpy as np
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    """
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def create_faiss_index_from_pdfs(folder_path):
    """
    Creates a FAISS index for all PDFs in the specified folder.
    """
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"No PDFs found in folder: {folder_path}")
        return None

    # Data storage
    texts = []
    metadata = []

    # Extract text from each PDF
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Extracting text from: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
        if text:
            texts.append(text)
            metadata.append({"file_name": pdf_file, "path": pdf_path})

    # Generate embeddings for the extracted text
    print("Generating embeddings...")
    embeddings = model.encode(texts, convert_to_tensor=False)
    embeddings = np.array(embeddings).astype('float32')

    # Create FAISS index
    print("Creating FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity
    index.add(embeddings)  # Add embeddings to the index

    # Save metadata for reference
    index_data = {
        "index": index,
        "metadata": metadata,
        "texts": texts
    }

    print("FAISS index created successfully.")
    return index_data

def query_faiss_index(index_data, query, top_k=5, folder_path=None):
    """
    Queries the FAISS index with the given query and saves the top_k results in the folder.
    """
    if not index_data:
        print("No index data available.")
        return

    # Generate embedding for the query
    print(f"Querying FAISS index for: {query}")
    query_embedding = model.encode([query], convert_to_tensor=False)
    query_embedding = np.array(query_embedding).astype('float32')

    # Perform search
    distances, indices = index_data["index"].search(query_embedding, top_k)

    # Fetch results
    results = []
    for i, idx in enumerate(indices[0]):
        result = {
            "file_name": index_data["metadata"][idx]["file_name"],
            "path": index_data["metadata"][idx]["path"],
            "text_snippet": index_data["texts"][idx][:500]  # First 500 characters
        }
        results.append(result)

    # Save results to a JSON file in the specified folder
    if folder_path:
        # Ensure folder exists
        os.makedirs(folder_path, exist_ok=True)

        # Define results file path
        results_file = os.path.join(folder_path, "faiss_query_results.json")
        try:
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            print(f"Query results saved in: {results_file}")
        except Exception as e:
            print(f"Error saving query results: {e}")

    return results

# Example Usage
folder_path = r"ihec_assets\Licence_en_Informatique_de_Gestion_-_Business_Intelligence"  # Replace with your folder path
index_data = create_faiss_index_from_pdfs(folder_path)

if index_data:
    query = "Find information about courses"  # Replace with your query
    query_results = query_faiss_index(index_data, query, folder_path=folder_path)

    # If you want to verify the results:
    print("\nQuery Results Saved!")
