import lxml.html
import requests
import yaml

WIKI_ELEMENTS_URL = 'https://en.wikipedia.org/wiki/List_of_elements'
TABLE_ELEMENTS = 118

body = requests.get(WIKI_ELEMENTS_URL).text
root = lxml.html.fromstring(body)

elements = []

for i in range(3, TABLE_ELEMENTS + 3):
    row = list(root.xpath('//*[@id="mw-content-text"]/table[1]/tr')[i].iterfind('td'))
    elements.append({
        'num': int(row[0].text_content()),
        'sym': str(row[1].text_content()),
        'name': str(row[2].text_content())
    })

with open('data/en/elements.yml', 'w') as elements_file:
    elements_file.write(yaml.dump(elements))
