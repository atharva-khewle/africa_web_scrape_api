from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return 'Happy Birthday bro 🎉🎉🎉🎉🎉. go here -- >   https://web-scraping-app.vercel.app/api/scrape   it takes 30 sec too load. refresh if it doesnt work. '






@app.route('/api/scrape', methods=['GET'])
def scrape():
    url = 'https://en.sputniknews.africa/'  # Replace with the actual URL of the page you want to scrape

    # Set a timeout value (in seconds)
    timeout = 30
    articles = []

    try:
        # Send a GET request to the webpage with a timeout
        response = requests.get(url, timeout=timeout)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all anchor tags with the specific class
            anchor_tags = soup.find_all('a', class_='cell-main-photo__image')
            
            # Initialize a counter for numbering articles
            article_counter = 1

            for anchor_tag in anchor_tags:
                # Extract the href attribute (link)
                article_link = anchor_tag['href']

                # Construct the full URL (assuming the base URL is https://en.sputniknews.africa)
                base_url = 'https://en.sputniknews.africa'
                full_article_link = base_url + article_link

                # Find all image tags within the anchor tag
                img_tags = anchor_tag.find_all('img')

                # Extract the src attribute of each image tag
                image_links = [img_tag['src'] for img_tag in img_tags]

                # Find the parent div with the class 'cell-main-photo__info'
                info_div = anchor_tag.find_parent('div', class_='cell-main-photo__info')

                # Check if info_div is None before trying to find the title
                if info_div:
                    # Find the span with the class 'cell-main-photo__size' within the div
                    title_span = info_div.find('span', class_='cell-main-photo__size')
                    title_text = title_span.text if title_span else 'No Title Found'
                else:
                    title_text = 'No Title Found'

                # Append the extracted information to the articles list
                articles.append({
                    'article_number': article_counter,
                    'article_link': full_article_link,
                    'title': title_text,
                    'image_links': image_links
                })

                # Increment the counter
                article_counter += 1

            return jsonify({'status': 'success', 'articles': articles})
        else:
            return jsonify({'status': 'fail', 'message': f'Failed to retrieve the webpage. Status code: {response.status_code}'})
    except requests.exceptions.Timeout:
        return jsonify({'status': 'fail', 'message': f'Request timed out after {timeout} seconds.'})
    except requests.exceptions.RequestException as e:
        return jsonify({'status': 'fail', 'message': f'An error occurred while making the request: {e}'})






if __name__ == '__main__':
    app.run()
