import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy
import time
from os import path

url = 'https://www.kijiji.ca/b-for-rent/ontario'
baseurl = 'https://www.kijiji.ca'
baseForOntario = '/c30349001l9004'
pageNos = '/page-'
apartment = 'v-apartments-condos'
roomRent = 'room rent'
adurl = []
listing = []
urlToSave = []
title = []
prices = []
description = []
location = []
datePosted = []
features = []
linksFromText = []
listingType = []
adId = []
savePoints = [1000,2000,3000,4000,5000,6000,7000]

def getUrls(noPages):

    if path.exists('links.txt'):
        with open('links.txt', 'r') as f:
            linksFromText = f.readlines()
        getDetails(linksFromText)
    else:
        for i in range(noPages):
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
            #time.sleep(1)
        print(len(adurl))

        ## since connection gets closed by the server its better to save the links to a text file
        saveLinks(adurl)
        getDetails(adurl)

def getDetails(urls):
    
    urls = urls[6766:]
    print(len(urls))

    i =0;
    try:
        for url in urls:
            print(url)
            listDetails = ""
            listDetailsTwo = []
            url = url.rstrip('\n')
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                adTitle = soup.select_one("h1[class*=title-2323565163]").text
                title.append(adTitle)
                adPrice = soup.select_one("span[class*=currentPrice-2842943473]").text
                prices.append(adPrice)
                adDescription = soup.find_all('div', attrs={'class' : 'descriptionContainer-3544745383'})
                description.append(adDescription)
                adLocation = soup.find('span', attrs={'class' : 'address-3617944557'})
                location.append(adLocation)
                date = soup.find('time')   
                datePosted.append(date)

                # get features from the listing 
                # we have two kinds of listing apartments and room rentals.

                if apartment in url:
                    adfts = soup.find_all('li', attrs={'class' : 'realEstateAttribute-3347692688'})
                    for ft in adfts:
                        #dd = ft.find('div').text
                        dd = ft.find_all('div')
                        listDetails = listDetails + str(dd) + " || "
                    features.append(listDetails)
                    listingType.append(apartment)
                    urlToSave.append(url)
                    adid = getAdId(url)
                    adId.append(adid)
                else:                
                    adfts = soup.find_all('dl', attrs={'class' : 'itemAttribute-983037059'})
                    for ft in adfts:
                        dd = ft.find('dd').text
                        dt = ft.find('dt').text
                        listDetails = listDetails + str(dt) + " : " + str(dd) + " || "
                    features.append(listDetails)
                    listingType.append(roomRent)
                    urlToSave.append(url)
                    adid = getAdId(url)
                    adId.append(adid)
                print("Scraping listing : ",str(i))
                #response.close()
                i += 1
                if i in savePoints:
                    saveToDisk(i)
                    #break
                time.sleep(1)
            except Exception as e:
                pass
        saveToDisk(i)
    except Exception as e: 
        print(e)
        pass
    #saveToDisk()

def getAdId(advt):
    advtList = advt.split("/")
    adlen = len(advtList)
    return advtList[adlen-1]


def saveToDisk(i):
    print("saving ***")
    name='kijiji'+str(i)+'.csv'
    d = {'adId':adId, 'Title':title,'Price':prices,'Description':description, 'Location':location,'Ddate Posted':datePosted, 'Location':location, 'Features' : features, 'URL':urlToSave, 'Type' : listingType}
    df = pd.concat([pd.Series(v, name=k) for k, v in d.items()], axis=1)
    df.to_csv(name,index=False)
    resetAll()
    
def saveLinks(liks):
    with open('links.txt', 'w') as f:
        for item in liks:
            f.write("%s\n" % item)

    f.close()

def resetAll():
    print('cleaning')
    adId.clear()
    title.clear()
    prices.clear()
    description.clear()
    datePosted.clear()
    location.clear()
    features.clear()
    urlToSave.clear()
    listingType.clear()
    

# call main methond to start scraping by passing number of pages wanted to scrape  
no_pages = 300
getUrls(no_pages)