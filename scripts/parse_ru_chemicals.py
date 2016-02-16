import lxml.html
import requests
import yaml

WIKI_CHEMICALS_URL = 'http://dic.academic.ru/dic.nsf/ruwiki/139424'

body = requests.get(WIKI_CHEMICALS_URL).text
root = lxml.html.fromstring(body)

chemicals = []

for table in root.xpath('//*[@id="mw-content-text"]/table')[1:-1]:
    for row in table.findall('tr')[1:]:
        columns = list(row.iterfind('td'))
        names = columns[1].text_content().split('\n')
        common_names = []
        chemicals.append({
            'name': names[0],
            'common_names': names[1:],
            'formula': str(columns[0].text_content()),
        })

with open('data/ru/chemicals.yml', 'w') as chemicals_file:
    chemicals_file.write(yaml.dump(chemicals))
