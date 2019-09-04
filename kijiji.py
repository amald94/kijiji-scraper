import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re

url = 'https://www.kijiji.ca/b-for-rent/ontario'
baseurl = 'https://www.kijiji.ca'
baseForOntario = '/c30349001l9004'
pageNos = '/page-'
adurl = []
listing = []

def getUrls():

    for i in range(2):
        url_final = url+pageNos+str(i)+baseForOntario
        response = requests.get(url_final)
        soup = BeautifulSoup(response.text, "html.parser")
        advtTitles = soup.findAll('div', attrs={'class' : 'title'})
        try:
            for link in advtTitles:
                adlink = baseurl+link.find('a')['href']
                adurl.append(adlink)
        except(Exception):
            print(Exception)
    
    print(len(adurl))

    getDetails(adurl)

def getDetails(urls):

    for url in urls:
        listDetails = ""
        #url = 'https://www.kijiji.ca/v-room-rental-roommate/oakville-halton-region/renting-a-private-furnished-room-very-clean-very-quiet-house/1456771236?enableSearchNavigationFlag=true'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.select_one("h1[class*=title-2323565163]").text
        #print(title)
        price = soup.select_one("span[class*=currentPrice-2842943473]").text
        #print(price)

        description = soup.find_all('div', attrs={'class' : 'descriptionContainer-3544745383'})
        #print(description)

        location = soup.find('span', attrs={'class' : 'address-3617944557'})
        #print(location)

        date = soup.find('time').text   
        #print(date)
        listFt = str(title) + "||" + str(price) + "||" + str(description) + "||" + str(location) + "||" + str(date) 

        features = soup.find_all('dl', attrs={'class' : 'itemAttribute-983037059'})
        for ft in features:
            dt = ft.find('dt').text
            #print(dt)
            dd = ft.find('dd').text
            #print(dd)

            listDetails = listFt + "||" + str(dt) + ":" + str(dd)
        
        saveToDisk(listDetails)

        
def saveToDisk(advt):

    adft = advt.split("||")
    print(len(adft))
    


getUrls()