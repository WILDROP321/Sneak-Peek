import requests
import json
import time

# Replace with your ParseHub API key and project token
API_KEY = 'taZxEdYUepPb'
PROJECT_TOKEN = 'tbDzHQyCjAGz'

# Start a new run with a specific URL
def start_run(api_key, project_token, url):
    response = requests.post(f'https://www.parsehub.com/api/v2/projects/{project_token}/run', data={
        'api_key': api_key,
        'start_url': url
    })
    return response.json()

# Get the status of a run
def get_run_status(api_key, run_token):
    response = requests.get(f'https://www.parsehub.com/api/v2/runs/{run_token}', params={
        'api_key': api_key
    })
    return response.json()

# Get the results of a run
def get_run_results(api_key, run_token):
    response = requests.get(f'https://www.parsehub.com/api/v2/runs/{run_token}/data', params={
        'api_key': api_key
    })
    return response.json()

# Save JSON response to a file
def save_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

# Example usage
def scrapeData():
    urls = [
        'https://www.zomato.com/bangalore/trending-this-week',  # URL for trending
        'https://www.zomato.com/bangalore/rooftop',  # URL for featured
        'https://www.zomato.com/bangalore/newly-opened',  # URL for newly opened
        'https://www.zomato.com/bangalore/romantic-restaurants',  # URL for date
        'https://www.zomato.com/bangalore/best-bars-and-pubs',  # URL for pub and bar
        'https://www.zomato.com/bangalore/picturesque-cafes-insta-worthy', #cafe
        'https://www.zomato.com/bangalore/microbreweries', #microbrewery
        'https://www.zomato.com/bangalore/rooftop' #rooftop
    ]

    filenames = [
        'trending.json',
        'featured.json',
        'newlyOpened.json',
        'date.json',
        'pubandbar.json',
        'cafe.json',
        'microbrewery.json',
        'rooftop.json'
    ]

    for url, filename in zip(urls, filenames):
        print(f"Processing URL: {url}")
        
        # Start a run with the URL
        run_response = start_run(API_KEY, PROJECT_TOKEN, url)
        run_token = run_response['run_token']
        print("Started run:", run_token)

        # Poll for completion
        while True:
            status = get_run_status(API_KEY, run_token)
            print("Run status:", status['status'])
            if status['status'] == 'complete':
                break
            time.sleep(10)  # Wait before checking again

        # Get results
        results = get_run_results(API_KEY, run_token)
        #print("Results:", json.dumps(results, indent=2))

        # Save results to a file
        save_json_to_file(results, 'DATA/'+ filename)
        print(f"Results saved to {filename}")

#scrapeData()