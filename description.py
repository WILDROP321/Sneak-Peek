import google.generativeai as genai
import json
import time
from google.generativeai.types import HarmCategory, HarmBlockThreshold

API_KEY = "AIzaSyCZeUvjbs_kx7VMz2a3FNLigwdmXA-3qHA"

def description(NAME, RATING, category):
    genai.configure(api_key=API_KEY)

    prompts = {
        'cafe': f"Write a description in 80 words for a cafe called {NAME}, with rating {RATING}",
        'date': f"Write a description in 80 words for a romantic restaurant called {NAME}, with rating {RATING}",
        'featured': f"Write a description in 80 words for a featured restaurant called {NAME}, with rating {RATING}",
        'microbrewery': f"Write a description in 80 words for a microbrewery in Bangalore called {NAME}, with rating {RATING}",
        'newlyOpened': f"Write a description in 80 words for a newly opened restaurant in Bangalore called {NAME}, with rating {RATING}",
        'pubandbar': f"Write a description in 80 words for a pub/bar called {NAME}, with rating {RATING}",
        'rooftop': f"Write a description in 80 words for a cool rooftop restaurant called {NAME}, with rating {RATING}",
        'trending': f"Write a description in 80 words of the trending place in Bangalore called {NAME}, with rating {RATING}"
    }

    prompt = prompts.get(category, "No description available for this category.")
    
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt, stream=True, generation_config = genai.GenerationConfig(temperature=0.1), safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        })
        # Wait for the response to complete
        response.resolve()
        desc = response.text
    except Exception as e:
        print(f"Error generating description: {e}")
        desc = "Description could not be generated."
    return desc

def getDesc():
    try:
        with open('DATA/process.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: 'process.json' file not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from 'process.json'.")
        return

    # Iterate through keys in the JSON data
    for key in data:
        for item in data[key]:
            if 'Ratings' in item and 'name' in item:
                rating = item.get('Ratings', 'No rating')
                name = item['name']
                print(f"Processing: {name}")
                NAME = f"{name}"
                RATING = f"{rating}"
                category = key
                print(category)
                # Get description
                desc = description(NAME, RATING, category)
                # Update description in the item
                item['description'] = desc

                time.sleep(10)  # Adjust the sleep time as needed

    # Save the updated JSON data back to the file
    with open('DATA/process.json', 'w') as file:
        json.dump(data, file, indent=4)
    print('Description has been updated')

