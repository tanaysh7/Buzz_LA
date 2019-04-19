# Scraper to download extra information useful for tagging different events
from bs4 import BeautifulSoup
import requests
import json
import sys
from lxml import html
import os
import json
import time
from selenium import webdriver 


urls = ['https://calendar.usc.edu/calendar','https://usc.campuslabs.com/engage/events','https://viterbi.usc.edu/news/events/calendar/?calendar=1&month']


def usc_calendar(link):



    return data

def usc_campus(link):


    return data

# def viterbi(link):
    #clean data nothing required

#     return data

def ucla(link):


    return data

with open("USC.json","w") as f:
    usc_list=json.load(f)
    
    for event in usc_list:
        if event.link[:10]==urls[0]:
            data=usc_calendar(event.link)
            event['tags']=data['tags']
            event['description']=data['description']
        elif event.link[:10]==urls[1]:
            data=usc_campus(event.link)
            event['tags']=data['tags']
            event['description']=data['description']
      
    json.dump(usc_list,f)

with open('UCLA.json') as fu:
    ucla_list=json.load(fu)
    
    for event in ucla_list:
        event['description']=ucla(event.link)
    json.dump(ucla_list,fu)



        
        



    