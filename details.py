import requests
import json
import time
import random
import os

def sort():
    files = ['cafe', 'date', 'featured', 'microbrewery', 'newlyOpened', 'pubandbar', 'rooftop', 'trending']

    # Check if 'DATA/previousdata.jsonl' exists and read names from it
    names_in_previous_data = set()
    if os.path.exists('DATA/previousdata.jsonl'):
        with open('DATA/previousdata.jsonl', 'r') as f:
            for line in f:
                data = json.loads(line)
                if 'name' in data:
                    names_in_previous_data.add(data['name'])
    else:
        print("'DATA/previousdata.jsonl' does not exist. Skipping name filtering.")

    # For each file, load the data and select a random object
    for file_name in files:
        file_path = f'DATA/{file_name}.json'
        if not os.path.exists(file_path):
            print(f"'{file_path}' does not exist. Skipping file.")
            continue

        with open(file_path, 'r') as f:
            data = json.load(f)

        l = len(data['Place'])
        valid_content_found = False

        # Try to select a random object, and if it doesn't meet criteria, loop through all objects
        while not valid_content_found and l > 0:
            # Select a random object
            content = data['Place'][random.randrange(0, l)]

            # Check if the 'Ratings' key exists and if its value is valid
            if 'Ratings' in content:
                rating = content['Ratings']
                if rating == "New" or (rating.replace('.', '', 1).isdigit() and float(rating) >= 4.1):
                    # Ensure the selected object does not have a name already present in previous data
                    if 'name' in content and content['name'] not in names_in_previous_data:
                        valid_content_found = True
                        break  # Exit the loop once a valid entry is found

        # If a valid entry wasn't found in the first random attempt, loop through all entries
        if not valid_content_found:
            for content in data['Place']:
                if 'Ratings' in content:
                    rating = content['Ratings']
                    if rating == "New" or (rating.replace('.', '', 1).isdigit() and float(rating) >= 4.1):
                        # Ensure the selected object does not have a name already present in previous data
                        if 'name' in content and content['name'] not in names_in_previous_data:
                            valid_content_found = True
                            break

        # Add a key to identify the source file for each JSON object
        if valid_content_found:
            content["source"] = file_name

            # Write the content as a JSON line
            with open('DATA/filtered_data.jsonl', 'a') as f:
                json.dump(content, f)
                f.write('\n')

    time.sleep(3)

    # Read existing filtered data
    if os.path.exists('DATA/filtered_data.jsonl'):
        with open('DATA/filtered_data.jsonl', 'r') as f:
            lines = f.readlines()
    else:
        print("'DATA/filtered_data.jsonl' does not exist. Skipping data copying.")
        return

    # Write the copied data back (if you need to process or modify it)
    with open('DATA/previousdata.jsonl', 'w') as f:
        f.writelines(lines)

API_KEY = 'taZxEdYUepPb'
PROJECT_TOKEN = 'tew4uTgVf5TK'


def convert_jsonl_to_json():
    structured_data = {}
    
    with open('DATA/filtered_data.jsonl', 'r') as f:
        for line in f:
            # Parse each line as a JSON object
            data = json.loads(line)
            source = data.pop("source")
            
            # Append the data under the appropriate source key
            if source not in structured_data:
                structured_data[source] = []
            structured_data[source].append(data)
    
    # Save the structured data to process.json
    with open('DATA/process.json', 'w') as out_file:
        json.dump(structured_data, out_file, indent=2)

    return structured_data

def start_run_with_url(api_key, project_token, url):
    response = requests.post(f'https://www.parsehub.com/api/v2/projects/{project_token}/run', data={
        'api_key': api_key,
        'start_url': url
    })
    return response.json()

def get_run_status(api_key, run_token):
    response = requests.get(f'https://www.parsehub.com/api/v2/runs/{run_token}', params={
        'api_key': api_key
    })
    return response.json()

def get_run_results(api_key, run_token):
    response = requests.get(f'https://www.parsehub.com/api/v2/runs/{run_token}/data', params={
        'api_key': api_key
    })
    return response.json()

def process_and_append():
    # Convert JSONL to JSON structure
    structured_data = convert_jsonl_to_json()

    with open('DATA/filtered_data.jsonl', 'r') as f:
        for line in f:
            data = json.loads(line)
            url = data['url']
            source = data['source']
            
            # Start a ParseHub run for the URL
            run_response = start_run_with_url(API_KEY, PROJECT_TOKEN, url)
            run_token = run_response.get('run_token')
            if not run_token:
                print(f"Failed to start run for URL: {url}")
                continue
            
            # Poll for completion of the run
            while True:
                status = get_run_status(API_KEY, run_token)
                print(f"Run status for {url}: {status['status']}")
                if status['status'] == 'complete':
                    break
                time.sleep(10)  # Wait before checking again

            # Get and append results
            results = get_run_results(API_KEY, run_token)

            # Append the results to the appropriate source key
            if source in structured_data:
                structured_data[source].append(results)
            else:
                structured_data[source] = [results]

    # Save the updated data back to process.json
    with open('DATA/process.json', 'w') as out_file:
        json.dump(structured_data, out_file, indent=2)

# Execute the process
# sort()
# process_and_append()
