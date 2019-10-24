import pandas as pd
import chart

df = pd.read_csv('data/candy.csv')

# users = df['user'].value_counts()[df['user'].value_counts() >= 5].index
# df = df[df['user'].isin(users)]

df['product'] = df['product'].apply(lambda x: x.replace('/reviews/', ''))
df['product'] = df['product'].apply(lambda x: x.replace('-', ' '))

products = df.sort_values('product')['product'].drop_duplicates()

pd.DataFrame(products).to_dict('list')

from bs4 import BeautifulSoup
dir(BeautifulSoup())

len(find)

find = [
'find',
 'findAll',
 'findAllNext',
 'findAllPrevious',
 'findChild',
 'findChildren',
 'findNext',
 'findNextSibling',
 'findNextSiblings',
 'findParent',
 'findParents',
 'findPrevious',
 'findPreviousSibling',
 'findPreviousSiblings',
 'find_all',
 'find_all_next',
 'find_all_previous',
 'find_next',
 'find_next_sibling',
 'find_next_siblings',
 'find_parent',
 'find_parents',
 'find_previous',
 'find_previous_sibling',
 'find_previous_siblings'
 ]
#
