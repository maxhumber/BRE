from gazpacho import Soup
import pandas as pd

# index

with open('influenster/index.html', 'r') as f:
    html = f.read()

soup = Soup(html)
products = soup.find('a', {'class': 'category-product'})
products = [p.attrs['href'] for p in products]

# skittles

with open('influenster/skittles.html', 'r') as f:
    html = f.read()

soup = Soup(html)
reviews = (soup
    .find('div', {'class': 'layoutComponents__Block-l2otzz-0 efHRYv'}, strict=True)
    .find('div', {'class': 'item wrappers__Wrapper-sc-1mex847-0 jEYnle'})
)

def parse_review(review):
    stars = len(review.find('div', {'class': 'productComponents__SingleStar-sc-1ffpes9-3 kzXpnS'}))
    user = (review.find('div',
        {'class': 'layoutComponents__Row-l2otzz-2 MSbai layoutComponents__Block-l2otzz-0 ixyxcj'}
        ).find('a').attrs['href'])[1:]
    return {'user': user, 'stars': stars}

review = reviews[0]
parse_review(review)
[parse_review(r) for r in reviews]
