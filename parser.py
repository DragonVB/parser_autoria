import requests
from bs4 import BeautifulSoup
import csv
import os

URL = input('Input URL: ')
URL=URL.strip()
HEADERS = {'user-agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36', 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://auto.ria.com/uk'
FILE = 'cars.csv'

def get_html(url,params=None):
    r=requests.get(url=URL,headers=HEADERS,params=params)
    return r

def get_pages_count(html):
    soup=BeautifulSoup(html,'html.parser')
    pagination=soup.find_all('span',class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1    
    


def get_content(html):
    soup=BeautifulSoup(html,'html.parser')
    items=soup.find_all('div', class_='proposition_area')
    cars=[]
    for item in items:
        uah_price=item.find('span',class_='grey size13')

        
            
        if uah_price:
            uah_price=uah_price.get_text()
        else:
            uah_price='Not Specified'
            

        cars.append({
            'title': item.find('strong').get_text('strong'),
            'link': HOST + item.find('a').get('href'),
            'usd_price': item.find('div',class_='proposition_price').get_text(strip=True).replace(uah_price,'').replace('•',''),
            'uah_price': uah_price,
            'city': item.find('div', class_='proposition_region').get_text(strip=True)
                   
        })
    
    return cars
   
def save_file(items,path):
    with open(path,'w',newline='') as file:
        writer=csv.writer(file, delimiter=';')
        writer.writerow(['Mark','Link','USD Price','UAH Price', 'City'])
        for item in items:
            writer.writerow([item['title'],item['link'],item['usd_price'],item['uah_price'], item['city']])


def parse():
    html=get_html(URL)
    if html.status_code == 200:
        cars=[]
        pages_count=get_pages_count(html.text)
        for page in range(1,pages_count+1):
            print(f'Parsing page {page} in {pages_count}')
            html=get_html(URL,params={'page':page})
            cars.extend((get_content(html.text)))
        print(f'Cars finded {len(cars)-1}')
        save_file(cars,FILE)
        os.startfile(FILE)
    else:
        print("Error")    
parse()    
