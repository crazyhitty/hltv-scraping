# -*- coding: utf-8 -*-
import scrapy


class EventsSpider(scrapy.Spider):
    name = 'events'
    allowed_domains = ['hltv.org']
    start_urls = ['https://www.hltv.org/events/archive']

    def parse(self, response):
        for href in response.css('div.events-month a::attr(href)').extract():
            event_meta = href.split('/')
            if event_meta[1] == 'events' and event_meta[2].isdigit():
                yield {
                    'event_id': event_meta[2],
                    'event_name': event_meta[3],
                }

        for next_page in response.css('a.pagination-next'):
            yield response.follow(next_page, self.parse)
