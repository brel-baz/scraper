import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3
import datetime
import re

URL = "https://www.businesswire.com/portal/site/home/news/"
date = datetime.datetime.now()

def get_html(siteName):

   r = requests.get(siteName)
   data = r.text
   scrap = BeautifulSoup(data, 'lxml')
   return scrap

scrap = get_html(URL)
driver = webdriver.Firefox(executable_path='/Users/brel-baz/Downloads/geckodriver')
last = scrap.find('div', attrs={'class' : 'pagingLinks'}).text
tab = last.split("\t")
last = int(tab[-1])
i = 1

connexion = sqlite3.connect("database")
cursor = connexion.cursor()
cursor.execute("CREATE TABLE business_wire (title TEXT, time_extraction TEXT, time_new TEXT, new TEXT, company_name TEXT, hashtag TEXT, cashtag TEXT, contact TEXT, url TEXT)")
while i <= last:
    page = str(i)
    URL = "https://www.businesswire.com/portal/site/home/template.PAGE/news/?javax.portlet.tpst=ccf123a93466ea4c882a06a9149550fd&javax.portlet.prp_ccf123a93466ea4c882a06a9149550fd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_ccf123a93466ea4c882a06a9149550fd_ndmHsc=v2*A1520168400000*B1522777315761*DgroupByDate*G" + page + "*N1000003&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken"
    scrap = get_html(URL)
    for link in scrap.find_all('div', attrs={'itemscope' : 'itemscope'}):

        url = link.get('itemid')
        html = get_html(url)
        driver.get(url)

        if html.find('ul', attrs={'class': 'hash-tags'}) != None:
            hashtag = html.find('ul', attrs={'class': 'hash-tags'}).text
        else:
            hashtag = "NEANT"
        if html.find('ul', attrs={'class': 'cash-tags'}) != None:
            cashtag = html.find('ul', attrs={'class': 'cash-tags'}).text
        else:
            cashtag = "NEANT"
        elems = {
            'titre': html.find('h1', attrs={'class' : "epi-fontLg"}).text,
            'time': html.find('time', attrs={'itemprop':'dateModified'}).text,
            'news': html.find('div', attrs={'itemprop':'articleBody'}).text,
            'company_name': driver.find_element_by_xpath('//*[@id="companyInformation"]').text,
            'hashtag': hashtag,
            'cashtag': cashtag,
            'contact': html.find('div', attrs={'class': 'bw-release-contact'}).text,
            'url': url,
            'extraction': str(date)
        }
        cursor.execute('INSERT INTO business_wire(title,time_extraction,time_new,new,company_name,hashtag,cashtag,contact,url) VALUES(?,?,?,?,?,?,?,?,?)', (elems['titre'],elems['extraction'],elems['time'],elems['news'],elems['company_name'],elems['hashtag'],elems['cashtag'],elems['contact'],elems['url']))
    i+= 1
connexion.commit()
driver.close()
