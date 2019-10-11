from gazpacho import get, Soup

url = 'https://github.com/maxhumber/gazpacho/stargazers'

html = get(url)
soup = Soup(html)

def get_next_url(soup):
    buttons = soup.find('div', mode='all', attrs={'class': 'BtnGroup', 'data-test-selector': "pagination"})
    button = buttons[-1].find('a', mode='all')[-1]
    if button.text == 'Next':
        return button.attrs['href']
    return None

get_next_url(soup)

def scrape_users(soup):
    users = soup.find('div', {'class': 'follower-list-align-top d-inline-block ml-3'})
    users = [u.find('a', {'data-hovercard-type': 'user'}) for u in users]
    users = [u.attrs['href'][1:] for u in users]
    return users

scrape_users(soup)



#
