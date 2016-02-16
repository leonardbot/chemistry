import lxml.html
import requests
import yaml

WIKI_CHEMICALS_URL = 'https://en.wikipedia.org/wiki/List_of_commonly_available_chemicals'

body = requests.get(WIKI_CHEMICALS_URL).text
root = lxml.html.fromstring(body)

chemicals = []

for table in root.xpath('//*[@id="mw-content-text"]/table')[1:-1]:
    for row in table.findall('tr')[1:]:
        columns = list(row.iterfind('td'))
        common_name = str(columns[2].text_content())
        if common_name == '—':
            common_names = []
        else:
            common_names = common_name.split(', ')
        chemicals.append({
            'name': str(columns[0].text_content()),
            'formula': str(columns[1].text_content()),
            'common_name': common_names
        })

with open('data/en/chemicals.yml', 'w') as chemicals_file:
    chemicals_file.write(yaml.dump(chemicals))
