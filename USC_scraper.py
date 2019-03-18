#USCraper
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



def crawl_USC(url):
    
    result = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")

    
    for i in soup.find_all("div",{'class':'item event_item vevent'}):
        event=dict()
        event['title']=i.find("h3",{'class':'summary'}).text.strip()
        event['link']=i.find("h3",{'class':'summary'}).find("a")['href'].strip()
        event['description']=i.find("h4",{'class':'description'}).text.strip()
        event['tags']=i.find("div",{'class':'event_filters'}).text.split(',')
        event['time']={'date':i.find("abbr",{'class':'dtstart'})['title'].split('T')[0],'start_time':i.find("abbr",{'class':'dtstart'})['title'].split('T')[1].split('-')[0],'end_time':i.find("abbr",{'class':'dtstart'})['title'].split('T')[1].split('-')[1]}
        event['location']=i.find("div",{'class':'location'}).text.strip()
        result.append(event)
    
  
    newurl = soup.find("a",{'class':'pagearrow right'})['href']
    print(newurl)
    #Code to repeat for all pages this year
    # if newurl!='https://calendar.usc.edu/calendar/week/2020/1/4':
    #     time.sleep(5)
    #     result+=crawl_USC(newurl)
         
    return result
def campus_crawl(url):
    result = []
    driver = webdriver.Chrome()
    driver.get(url)
    htmlSource = driver.page_source
    
    elist  = BeautifulSoup(htmlSource, "lxml")
    print(elist.text)
    # linklist=elist.find('div',{'id':'event-discovery-list'}).find_all('a')
    # print(linklist)
    # for i in linklist:
    #     event=dict()
    #     event['title']=i.find("h3").text.strip()
    #     event['link']=url.split('/engage')[0]+i['href'].strip()
    #     event['description']=''
    #     event['tags']=''
    #     event['time']=[k.parent.text for k in i.find_all('svg')][0]
    #     event['location']=[k.parent.text for k in i.find_all('svg')][1]
    #     result.append(event)
       
    return result

url = 'https://calendar.usc.edu/calendar'
crawl  = campus_crawl('https://usc.campuslabs.com/engage/events')#+crawl_USC(url)


with open("USC.json","w") as f:
    json.dump(crawl,f)