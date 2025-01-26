import os
import json
import ollama

def generate_description_with_ollama(image_path):
    """
    Generates a description for the given image using the LLaVA model in Ollama.
    """
    try:
      with open(image_path, 'rb') as file:
            response = ollama.chat(
                model='llava',
                messages=[
                    {
                        'role': 'user',
                        'content': (
                            "Analysez cette image en détail et répondez en français. "
                            "Si l'image contient du texte, extrayez-le avec précision. "
                            "Si c'est un logo, décrivez son design, ses couleurs et ses éléments. "
                            "Si elle montre un événement ou des personnes, décrivez le contexte, les activités et les émotions. "
                            "Pour les documents ou les infographies, résumez leur contenu et leur mise en page. "
                            "Concentrez-vous sur des thèmes éducatifs, institutionnels ou professionnels, car cela concerne un site universitaire."
                        ),
                        'images': [file.read()],
                    },
                ],
            )

            # Extract the description from the response
            return response.get('message', {}).get('content', 'No description available.')
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return "Error generating description."

def describe_images_in_folder(folder_path):
    """
    Processes all images in the specified folder and generates descriptions for each.
    Saves the descriptions in a JSON file.
    """
    # Supported image formats
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_formats)]

    if not image_files:
        print(f"No images found in folder: {folder_path}")
        return

    # Initialize data for JSON output
    descriptions = []

    # Process each image
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"Processing: {image_path}")

        # Generate description
        description = generate_description_with_ollama(image_path)
        descriptions.append({
            "file_name": image_file,
            "path": image_path,
            "description": description
        })

    # Save descriptions to a JSON file
    output_file = os.path.join(folder_path, "image_descriptions.json")
    try:
        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(descriptions, json_file, ensure_ascii=False, indent=4)
        print(f"Descriptions saved in: {output_file}")
    except Exception as e:
        print(f"Error saving descriptions: {e}")

# Example Usage
folder_path = "ihec_assets\Licence_en_Informatique_de_Gestion_-_Business_Intelligence"  # Replace with your folder path
describe_images_in_folder(folder_path)
