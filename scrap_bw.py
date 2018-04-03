import requests
from bs4 import BeautifulSoup
import sqlite3
import re

URL = "https://www.businesswire.com/portal/site/home/news/"


def get_html(siteName):
   """
   Renvoie le contenu html d'une page dont l'url a ete passe en parametre.
   """
   # print("pp")
   r = requests.get(siteName)
   # print(r, type(r))
   # print(dir(r))
   # print(r.url)
   # print(r.request)
   data = r.text
   # print(data[0:10], type(data))
   scrap = BeautifulSoup(data, 'lxml')
   # print(type(scrap))
   # print(dir(scrap))
   return scrap

scrap = get_html(URL)
for link in scrap.find_all('div', attrs={'itemscope' : 'itemscope'}):
    url = link.get('itemid')
    html = get_html(url)
    elems = {
        'titre': html.find('h1', attrs={'class' : "epi-fontLg"}).text,
        'time': html.find('time', attrs={'itemprop':'dateModified'}).text,
        'news': html.find('div', attrs={'itemprop':'articleBody'}).text,
        # 'company_name': html.find('span', attrs={'itemprop': 'sourceOrganization'})
    }
    # a = html.find('h3', attrs={'itemprop': 'sourceOrganization'})
    a = html.findAll('h3')
    # if a is not None:
    #     print(a)
    # a.find('span').text
    print(a)
    # print(dir(a))
    # print(elems['news'])
    # print(elems['company_name'])

    break
    # print(a.text)
    # print(b.text)
    # break