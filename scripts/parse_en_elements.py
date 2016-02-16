import lxml.html
import requests
import yaml

WIKI_ELEMENTS_URL = 'https://en.wikipedia.org/wiki/List_of_elements'
TABLE_ELEMENTS = 118

body = requests.get(WIKI_ELEMENTS_URL).text
root = lxml.html.fromstring(body)

elements = []

for i in range(3, TABLE_ELEMENTS + 3):
    row = root.xpath('//*[@id="mw-content-text"]/table[1]/tr')[i]
    columns = list(row.iterfind('td'))
    links = list(row.iterlinks())
    if columns[6].findall('span'):
        atomic_weight = str(columns[6].xpath('span[2]')[0].text_content())
    else:
        atomic_weight = str(columns[6].text_content())
    element_link = 'https://en.wikipedia.org{}'.format(links[0][2])
    elements.append({
        'num': int(columns[0].text_content()),
        'sym': str(columns[1].text_content()),
        'name': str(columns[2].text_content()),
        'group': str(columns[4].text_content()),
        'period': str(columns[5].text_content()),
        'atomic_weight': atomic_weight,
        'density': str(columns[7].text_content()) + ' g/cm^3',
        'source': element_link
    })

with open('data/en/elements.yml', 'w') as elements_file:
    elements_file.write(yaml.dump(elements))
