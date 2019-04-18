#UCLAraper
from bs4 import BeautifulSoup
import requests
import json
import sys
from lxml import html
import os
import json
import time
from selenium import webdriver 


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)    



def crawl_UCLA(url):
    
    result = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")

    
    for i in soup.find("div",{'id':'results'}).find_all("div",{'class':'results-item'}):
        event=dict()
        event['title']=i.find("a").text.strip()
        event['link']=url+i.find("a")['href'].strip()
        event['description']=i.find("p",{'class':'description'}).text.strip()
        event['tags']=[]
        k=i
        while k.name!='h2':
            k=k.previous_element
        #print(k)
        event['date_time']={'date':k.text,'time':i.find("p",{'class':'results-info'}).text.split('m,')[0]+'m'}
        event['location']=i.find("p",{'class':'results-info'}).text.split('m,')[1]
        result.append(event)
    
    x=soup.find("ul",{'id':'pagination'}).find_all('li')[-1].find('a')['href']
    # Code to repeat for next pages
    # if x:
    #     newurl = url+x
    #     print(newurl)
    #     time.sleep(2)
    #     result+=crawl_UCLA(newurl)
         
    return result


url = 'http://happenings.ucla.edu'
crawl  = crawl_UCLA(url)


with open("UCLA.json","w") as f:
    json.dump(crawl,f)