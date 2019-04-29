import scrapy
from lxml import etree
from lxml import html
import os
from datetime import datetime

class CalstatelaSpider(scrapy.Spider):
    name = "events"
    start_urls = ['http://www.calstatela.edu/univ/calendar/index.htm/Alumni', 'http://www.calstatela.edu/univ/calendar/index.htm/Art', \
        'http://www.calstatela.edu/univ/calendar/index.htm/Lectures%2C%20Readings%2C%20Symposia', 'http://www.calstatela.edu/univ/calendar/index.htm/Music', \
        'http://www.calstatela.edu/univ/calendar/index.htm/Special%20Event', 'http://www.calstatela.edu/univ/calendar/index.htm/Student', \
        'http://www.calstatela.edu/univ/calendar/index.htm/Training%20and%20Workshops', 'http://www.calstatela.edu/univ/calendar/index.htm/Video%20and%20Film']

    def parse(self, response):
        calstatela = 'https://www.calstatela.edu'
        next_page = response.xpath('//li[@class = "pager-next"]/a/@href').extract_first()
        events = response.xpath('//div[@class = "view-content"]//span[@class = "field-content"]/a/@href').extract()
        next_page = response.xpath('//li[@class = "pager-next"]/a/@href').extract_first()
        start_date = response.xpath('//span[@class = "date-display-start"]/text()|//span[@class = "date-display-single"]/text()').extract_first()
        if not start_date:
            start_date = ''
        for event in events:
            if event is not None:
                yield scrapy.Request(calstatela + event, callback=self.download, meta={'tag': response.xpath('//h1[@id = "page-title"]/text()').extract_first().lower(), 'start_date': start_date})
        if next_page is not None:
            yield response.follow(calstatela + next_page, self.parse)
        
    def download(self, response):
        calstatela = 'https://www.calstatela.edu'
        _time = response.xpath('//span[@class = "date-display-start"]/text()|//span[@class = "date-display-single"]/text()').extract_first()
        _time = _time.split(' - ')
        start_date = _time[0]
        start_time = _time[1]
        if start_time == "":
            start_time = response.xpath('//span[@class = "date-display-range"]//span[@class = "date-display-start"]/text()').extract_first()
        description = ' '.join([desc.strip() for desc in response.xpath('//div[@class = "field field-name-body field-type-text-with-summary field-label-above"]//p//text()').extract()])
        location = response.xpath('//div[@class = "field field-name-field-place field-type-text field-label-above"]/text()').extract_first()
        location = 'no location' if not location else location.strip()
        yield{
            'title': response.xpath('//h1[@id = "page-title"]/text()').extract_first(),
            'link': response.url,
            'description': description,
            'tags': [response.meta['tag']],
            'time': {'start_time': start_time, 'date': start_date},
            'location': location
        }    