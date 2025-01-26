# IHEC Data Processing Pipeline

This project is a comprehensive pipeline for scraping, processing, and structuring data from the IHEC website. It utilizes several models and tools to extract, analyze, and organize data for structured insights.

## Features

1. **Data Scraping**:
   - Scrapes data from the IHEC website, including text, images, and PDF documents.
   - Handles dynamic content using Selenium with undetected-chromedriver.
   - Stores scraped data in JSON format.

2. **Image Analysis**:
   - Processes images using **LLaVA** (Large Language Vision Assistant) to generate contextual descriptions.
   - Saves detailed metadata for each image, including extracted text and visual insights.

3. **PDF Analysis**:
   - Uses FAISS (Facebook AI Similarity Search) to parse and index PDF documents.
   - Enables querying PDFs with semantic similarity searches based on embeddings from SentenceTransformers.

4. **Data Merging**:
   - Combines the scraped data with results from image and PDF analysis.
   - Structures merged data into a unified JSON format.

5. **FAQ Generation**:
   - Uses **LLaMA 3.2** to generate FAQs based on scraped and processed data.
   - Structures FAQs into categories, questions, and answers.

6. **Data Transformation**:
   - Transforms the generated FAQ into a structured JSON format with hierarchical categories.

7. **Main Pipeline**:
   - Integrates all modules into a single pipeline for end-to-end processing.

---

## Models and Tools Used

### 1. **LLaVA** (Image Analysis)
   - Extracts context and meaningful descriptions from images.
   - Handles diverse types of images like logos, documents, and event photos.

### 2. **FAISS** (PDF Processing)
   - Efficient similarity search and clustering for PDF document embeddings.
   - Enables semantic queries using `all-MiniLM-L6-v2` from SentenceTransformers.

### 3. **LLaMA 3.2** (FAQ Generation)
   - Processes text data to create categories and FAQs tailored to student needs.
   - Ensures high-quality question-answer pairs with relevant context.

### 4. **Selenium with Undetected-Chromedriver** (Scraping)
   - Navigates dynamic web pages to extract text, images, and downloadable files.

---

## Workflow

### 1. **Scraping**:
   - Use `scrape.py` to extract data from a given IHEC URL.
   - Saves assets (text, images, PDFs) in a structured directory.

### 2. **Image Processing**:
   - Run `image.py` to analyze images and generate descriptions.
   - Saves results in `image_descriptions.json`.

### 3. **PDF Indexing**:
   - Use `pdf.py` to create a FAISS index for PDF documents.
   - Allows querying and saves results in `faiss_query_results.json`.

### 4. **Data Merging**:
   - Execute `merge.py` to combine the image, PDF, and scraped data.
   - Updates `scraped_data.json` with enriched metadata.

### 5. **FAQ Generation**:
   - Use `create.py` to generate FAQs from the merged data.
   - Saves the FAQ in `student_faq.json`.

### 6. **Data Transformation**:
   - Run `transform.py` to structure FAQs into a hierarchical JSON format.
   - Saves the transformed FAQ in `transformed_faq.json`.

### 7. **Main Execution**:
   - Run `main.py` to execute the entire pipeline sequentially.
   - Outputs structured and enriched data for downstream use.

---

## File Overview

| File        | Purpose                                                   |
|-------------|-----------------------------------------------------------|
| `scrape.py` | Scrapes data from the IHEC site.                          |
| `image.py`  | Analyzes images using LLaVA for context generation.        |
| `pdf.py`    | Creates FAISS index and processes PDFs.                   |
| `merge.py`  | Merges scraped, image, and PDF data into a unified format. |
| `create.py` | Generates FAQ using LLaMA 3.2.                            |
| `transform.py` | Transforms FAQ into a structured format.                |
| `main.py`   | Executes the complete pipeline.                           |

---

## Prerequisites

1. **Python 3.8+**
2. **Dependencies**:
   - `undetected-chromedriver`
   - `requests`
   - `json`
   - `selenium`
   - `PyPDF2`
   - `sentence-transformers`
   - `faiss`
   - `ollama`

### Installation
Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Usage

### Run the Complete Pipeline:
```bash
python main.py
```

---

## Outputs

1. **Scraped Data**: JSON files with text, images, and PDFs.
2. **Image Descriptions**: Contextual metadata for each image.
3. **FAISS Results**: Semantic search results from PDFs.
4. **FAQs**: Structured question-answer pairs.
5. **Transformed Data**: Final structured JSON with categories.

---

## Author
Chedly - A creative AI enthusiast pushing boundaries in automation and data processing.

