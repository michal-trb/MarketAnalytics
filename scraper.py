from bs4 import BeautifulSoup
import requests as req
import csv
import time

url = ''  # wprowadź adres popularnego serwisu ogłoszeniowego

for i in range(1, 10):
    page = req.get(url+str(i))
    filename = 'strona' + str(i) + '.csv'

    soup = BeautifulSoup(page.content, 'html.parser')

    lists = soup.find_all('div', class_='listing__teaserWrapper')
    with open(filename, 'w', encoding='utf8', newline='') as f:

        thewriter = csv.writer(f)
        header = ['Title', 'Location', 'Price', 'Area']
        thewriter.writerow(header)

        for element in lists:
            title = element.find('h2', class_='teaserUnified__title').text.replace('\n', '')
            location = element.find('span', class_='teaserUnified__location').text.replace('\n', '')
            price = element.find('p', class_='teaserUnified__price').text.replace('\n', '')
            area = element.find('li', class_='teaserUnified__listItem').text.replace('\n', '')
            info = [title, location, price, area]
            thewriter.writerow(info)

        time.sleep(3)
