# -*- coding: utf-8 -*-
from os import path
import scrapy
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs


class WeaponStatsByEventSpider(scrapy.Spider):
    name = 'weapon_stats_by_event'
    allowed_domains = ['hltv.org']

    try:
        base_path = path.dirname(__file__)
        events_json_file_path = path.abspath(path.join(base_path, "..", "..", "data", "events.json"))
        with open(events_json_file_path, 'r') as json_file:
            events = json.load(json_file)
            start_urls = list(map(lambda event: 'https://www.hltv.org/stats?event=' + event['event_id'], events))
    except FileNotFoundError:
        print('[WeaponStatsByEventSpider]', 'events.json does not exist')
        start_urls = []

    def parse(self, response):
        chart_config = json.loads(response.css('div.graph::attr(data-fusionchart-config)').get())

        event_dates = []
        for event_date in response.css('td.eventdate span::attr(data-unix)').extract():
            event_dates.append(event_date)

        if len(event_dates) == 0 or chart_config is None:
            return

        if len(event_dates) == 1:
            start_date = event_dates[0]
            end_date = event_dates[0]
        else:
            start_date = event_dates[0]
            end_date = event_dates[1]

        yield {
            'event_id': parse_qs(urlparse.urlparse(response.request.url).query)['event'][0],
            'event_name': response.css('div.eventname::text').get(),
            'event_start_date': start_date,
            'event_end_date': end_date,
            'weapon_stats': chart_config['dataSource']['data'],
        }
