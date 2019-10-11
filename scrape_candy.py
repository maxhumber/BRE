from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from gazpacho import Soup

options = Options()
options.headless = True
browser = Firefox(options=options)

def build_review_url(product, page):
    base = 'https://www.influenster.com/reviews'
    url = f'{base}/{product}?review_sort=most+recent&review_page={page}'
    return url

product = 'reeses-peanut-butter-cups-miniatures-76'
url = build_review_url(product, 1)

browser.get(url)
html = browser.page_source
soup = Soup(html)

reviews = soup.find('div', {'class': 'content-item review-item'})

def parse_review(review):
    stars = int(review.find('div', {'class': 'avg-stars'}).attrs['data-stars'])
    user = review.find('a', {'rel': 'nofollow'}).attrs['href'][1:]
    return user, stars

[parse_review(r) for r in reviews]

### scrape products

page = 1
url = f'https://www.influenster.com/reviews/sweets-candy-gum?page={page}'

browser.get(url)
html = browser.page_source
soup = Soup(html)

products = soup.find('a', {'class': 'category-product'}, strict=True)
products = [p.attrs['href'] for p in products]
len(products)
