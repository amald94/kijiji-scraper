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
apartment = 'v-apartments-condos'
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
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            adTitle = soup.select_one("h1[class*=title-2323565163]").text
            title.append(adTitle)
            adPrice = soup.select_one("span[class*=currentPrice-2842943473]").text
            prices.append(adPrice)
            adDescription = soup.find_all('div', attrs={'class' : 'descriptionContainer-3544745383'})
            description.append(adDescription)
            adLocation = soup.find('span', attrs={'class' : 'address-3617944557'})
            location.append(adLocation)
            date = soup.find('time').text   
            datePosted.append(date)

            # get features from the listing 
            # we have two kinds of listing apartments and room rentals.

            if apartment in url:
                adfts = soup.find_all('li', attrs={'class' : 'realEstateAttribute-3347692688'})
                for ft in adfts:
                    dd = ft.find('div').text
                    listDetails = listDetails + str(dd) + " : "
            else:                
                adfts = soup.find_all('dl', attrs={'class' : 'itemAttribute-983037059'})
                for ft in adfts:
                    dt = ft.find('dt').text
                    dd = ft.find('dd').text
                    listDetails = listDetails + str(dt) + " : " + str(dd)
            features.append(listDetails)

            print("Scraping listing : ",str(i))
            i += 1
        saveToDisk()
    except Exception as e: 
        print(e)
        saveToDisk()

        
def saveToDisk():

    df = pd.DataFrame({'Title':title,'Price':prices,'Description':description, 'Location':location,'Ddate Posted':datePosted, 'Location':location, 'Features' : features, 'URL':adurl})
    df.to_csv('kijiji.csv',index=False)
    

getUrls()