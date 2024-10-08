from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
import json
import time
import re

# Path to your JSON file and Chromedriver
json_file_path = 'DATA/process.json'  # Update this path
chromedriver_path = '/usr/local/bin/chromedriver'  # Update this path if necessary

def scroll_slowly(driver, scroll_pause_time=2, scroll_increment=300):
    """Scrolls the page slowly up and down to load all images."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(scroll_pause_time)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(f"window.scrollBy(0, -{scroll_increment});")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def clean_url(url):
    """Remove query parameters and add /photos to the URL."""
    if url:
        base_url = re.sub(r'\?zrp_bid=\d+&zrp_pid=\d+', '', url)
        return base_url + '/photos'
    return url

def clean_image_url(url):
    """Remove everything after the question mark in the URL."""
    if url:
        return url.split('?')[0]
    return url

def get_image_sources(driver, url):
    driver.get(url)
    scroll_slowly(driver)

    wait = WebDriverWait(driver, 60)
    driver.save_screenshot('screenshot.png')  # For debugging

    try:
        img_elements = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'img.sc-s1isp7-5.eisbVA')))
        return [clean_image_url(img_element.get_attribute('src')) for img_element in img_elements]
    except Exception as e:
        print(f"Error finding images: {e}")
        return []

def get_feature_image(driver, url):
    driver.get(url)
    
    wait = WebDriverWait(driver, 40)
    
    try:
        feature_img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.sc-s1isp7-5.eQUAyn')))
        return clean_image_url(feature_img_element.get_attribute('src'))
    except Exception as e:
        print(f"Error finding feature image: {e}")
        return ""

def getImage():
    # Start a virtual display
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        for key in data:
            for item in data[key]:
                if 'url' in item:
                    url = clean_url(item['url'])
                    print(f"Processing URL: {url}")

                    image_sources = get_image_sources(driver, url)
                    feature_image = get_feature_image(driver, url)
                    
                    if 'images' not in item:
                        item['images'] = []
                    item['images'].extend(image_sources)
                    item['feature_image'] = feature_image

        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print('Images and feature image have been updated')

    finally:
        driver.quit()


