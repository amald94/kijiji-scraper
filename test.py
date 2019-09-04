import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy
title = []
prices = []
description = []
location = []
datePosted = []
features = []
def getDetails():
    listDetails = ""
    url = 'https://www.kijiji.ca/v-apartments-condos/petawawa/gorgeous-3-bedroom-furnished-waterfront-home-for-rent/1457667231'
    response = requests.get(url)
    print('hi')
    soup = BeautifulSoup(response.text, "html.parser")
    adTitle = soup.select_one("h1[class*=title-2323565163]").text
    print(adTitle)
    title.append(adTitle)
    adPrice = soup.select_one("span[class*=currentPrice-2842943473]").text
    #print(adPrice)
    prices.append(adPrice)
    adDescription = soup.find_all('div', attrs={'class' : 'descriptionContainer-3544745383'})
    #print(description)
    description.append(adDescription)
    adLocation = soup.find('span', attrs={'class' : 'address-3617944557'})
    #print(adLocation)
    location.append(adLocation)
    date = soup.find('time').text   
    print(date)
    datePosted.append(date)
    #listFt = str(title) + "||" + str(price) + "||" + str(description) + "||" + str(location) + "||" + str(date) 

    featuresx = soup.find_all('li', attrs={'class' : 'realEstateAttribute-3347692688'})
    for ft in featuresx:
        dd = ft.find('div').text
        print(dd)

getDetails()