# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    job_title = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    industry = scrapy.Field()
    company_finance = scrapy.Field()
    company_size = scrapy.Field()