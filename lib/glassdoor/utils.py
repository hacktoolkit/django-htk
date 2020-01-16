# Python Standard Library Imports
import json
import time

# Third Party / PIP Imports
import requests
from bs4 import BeautifulSoup


GLASSDOOR_API_URL = 'http://api.glassdoor.com/api/api.htm'

def get_company_info(company_name, partner_id, partner_key):
    """Gets company info from Glassdoor API
    http://www.glassdoor.com/api/index.htm
    """
    params = {
        'v' : 1,
        'format' : 'json',
        't.p' : partner_id,
        't.k' : partner_key,
        'userip' : '0.0.0.0',
        'useragent' : 'Mozilla/4.0',
        'action' : 'employers',
        'q' : company_name,
    }
    headers = {
        'User-Agent': 'Mozilla/4.0',
        'From': 'hello@hacktoolkit.com'  # This is another valid field
    }

    response = requests.get(GLASSDOOR_API_URL, headers=headers, params=params)
    data = json.loads(response.content)

    company = data['response']['employers'][0]

    return company

def scrape_company_reviews(review_url_base, num_reviews=None):
    import math
    review_url_ext = '.htm'
    review_url = review_url_base + review_url_ext
    review_urls = [review_url,]
    if num_reviews:
        reviews_per_page = 10
        num_pages = int(math.ceil(num_reviews / float(reviews_per_page)))
        for i in range(1, num_pages + 1):
            review_url = '%s_P%d%s' % (review_url_base, i, review_url_ext,)
            review_urls.append(review_url)

    headers = {
        'User-Agent': 'Mozilla/%2F4.0',
        'From': 'hello@hacktoolkit.com'  # This is another valid field
    }
    params = {
        'filter.defaultEmploymentStatuses' : 'false',
    }

    def format_review(list_item):
        title = list_item.find_all('span', class_='summary')[0].get_text()
        pros = list_item.find_all('p', class_='pros')[0].get_text()
        cons = list_item.find_all('p', class_='cons')[0].get_text()
        advice = list_item.find_all('p', class_='adviceMgmt')
        if len(advice) == 0:
            advice = ''
        else:
            advice = advice[0].get_text()
        review = {
            'title' : title,
            'pros' : pros,
            'cons' : cons,
            'advice' : advice,
        }
        return review

    all_reviews = []
    for review_url in review_urls:
        response = requests.get(review_url, headers=headers, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')

        #num_reviews = int(soup.select('.empLinks .reviews .num').get_text())
        list_items = soup.find_all('li', class_='empReview')
        reviews = map(format_review, list_items)
        all_reviews += reviews
        time.sleep(1)
    return all_reviews
