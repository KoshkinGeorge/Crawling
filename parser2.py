import requests
from bs4 import BeautifulSoup as bs
import json
import csv


headers = {
     'Accept': '*/*',
     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}
url = 'https://health-diet.ru/table_calorie/'
page = requests.get(url, headers)
# with open('C:\PythonProjects\parsing_beginning\index.html', 'w', encoding='utf-8') as f:
#     f.write(page.text)

soup = bs(page.content, 'lxml')
links = dict()
for i in soup.select('a.mzr-tc-group-item-href'):
    links[i.text] = 'https://health-diet.ru' + i.get('href')
[print(key, '   --->    ', value, '\n') for key, value in links.items()]
# with open('all_links.json', 'w') as f:
#     json.dump(links, f, indent=4, ensure_ascii=False)
temp_links = dict()
for line in links.keys():
    rep = ['`', "'", ',', ' ', '-']
    temp = line
    for item in rep:
        if item in temp:
            temp = temp.replace(item, '_')
    temp_links[temp] = links[line]
links = temp_links
counter = 0
parameters = []
pages = len(links.keys()) - 1
for name, page in links.items():
    page_code = requests.get(page, headers).content
    with open(rf'C:\PythonProjects\parsing_beginning\scrap_tutorial-master\data\pg_{name}.html', 'wb') as f:
        f.write(page_code)
    cur_soup = bs(page_code, 'lxml')
    if cur_soup.select_one('.uk-alert.uk-alert-danger.uk-h1.uk-text-center.mzr-block.mzr-grid-3-column-margin-top'):
        break
    for el in cur_soup.select('.uk-table tbody tr'):
        row = el.select('td')
        parameters.append(dict(zip(['Title', 'Callories', 'Proteins', 'Fats', 'Carbonates'], [row[0].text, row[1].text, row[2].text, row[3].text, row[4].text])))
        with open(rf'C:\PythonProjects\parsing_beginning\scrap_tutorial-master\data\{name}.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='=')
            writer.writerow([row[0].text, row[1].text, row[2].text, row[3].text, row[4].text])
    counter += 1
    if counter == pages:
        break

with open(r'C:\PythonProjects\parsing_beginning\scrap_tutorial-master\data\parameters.json', 'w') as f:
    json.dump(parameters, f, indent=4, ensure_ascii=False)
print('Обработано страниц: ', counter)