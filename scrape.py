import undetected_chromedriver as uc
import os
import requests
import json
import time
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

# Initialize Selenium WebDriver with undetected Chrome
options = uc.ChromeOptions()
options.add_argument("--start-maximized")  # Maximize the browser window
driver = uc.Chrome(options=options)

def remove_elements_by_xpath(xpaths):
    """
    Removes elements from the page based on a list of XPaths.
    """
    for xpath in xpaths:
        script = f"""
        var element = document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) element.remove();
        """
        driver.execute_script(script)

def download_file(url, folder):
    """
    Downloads a file (image, PDF, etc.) and saves it to the specified folder.
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = os.path.join(folder, url.split("/")[-1])
            with open(filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def load_existing_data(json_path):
    """
    Loads existing JSON data if the file exists; otherwise, returns an empty list.
    """
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # If the file is corrupted or empty, return an empty list
    return []

def merge_data(existing_data, new_data):
    """
    Merges new data with existing data, avoiding duplicates.
    """
    for new_entry in new_data:
        if not any(entry["url"] == new_entry["url"] for entry in existing_data):
            existing_data.append(new_entry)
    return existing_data

def save_to_json(data, json_path):
    """
    Saves the merged data to a JSON file, avoiding redundancies.
    """
    existing_data = load_existing_data(json_path)
    merged_data = merge_data(existing_data, data)

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(merged_data, file, ensure_ascii=False, indent=4)

def scrape_and_collect_data(url, output_folder):
    """
    Scrapes the page, extracts the title, removes unwanted elements, collects visible assets (images, PDFs),
    and visible text (excluding specific words), and appends all data to a JSON file.
    """
    try:
        # Navigate to the URL
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Extract the title
        title_xpath = "/html/body/section[1]/div[2]/h1"
        title = driver.find_element(By.XPATH, title_xpath).text.strip()
        title_folder = os.path.join(output_folder, title.replace(" ", "_"))  # Create folder name from title

        # Ensure the title-specific folder exists
        if not os.path.exists(title_folder):
            os.makedirs(title_folder)

        # Extract Date de dernière mise à jour
        last_update_xpath = "/html/body/section[1]/div[2]/div/div/ul/li[1]/span"
        last_update = driver.find_element(By.XPATH, last_update_xpath).text.replace("Date de dernière mise à jour:", "").strip()

        # Extract Nombre de vues
        views_xpath = "/html/body/section[1]/div[2]/div/div/ul/li[2]/span"
        views = driver.find_element(By.XPATH, views_xpath).text.replace("Nombre de vues:", "").strip()

        # Remove unwanted elements
        unwanted_xpaths = [
            "/html/body/section[1]",
            "/html/body/div[2]",
            "/html/body/footer"
        ]
        remove_elements_by_xpath(unwanted_xpaths)

        # Initialize data storage for this scrape
        new_data = {
            "url": url,
            "title": title,
            "Date de dernière mise à jour": last_update,
            "Nombre de vues": views,
            "visible_text": "",
            "images": [],
            "documents": []
        }

        # Find and process images (excluding SVGs)
        images = driver.find_elements(By.TAG_NAME, "img")
        for img in images:
            src = img.get_attribute("src")
            if src and not src.endswith(".svg"):  # Exclude .svg files
                full_url = urljoin(url, src)
                if full_url not in new_data["images"]:  # Avoid duplicates
                    new_data["images"].append(full_url)
                    download_file(full_url, title_folder)

        # Find and process links for PDFs or text files
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            href = link.get_attribute("href")
            if href and (".pdf" in href or ".txt" in href or ".doc" in href):
                full_url = urljoin(url, href)
                if full_url not in new_data["documents"]:  # Avoid duplicates
                    new_data["documents"].append(full_url)
                    download_file(full_url, title_folder)

        # Extract visible text and exclude specified words/phrases
        visible_text = driver.find_element(By.TAG_NAME, "body").text
        excluded_phrases = [
            "Télécharger les termes de référence",
            "Partager Tweeter Email Partager Partager Partager Partager",
            "Espace Intranet",
            "MENU"
        ]
        for phrase in excluded_phrases:
            visible_text = visible_text.replace(phrase, "")
        new_data["visible_text"] = visible_text.strip()

        # JSON file path
        json_path = os.path.join(title_folder, "scraped_data.json")

        # Append the new data to the JSON file
        save_to_json([new_data], json_path)

        print(f"Scraping and data collection completed. Data saved in '{json_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            print("Error during WebDriver cleanup.")

# URL for scraping
ihec_url = "https://ihec.rnu.tn/fr/article/470/licence-en-informatique-de-gestion-business-intelligence"
output_directory = "ihec_assets"
scrape_and_collect_data(ihec_url, output_directory)
