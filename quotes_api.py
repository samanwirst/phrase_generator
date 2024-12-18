import requests
from config import QUOTES_API_KEY
import random

category_list = ['attitude', 'change', 'courage', 'dreams', 'education', 'experience', 'failure', 'faith', 'famous', 'freedom', 'future', 'great', 'happiness', 'history', 'hope', 'inspirational', 'intelligence', 'knowledge', 'leadership', 'learning', 'life', 'success']

class QuotesAPI:
    def get_random_quote():
        api_url = 'https://api.api-ninjas.com/v1/quotes'.format(random.choice(category_list))
        response = requests.get(api_url, headers={'X-Api-Key': QUOTES_API_KEY})

        if response.status_code == requests.codes.ok:
            response_content = response.json()[0]
            quote_text = response_content['quote']
            quote_author = response_content['author']
            return quote_text, quote_author
        else:
            return response.status_code
