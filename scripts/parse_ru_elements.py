import lxml.html
import requests
import yaml

WIKI_ELEMENTS_URL = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%85%D0%B8%D0%BC%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85_%D1%8D%D0%BB%D0%B5%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2'
TABLE_ELEMENTS = 118

body = requests.get(WIKI_ELEMENTS_URL).text
root = lxml.html.fromstring(body)

elements = []

for i in range(1, TABLE_ELEMENTS + 1):
    row = root.xpath('//*[@id="mw-content-text"]/table[2]/tr')[i]
    columns = list(row.iterfind('td'))
    links = list(row.iterlinks())

    atomic_weight = str(columns[5].text)

    period = str(columns[4].text_content()).split(', ')[0]
    group = ''
    if len(str(columns[4].text_content()).split(', ')) == 2:
        group = str(columns[4].text_content()).split(', ')[1]

    element_link = 'https://ru.wikipedia.org{}'.format(links[0][2])
    elements.append({
        'num': int(columns[0].text_content()),
        'name': str(columns[1].text_content()),
        'sym': str(columns[2].text_content()),
        'english_name': str(columns[3].text_content()).split(', ')[0],
        'period': period,
        'group': group,
        'atomic_weight': atomic_weight,
        'density': str(columns[6].text_content()) + ' г/см^3',
        'source': element_link
    })

with open('data/ru/elements.yml', 'w') as elements_file:
    elements_file.write(yaml.dump(elements))
