# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
import json
import calendar
import urllib.parse as urlparse
from urllib.parse import parse_qs

START_YEAR = 2021
START_MONTH = 3

FINAL_YEAR = 2012
FINAL_MONTH = 8


def get_start_urls():
    urls = []
    year = START_YEAR
    month = START_MONTH

    while year >= FINAL_YEAR:
        date_range = calendar.monthrange(year, month)
        start = datetime.today().replace(day=1, month=month, year=year).strftime("%Y-%m-%d")
        end = datetime.today().replace(day=date_range[1], month=month, year=year).strftime("%Y-%m-%d")

        urls.append('https://www.hltv.org/stats?startDate=' + start + '&endDate=' + end)

        month -= 1

        if month == 0:
            month = 12
            year -= 1

        if year == FINAL_YEAR and month == FINAL_MONTH:
            break

    return urls


class EventsSpider(scrapy.Spider):
    name = 'weapon_stats_per_month'
    allowed_domains = ['hltv.org']

    start_urls = get_start_urls()

    print('weapon_stats_per_month', 'start_urls', start_urls)

    def parse(self, response):
        chart_config = json.loads(response.css('div.graph::attr(data-fusionchart-config)').get())

        yield {
            'start_date': parse_qs(urlparse.urlparse(response.request.url).query)['startDate'][0],
            'end_date': parse_qs(urlparse.urlparse(response.request.url).query)['endDate'][0],
            'weapon_stats': chart_config['dataSource']['data'],
        }
