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

def getUrls():

    for i in range(5):
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

def getDetails():
    url = 'https://www.kijiji.ca/v-room-rental-roommate/mississauga-peel-region/female-only-room-for-rent-w-private-bath-bramalea-city-centre/1457114159'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.select_one("h1[class*=title-2323565163]").text)
    print(soup.select_one("span[class*=currentPrice-441857624]").text)


getUrls()