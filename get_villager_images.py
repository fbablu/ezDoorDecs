import requests
from bs4 import BeautifulSoup
import json


url = 'https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


table = soup.find('table', {'class': 'sortable'})

image_urls = []
for img_tag in table.find_all('img'):
    img_url = img_tag.get('data-src', None)  # Look for 'data-src' first
    if not img_url:                          # Now look for 'src'
        img_url = img_tag.get('src')
        
    if img_url and img_url.startswith('https://'):
        img_url = img_url.replace('scale-to-width-down/100', 'scale-to-width-down/500')
        image_urls.append(img_url)

# Image URLs list to a JSON format
image_urls_json = json.dumps(image_urls, indent=4)

print(image_urls_json)
with open('villager_image_urls.json', 'w') as json_file:
    json_file.write(image_urls_json)
