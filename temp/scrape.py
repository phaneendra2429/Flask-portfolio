import requests
from bs4 import BeautifulSoup
import json

# URL of the LinkedIn Recommendations page
url = 'https://www.linkedin.com/in/phaneendra-g/details/recommendations/'

# Path to the JSON file
json_file_path = 'recommendations.json'

# Scraping function
def scrape_recommendations():
    # Send a GET request to fetch the LinkedIn page (you may need to handle login)
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    recommendations = []

    # Find and extract the relevant data (assuming you have the page structure)
    recommendation_cards = soup.find_all('li', class_='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column')  # Modify this selector based on the actual HTML

    for card in recommendation_cards:
        name = card.find('h5').text
        title = card.find('h6').text
        recommendation_text = card.find('p', class_='recommendation-text').text
        date = card.find('small').text
        image_url = card.find('img')['src']

        recommendation = {
            "name": name,
            "title": title,
            "recommendation": recommendation_text,
            "date": date,
            "image": image_url
        }

        recommendations.append(recommendation)

    # Save the scraped data to JSON file
    with open(json_file_path, 'w') as f:
        json.dump(recommendations, f, indent=4)

    print(f"Saved {len(recommendations)} recommendations to {json_file_path}")

if __name__ == '__main__':
    scrape_recommendations()
