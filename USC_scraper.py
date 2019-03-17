#USCraper
import io
import sys
from lxml import html
import requests
import os
import json
import time


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)    

from bs4 import BeautifulSoup
import requests
import json

def crawl_USC(url):
    
    result = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "lxml")

    
    for i in soup.find_all("div",{'class':'item event_item vevent'}):
        event=dict()
        event['title']=i.find("h3",{'class':'summary'}).text.strip()
        event['tags']=i.find("div",{'class':'event_filters'}).text.split(',')
        event['time']={'date':i.find("abbr",{'class':'dtstart'})['title'].split('T')[0],'start_time':i.find("abbr",{'class':'dtstart'})['title'].split('T')[1].split('-')[0],'end_time':i.find("abbr",{'class':'dtstart'})['title'].split('T')[1].split('-')[1]}
        event['location']=i.find("div",{'class':'location'}).text.strip()
        result.append(event)
    
    # #find paging page 
    # paging = soup.find_all("div",{'class':'paging clearfix'})
    # paging_link = paging[0].find_all('a',{'class':'paging__link'})
    # last_page = int([item.get('href').split('/')[-1] for item in paging_link][-1])

    # #looping through paging
    # for i in range(1,last_page):
    #     print url+str(i)

    #     #find article link
    #     req = requests.get(url+str(i))
    #     soup = BeautifulSoup(req.text, "lxml")
    #     news_links = soup.find_all("div",{'class':'article__list clearfix'})

    #     #looping through article link
    #     for idx,news in enumerate(news_links):
    #         news_dict = {}

    #         #find news title
    #         title_news= news.find('a',{'class':'article__link'}).text 

    #         #find urll news
    #         url_news = news.find('a',{'class':'article__link'}).get('href')
            
    #         #find news content in url
    #         req_news =  requests.get(url_news)
    #         soup_news = BeautifulSoup(req_news.text, "lxml")

    #         #find news content 
    #         news_content = soup_news.find("div",{'class':'read__content'})

    #         #find paragraph in news content 
    #         p = news_content.find_all('p')
    #         content = ' '.join(item .text for item in p)
    #         news_content = content.encode('utf8','replace')

    #         #wrap in dictionary 
    #         news_dict['id']=idx
    #         news_dict['url'] = url_news
    #         news_dict['title'] = title_news
    #         news_dict['content'] = news_content
    #         result.append(news_dict)

    newurl = soup.find("a",{'class':'pagearrow right'})['href']
    print(newurl)
    #Code to repeat for all pages this year
    # if newurl!='https://calendar.usc.edu/calendar/week/2020/1/4':
    #     time.sleep(5)
    #     result+=crawl_USC(newurl)
         
    # return result

url = 'https://calendar.usc.edu/calendar'
crawl  = crawl_USC(url)
with open("USC.json","w") as f:
    json.dump(crawl,f)