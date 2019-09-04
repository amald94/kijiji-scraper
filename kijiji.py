import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy

url = 'https://www.kijiji.ca/b-for-rent/ontario'
baseurl = 'https://www.kijiji.ca'
baseForOntario = '/c30349001l9004'
pageNos = '/page-'
adurl = []
listing = []

title = []
prices = []
description = []
location = []
datePosted = []
features = []

def getUrls():

    for i in range(1):
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

    try:
        i =0
        for url in urls:
            print(url)
            listDetails = ""
            #url = 'https://www.kijiji.ca/v-room-rental-roommate/oakville-halton-region/renting-a-private-furnished-room-very-clean-very-quiet-house/1456771236?enableSearchNavigationFlag=true'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            adTitle = soup.select_one("h1[class*=title-2323565163]").text
            #print(adTitle)
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
            #print(date)
            datePosted.append(date)
            #listFt = str(title) + "||" + str(price) + "||" + str(description) + "||" + str(location) + "||" + str(date) 

            adfts = soup.find_all('dl', attrs={'class' : 'itemAttribute-983037059'})
            for ft in adfts:
                dt = ft.find('dt').text
                #print(dt)
                dd = ft.find('dd').text
                #print(dd)

                listDetails = listDetails + str(dt) + ":" + str(dd)
            features.append(listDetails)

            print("Scraping listing : ",str(i))
            i += 1
        #print(listDetails)
        saveToDisk()
    except Exception as e: 
        print(e)
        saveToDisk()

        
def saveToDisk():

    # adft = advt.split("||")
    # print(advt)

    df = pd.DataFrame({'Title':title,'Price':prices,'Description':description, 'Location':location,'Ddate Posted':datePosted, 'Location':location, 'Features' : features})
    df.to_csv('kijiji.csv',index=False)
    





getUrls()