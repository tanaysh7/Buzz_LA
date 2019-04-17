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
        event['time']={'date':i.find("abbr",{'class':'dtstart'})['title'].split('T')[0],'start_time':i.find("abbr",{'class':'dtstart'})['title'].split('T')[1].split('-')[0]}
        event['location']=i.find("div",{'class':'location'}).text.strip()
        result.append(event)
    
  
    newurl = soup.find("a",{'class':'pagearrow right'})['href']
    
    #Code to repeat for all pages this year
    if int(newurl.split('/')[-3])<2020:
        print(newurl)
        time.sleep(2)
        result+=crawl_USC(newurl)
         
    return result
def campus_crawl(url):
    result = []
    driver = webdriver.Chrome()
    driver.get(url)
    #driver.implicitly_wait(3)
    print([i.text for i in driver.find_elements_by_xpath("//button")])
    # while(driver.find_elements_by_xpath("//button")[-1].text=='Load More'):
    #     driver.find_elements_by_xpath("//button")[-1].click()
    #     time.sleep(3)
    # driver.find_elements_by_xpath("//button")[-1].click()
    # time.sleep(3)
    htmlSource = driver.page_source
    elist  = BeautifulSoup(htmlSource, "lxml")
    #print(elist.find('div',{'id':'event-discovery-list'}).find_all('a')[-1].text)
    linklist=elist.find('div',{'id':'event-discovery-list'}).find_all('a')
    for i in linklist:
        event=dict()
        event['title']=i.find("h3").text.strip()
        event['link']=url.split('/engage')[0]+i['href'].strip()
        event['description']=''
        event['tags']=[]
        event['time']={'start_time':[k.parent.text for k in i.find_all('svg')][0].split('at')[1].strip('PDT').strip(),'date':[k.parent.text for k in i.find_all('svg')][0].split('at')[0].strip()}
        event['location']=[k.parent.text for k in i.find_all('svg')][1]
        result.append(event)
       
    return result
def crawl_Viterbi(url):
    result = []
    driver = webdriver.Chrome()
    driver.get(url)
   
    htmlSource = driver.page_source
    elist  = BeautifulSoup(htmlSource, "lxml")

    
    for i in elist.find('div',{'id':'events'}).ul.find_all('li', recursive=False):
    
        event=dict()
        
        
        date_string=(i.find('div',{'class':'event_stats'}).strong.text)
        if '@' in date_string:
            event['date_time']={'date':date_string.split('@')[0],'start_time':date_string.split('@')[1].split('-')[0]}
        else:
            event['date_time']=date_string.strip()

        event['tags']=[i.find('div',{'class':'event_stats'}).find_all('p')[-1].text]

    
        
        event['title']=i.find("h3").a.text.strip()
        event['link']=url.split('?')[0]+i.find("h3").find("a")['href'].strip()
        event['description']=i.find("blockquote").text.strip()
        
        
        
        loc=i.find("blockquote").next_sibling.text.strip()
        if 'Location:' in loc:
            event['location']=loc.split('Location:')[1]
        else:
            event['location']='USC'
        result.append(event)

    print(result)
    
    return result

url = 'https://calendar.usc.edu/calendar'
crawl  = campus_crawl('https://usc.campuslabs.com/engage/events')+crawl_USC(url)+crawl_Viterbi('https://viterbi.usc.edu/news/events/calendar/?calendar=1&month')


with open("USC.json","w") as f:
    json.dump(crawl,f)