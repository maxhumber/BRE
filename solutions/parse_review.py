def parse_review(review):
    stars = len(review.find('div', {'class': 'productComponents__SingleStar-sc-1ffpes9-3 kzXpnS'}))
    user = (review.find('div',
        {'class': 'layoutComponents__Row-l2otzz-2 MSbai layoutComponents__Block-l2otzz-0 ixyxcj'}
        ).find('a').attrs['href'])[1:]
    return {'user': user, 'stars': stars}
