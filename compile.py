import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

now = datetime.now()

day = str(now.day)
month = str(now.strftime("%B"))
year = str(now.year)
date = f"{day} {month}, {year}"
filename = 'TEXT/articleNum.txt'

def articleNum():
    try:
        with open(filename, 'r') as file:
            number_str = file.read().strip()
        
        number = int(number_str)
        number += 1
        new_number_str = str(number).zfill(3)
        
        with open(filename, 'w') as file:
            file.write(new_number_str)
        
        return new_number_str
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
        return '000'  # Default to 001 if the file does not exist
    except ValueError:
        print("The file does not contain a valid integer.")
        return '000'  # Default to 001 if the content is invalid

def combineANDsave():
    with open('DATA/process.json', 'r') as f:
        data = json.load(f)

    def extract_first_item(data_list):
        return data_list[0] if data_list else {}

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('HTML/emailTemplate.html')

    cafe_data = extract_first_item(data.get('cafe', []))
    date_data = extract_first_item(data.get('date', []))
    trending_data = extract_first_item(data.get('trending', []))
    featured_data = extract_first_item(data.get('featured', []))
    microbrewery_data = extract_first_item(data.get('microbrewery', []))
    newly_opened_data = extract_first_item(data.get('newlyOpened', []))
    pubandbar_data = extract_first_item(data.get('pubandbar', []))

    html_content = template.render(
        article_issue=articleNum(),
        article_date=date,

        featured_image_url=featured_data.get('feature_image'),
        featured_name=featured_data.get('name'),
        featured_content=featured_data.get('description'),
        featured_link=featured_data.get('url'),
        featured_rating=featured_data.get('Ratings'),
        featured_grid_image_1=featured_data.get('images', [])[0] if len(featured_data.get('images', [])) > 0 else '',
        featured_grid_image_2=featured_data.get('images', [])[1] if len(featured_data.get('images', [])) > 1 else '',
        featured_grid_image_3=featured_data.get('images', [])[2] if len(featured_data.get('images', [])) > 2 else '',
        featured_grid_image_4=featured_data.get('images', [])[3] if len(featured_data.get('images', [])) > 3 else '',

        trending_image_url=trending_data.get('feature_image'),
        trending_name=trending_data.get('name'),
        trending_content=trending_data.get('description'),
        trending_link=trending_data.get('url'),
        trending_rating=trending_data.get('Ratings'),

        new_in_town_image_url=newly_opened_data.get('feature_image'),
        new_in_town_name=newly_opened_data.get('name'),
        new_in_town_content=newly_opened_data.get('description'),
        new_in_town_link=newly_opened_data.get('url'),
        new_in_town_rating=newly_opened_data.get('Ratings'),

        date_image_url=date_data.get('feature_image'),
        date_name=date_data.get('name'),
        date_content=date_data.get('description'),
        date_link=date_data.get('url'),
        date_rating=date_data.get('Ratings'),

        events_image_url=microbrewery_data.get('feature_image'),
        brew_name=microbrewery_data.get('name'),
        brew_content=microbrewery_data.get('description'),
        events_link=microbrewery_data.get('url'),
        brew_rating=microbrewery_data.get('Ratings'),

        cafe_image_url=cafe_data.get('feature_image'),
        cafe_name=cafe_data.get('name'),
        cafe_content=cafe_data.get('description'),
        cafe_link=cafe_data.get('url'),
        cafe_rating=cafe_data.get('Ratings'),

        pubandbar_image_url=pubandbar_data.get('feature_image'),
        pubandbar_name=pubandbar_data.get('name'),
        pubandbar_content=pubandbar_data.get('description'),
        pubandbar_link=pubandbar_data.get('url'),
        pubandbar_rating=pubandbar_data.get('Ratings')
    )

    with open('HTML/output.html', 'w') as f:
        f.write(html_content)

    print("HTML file generated successfully.")



