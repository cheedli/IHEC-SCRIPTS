import json
import ollama

SCHOOL_DESCRIPTION = (
    "IHEC (Institut des Hautes Études Commerciales) est une école de commerce de renom en Tunisie, "
    "offrant des formations en gestion, informatique, commerce et autres disciplines liées aux affaires. "
    "L'école est connue pour son excellence académique, son réseau professionnel, "
    "et son engagement envers les étudiants."
)

def ask_llama(prompt: str) -> str:
    """
    Generates a response from the specified Llama model via Ollama.
    Returns a fallback string if the query fails or no response is available.
    """
    try:
        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.get("message", {}).get("content", "No response available.")
    except Exception as e:
        print(f"Error querying Llama: {e}")
        return "Error generating response."

def generate_prompt(document_title: str, text_content: str) -> str:
    """
    Creates a French-language prompt for IHEC student FAQs based on the provided text content.
    """
    return (
        f"Lisez le texte suivant, destiné aux étudiants de l'IHEC, et générez des catégories pertinentes. "
        f"Pour chaque catégorie, proposez une ou plusieurs questions que les étudiants pourraient poser, "
        f"et fournissez des réponses claires et utiles. Voici une brève description de l'IHEC :\n\n"
        f"{SCHOOL_DESCRIPTION}\n\n"
        f"{text_content}"
    )

def generate_faq(scraped_data: list) -> list:
    """
    Processes scraped data, filtering out trivial content, and generates
    a student-relevant FAQ in the desired format.
    """
    faq = []

    for entry in scraped_data:
        title = entry.get("title", "Titre Inconnu")
        visible_text = entry.get("visible_text", "").strip()
        documents = entry.get("documents", [])

        # Skip if the visible text is too short or empty (not useful for students)
        if len(visible_text) > 50:  
            prompt = generate_prompt(title, visible_text)
            faq_response = ask_llama(prompt)
            faq.append({
                "category": f"Informations sur {title}",
                "faq": faq_response
            })

        # Process documents
        for doc in documents:
            file_name = doc.get("file_name", "Document Inconnu")
            snippet = doc.get("text_snippet", "").strip()

            # Skip if document snippet is trivial
            if len(snippet) > 50:
                prompt = generate_prompt(file_name, snippet)
                doc_faq_response = ask_llama(prompt)
                faq.append({
                    "category": f"Informations sur {file_name}",
                    "faq": doc_faq_response
                })

    return faq

def save_faq_to_json(faq: list, output_file: str) -> None:
    """
    Saves the generated FAQ to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(faq, file, ensure_ascii=False, indent=4)
    print(f"Generated FAQ saved to {output_file}")

if __name__ == "__main__":
    input_file = r"ihec_assets\Licence_en_Informatique_de_Gestion_-_Business_Intelligence\scraped_data.json"
    output_file = "student_faq.json"

    # Load scraped data
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            scraped_data = json.load(file)
    except Exception as e:
        print(f"Error loading scraped data: {e}")
        scraped_data = []

    # Generate FAQ
    if scraped_data:
        faq_list = generate_faq(scraped_data)
        save_faq_to_json(faq_list, output_file)
    else:
        print("No data found in the scraped data file.")
