import os
import scrape
import image
import pdf
import merge
import create
import transform
import json
import sys


def find_newest_folder(base_path):
    """
    Finds the most recently created folder in the specified base directory.
    """
    folders = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    if not folders:
        raise FileNotFoundError(f"No folders found in {base_path}")
    return max(folders, key=os.path.getctime)  # Get the newest folder by creation time

if True :
    
    # Step 1: Scrape data from the provided link
    scrape_url = "https://ihec.rnu.tn/fr/article/470/licence-en-informatique-de-gestion-business-intelligence"
    output_directory = "ihec_assets"  # Base directory where data will be saved
    print("Starting scraping...")
    scrape.scrape_and_collect_data(scrape_url, output_directory)

    # Step 2: Dynamically detect the newly created folder
    print("Detecting newly created folder...")
    new_folder_path = find_newest_folder(output_directory)
    print(f"Newly created folder detected: {new_folder_path}")

    # Step 3: Process images in the newly created folder
    print("Processing images...")
    image.describe_images_in_folder(new_folder_path)

    # Step 4: Process PDFs in the same folder and create a FAISS index
    print("Processing PDFs...")
    index_data = pdf.create_faiss_index_from_pdfs(new_folder_path)
    if index_data:
        query = "Sample Query"
        pdf.query_faiss_index(index_data, query, folder_path=new_folder_path)

    # Step 5: Merge processed image and PDF data into the scraped data
    print("Merging data...")
    merge.update_scraped_data(new_folder_path)

    # Step 6: Generate FAQ from the merged data
    print("Generating FAQ...")
    scraped_file = os.path.join(new_folder_path, "scraped_data.json")
    faq_output_file = os.path.join(new_folder_path, "student_faq.json")
    try:
        with open(scraped_file, "r", encoding="utf-8") as file:
            scraped_data = json.load(file)
        faq_list = create.generate_faq(scraped_data)
        create.save_faq_to_json(faq_list, faq_output_file)
    except Exception as e:
        print(f"Error generating FAQ: {e}")

    # Step 7: Transform FAQ into the desired format
    print("Transforming FAQ...")
    transformed_output_file = os.path.join(new_folder_path, "transformed_faq.json")
    transform.transform_faq_file(faq_output_file, transformed_output_file)

    print(f"Process completed. Final transformed FAQ saved at: {transformed_output_file}")
    sys.exit(0)

