import scrapy
import os
from datetime import datetime

class CaltechSpider(scrapy.Spider):
    name = "events"
    start_urls = ['https://www.caltech.edu/campus-life-events/master-calendar',]

    def parse(self, response):
        caltech = 'https://www.caltech.edu'
        header = response.css('div.event-listing-block__nav.d-flex.justify-content-between')
        date = header.xpath('//h2[@class = "event-listing-block__nav__title"]/text()').extract_first()
        next_page = header.xpath('a[2]/@href').extract_first()
        for event in response.css('div.event-listing-block__event.d-flex.flex-column.flex-md-row'):
            academic = event.xpath('div[2]//li[contains(a, "Academic")]/a/text()').extract_first()
            if academic == 'Academic': continue
            learn_more = event.xpath('div[2]//div[@class = "event-listing-block__event__learn-more"]/a/@href').extract_first()
            if learn_more is not None:
                yield response.follow(caltech + learn_more, self.download)
        if datetime.strptime(date, '%A, %B %d, %Y') < datetime.strptime('December 31 2019', '%B %d %Y'):
            if next_page is not None:
                yield response.follow(caltech + next_page, self.parse)
        
    def download(self, response):
        caltech = 'https://www.caltech.edu'
        title = response.css('div.event-page__header.offset-lg-1.mb-md-5.py-5.px-4.pl-lg-0').xpath('h1/text()').extract_first().strip().replace('"','')
        details = response.css('div.event-page__details.offset-lg-1.d-flex.flex-column.flex-sm-row')
        date_time = details.xpath('div[@class = "event-page__details__date-time"]//div[@class = "event-page__details__date-time__line"]/text()').extract()
        date_time = [d.strip() for d in date_time]
        start_date = date_time[0]
        start_time = date_time[1].split(" to ")[0] if len(date_time) == 2 else date_time[1]
        # end_date = date_time[0] if len(date_time) == 2 else date_time[-2]
        # end_time = date_time[1].split(" to ")[1] if len(date_time) == 2 else date_time[-1]
        location = details.xpath('div[2]/a/text()').extract_first()   
        seminar = response.xpath('//div[@class = "event-page__details__seminar-title mt-5 mt-sm-0 mb-2"]/text()').extract_first()
        title = ' - '.join([title, seminar.strip()]) if seminar else title
        title = title.replace('"','')
        link = response.url     
        if not location:
            location = 'no location'
        description = ' '.join([desc.strip() for desc in response.xpath('//div[@class = "rich-text"]//p//text()|//div[@class = "rich-text"]/text()').extract()])
        yield{
            'title': title,
            'link': link,
            'description': description,
            'tags': [],
            'time': {'start_time': start_time, 'date': start_date},
            'location': location
        }