import requests
from bs4 import BeautifulSoup


def download_page(url: str):
    page_raw = requests.get(url)
    return BeautifulSoup(page_raw.text, parser='lxml')


url = 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/3128452'
raw_content = requests.get(url)
raw_data = json.loads(raw_content.text)

raw_data.keys()

parser = download_page(url)

tmp = parser.findAll('span', {'class': 'dib'})

label_list = []
content_list = []
for i in tmp:
    if 'Bio' in str(i):
        label_list.append(i)
    else:
        content_list.append(i)


for j in range(len(content_list)):
    print(label_list[j].text, '\t', content_list[j].text)