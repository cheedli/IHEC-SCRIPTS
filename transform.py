import json
import re

def transform_faq_file(input_file, output_file):
    """
    Transforms a JSON file containing FAQs into a structured JSON format
    with categories, questions, and answers.
    """
    try:
        # Load the input JSON
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        faq_list = []

        # Process each entry in the JSON
        for entry in data:
            main_category = entry.get("category", "Unknown Category")
            faq_text = entry.get("faq", "")

            # Split FAQ text into individual categories
            categories = re.split(r"\*\*Catégorie \d+ : ", faq_text)

            for cat_text in categories:
                if not cat_text.strip():
                    continue

                # Extract category name
                lines = cat_text.split("\n", 1)
                sub_category = lines[0].strip() if lines else main_category

                # Extract questions and answers
                qa_pairs = re.findall(r"\* (.*?)\nRéponse ?: (.*?)\n", cat_text, re.DOTALL)

                for question, answer in qa_pairs:
                    faq_list.append({
                        "category": f"{main_category} - {sub_category}",
                        "question": question.strip(),
                        "answer": answer.strip()
                    })

        # Save the transformed data to the output file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(faq_list, file, ensure_ascii=False, indent=4)

        print(f"Transformed FAQ saved to {output_file}")

    except Exception as e:
        print(f"Error processing file: {e}")

# File paths
input_file = "student_faq.json"  # Replace with the path to your input JSON file
output_file = "output.json"  # Replace with the desired path for the output JSON file

# Transform the FAQ file
transform_faq_file(input_file, output_file)
