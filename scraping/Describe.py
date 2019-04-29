# Scraper to download extra information useful for tagging different events
from bs4 import BeautifulSoup
import requests
import json
import sys
from lxml import html
import os
import json
import re
import time
from selenium import webdriver 


urls = ['https://calendar.usc','https://usc.campusla','https://viterbi.usc.']


def usc_calendar(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "lxml")
    if soup.find('div',{'class','description'}):
        return soup.find('div',{'class','description'}).text
    else:
        print(link)
        return ''
  


def usc_campus(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "lxml")
    data=soup.find_all('script')[4].text
    data=json.loads(data.strip('window.initialAppState = ').strip(';'))
    tags=[]

    for i in data['preFetchedData']['event']['categories']:
        tags.append(i['name'])
    

    desc=re.sub('<[^<]+?>', '', data['preFetchedData']['event']['description'])
    
    return (desc,tags)


def ucla(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.text, "lxml")
    return soup.find("div",{'id':'event-details'}).text.split('Additional Information')[-1]


# with open("USC.json",'r') as f:
    
#     usc_list=json.loads(f.read())
    
#     for i in range(len(usc_list)):
#         event=usc_list[i]
#         if event['link'][:20]==urls[0]:
#             event['description']=usc_calendar(event['link'])
#         elif event['link'][:20]==urls[1]:
#             data=usc_campus(event['link'])
#             event['tags']=data[1]
#             event['description']=data[0]

# with open("USC.json",'w') as f:     
#     json.dump(usc_list,f)

with open('UCLA.json') as fu:
    ucla_list=json.load(fu)
    
    for i in range(len(ucla_list)):
        event=ucla_list[i]
        event['description']=ucla(event['link'])
with open("UCLA.json",'w') as f:     
    json.dump(ucla_list,f)



        
        



    