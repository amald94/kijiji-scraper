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
adurl = []
listing = []

title = []
prices = []
description = []
location = []
datePosted = []
features = []
linksFromText = []

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
    
    #urls = urls[3364:]
    print(len(urls))

    try:
        i =0
        for url in urls:
            print(url)
            listDetails = ""
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
                #response.close()
                i += 1
                time.sleep(3)
            except Exception as e:
                pass
        saveToDisk()
    except Exception as e: 
        print(e)
        pass
    #saveToDisk()

        
def saveToDisk():
    print("saving ***")
    d = {'Title':title,'Price':prices,'Description':description, 'Location':location,'Ddate Posted':datePosted, 'Location':location, 'Features' : features, 'URL':adurl}
    df = pd.concat([pd.Series(v, name=k) for k, v in d.items()], axis=1)
    df.to_csv('kijiji.csv',index=False)
    
def saveLinks(liks):
    with open('links.txt', 'w') as f:
        for item in liks:
            f.write("%s\n" % item)

    f.close()

# call main methond to start scraping by passing number of pages wanted to scrape  
no_pages = 150
getUrls(no_pages)