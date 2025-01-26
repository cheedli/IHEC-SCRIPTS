import os
import json

def load_json(file_path):
    """
    Loads a JSON file and returns its content.
    """
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return None

def save_json(data, file_path):
    """
    Saves data to a JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Updated JSON saved at: {file_path}")

def update_scraped_data(folder_path):
    """
    Updates the 'images' and 'documents' sections in scraped_data.json with data from 
    image_descriptions.json and faiss_query_results.json.
    """
    # Define expected file names
    scraped_file = os.path.join(folder_path, "scraped_data.json")
    image_file = os.path.join(folder_path, "image_descriptions.json")
    pdf_file = os.path.join(folder_path, "faiss_query_results.json")

    # Load JSON files
    scraped_data = load_json(scraped_file)
    image_data = load_json(image_file)
    pdf_data = load_json(pdf_file)

    if not scraped_data:
        print(f"Error: '{scraped_file}' not found or invalid.")
        return
    if not image_data:
        print(f"Error: '{image_file}' not found or invalid.")
        return
    if not pdf_data:
        print(f"Error: '{pdf_file}' not found or invalid.")
        return

    # Ensure scraped_data is a list
    if not isinstance(scraped_data, list):
        print("Error: scraped_data is not a list.")
        return

    # Update each entry in scraped_data
    for entry in scraped_data:
        if not isinstance(entry, dict):
            print("Warning: Entry in scraped_data is not a dictionary. Skipping...")
            continue

        # Process images
        updated_images = []
        for img_url in entry.get("images", []):
            file_name = os.path.basename(img_url)  # Extract file name from URL
            # Find matching description in image_data
            description = next((img["description"] for img in image_data if img["file_name"] == file_name), "No description available.")
            updated_images.append({
                "url": img_url,
                "file_name": file_name,
                "description": description
            })
        entry["images"] = updated_images  # Replace with detailed entries

        # Process PDFs
        updated_documents = []
        for doc_url in entry.get("documents", []):
            file_name = os.path.basename(doc_url)  # Extract file name from URL
            # Find matching metadata in pdf_data
            snippet = None
            if isinstance(pdf_data, dict):
                # Check if the structure is a dictionary
                for i, meta in enumerate(pdf_data.get("metadata", [])):
                    if meta["file_name"] == file_name:
                        snippet = pdf_data["texts"][i][:500]  # Extract first 500 characters
                        break
            elif isinstance(pdf_data, list):
                # Check if the structure is a list
                for pdf_entry in pdf_data:
                    if pdf_entry.get("file_name") == file_name:
                        snippet = pdf_entry.get("text_snippet", "")[:500]
                        break
            updated_documents.append({
                "url": doc_url,
                "file_name": file_name,
                "text_snippet": snippet or "No snippet available."
            })
        entry["documents"] = updated_documents  # Replace with detailed entries

    # Save the updated scrape data
    save_json(scraped_data, scraped_file)

# Example usage
folder_path = r"ihec_assets/Licence_en_Informatique_de_Gestion_-_Business_Intelligence"  # Replace with your folder path
update_scraped_data(folder_path)
