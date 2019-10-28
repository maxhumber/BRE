import time
import json
import random
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from gazpacho import Soup
from tqdm import tqdm
import pandas as pd

options = Options()
options.headless = True
browser = Firefox(options=options)

def make_soup(url):
    browser.get(url)
    html = browser.page_source
    soup = Soup(html)
    return soup

def build_review_url(product, page):
    base = 'https://www.influenster.com'
    url = f'{base}/{product}?review_sort=most+recent&review_page={page}'
    return url

def parse_review(product, review):
    stars = int(review.find('div', {'class': 'avg-stars'}).attrs['data-stars'])
    user = review.find('div', {'class': 'content-item-author-info'}).find('a').attrs['href'][1:]
    return {'product': product, 'user': user, 'stars': stars}

def scrape_product_page(product, page):
    url = build_review_url(product, page)
    soup = make_soup(url)
    page_reviews = soup.find('div', {'class': 'content-item review-item'})
    return [parse_review(product, r) for r in page_reviews]

def scrape_product(product):
    url = build_review_url(product, 1)
    soup = make_soup(url)
    pages = int(
        soup.find('div', {'class': 'product-highlights-results'})
        .text
        .replace(',', '')
        .split(' ')[0]
    ) // 10 + 1
    pages = min(pages, 100)
    pages = list(range(1, pages+1))
    random.shuffle(pages)
    reviews = []
    for page in pages:
        print(f'scraping page: {page}')
        page_reviews = scrape_product_page(product, page)
        reviews.extend(page_reviews)
        time.sleep(random.randint(1, 10) / 10)
    return reviews

def scrape_index(category='sweets-candy-gum'):
    product_index = []
    for page in tqdm(range(1, 10+1)):
        url = f'https://www.influenster.com/reviews/{category}?page={page}'
        soup = make_soup(url)
        products = soup.find('a', {'class': 'category-product'}, strict=True)
        products = [p.attrs['href'] for p in products]
        candy.extend(products)
        time.sleep(random.randint(1, 10) / 10)
    return product_index

if __name__ == '__main__':

    product_index = scrape_index(category='sweets-candy-gum')

    product_reviews = []
    for product in tqdm(product_index):
        print(f'scraping: {product}')
        try:
            reviews = scrape_product(product)
            product_reviews.extend(reviews)
        except:
            pass
        time.sleep(random.randint(1, 10) / 10)

    df = pd.DataFrame(product_reviews)
    # df.to_csv('candy.csv', index=False)
