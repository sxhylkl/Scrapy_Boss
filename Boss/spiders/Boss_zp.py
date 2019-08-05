# -*- coding: utf-8 -*-
import json
import scrapy
from Boss.items import BossItem


class BossZpSpider(scrapy.Spider):
    name = 'Boss_zp'
    allowed_domains = ['www.zhipin.com']
    # start_urls = ['http://www.zhipin.com/']
    base_url = 'https://www.zhipin.com'
    city_json_url = 'https://www.zhipin.com/wapi/zpCommon/data/city.json'
    city_url = 'https://www.zhipin.com/job_detail/?query={query}&city={city}&industry=&position='
    # custom_settings = {
    #     'MYSQL_TABLE':'xiamen'
    # }

    def __init__(self, city=None, keyword=None, *args, **kwargs):
        super(BossZpSpider, self).__init__(*args, **kwargs)
        if len(city) > 3 and city[-3] == '自治区':
            if city[0:3] == '内蒙古':
                city = '内蒙古'
            else:
                city = city[0:2]
        if city[-1] == '省':
            city = city[0:-1]
        elif city[-1] == '市':
            city = city[0:-1]
        self.keyword = keyword
        self.city = city

    def start_requests(self):
        return [scrapy.Request(self.city_json_url, callback=self.get_city_data)]

    def get_city_data(self, response):
        # self.logger.debug(response)
        result = json.loads(response.text)
        if result.get('zpData').get('cityList'):
            cityList = result.get('zpData').get('cityList')
            for province in cityList:
                if self.city != province.get('name'):
                    for city in province.get('subLevelModelList'):
                        if self.city == city.get('name'):
                            yield scrapy.Request(self.city_url.format(city=city.get('code'),query=self.keyword), callback=self.parse)
                            break
                    else:
                        continue
                    break
                else:
                    for city in province.get('subLevelModelList'):
                        yield scrapy.Request(self.city_url.format(city=city.get('code'),query=self.keyword), callback=self.parse)
                        continue
                    else:  # 内循环正常终止时
                        break

    def parse(self, response):
        try:
            for job_primary in response.xpath('//div[@class="job-primary"]'):
                item = BossItem()
                info_primary = job_primary.xpath('./div[@class="info-primary"]')
                item['job_title'] = info_primary.xpath('.//div[@class="job-title"]/text()').get()
                item['salary'] = info_primary.xpath('.//span[@class="red"]/text()').get()
                # item['url'] = info_primary.xpath('./h3/a').re('href="(.*?)"')[0]
                # item['url'] = info_primary.xpath('./h3/a/@href').get()
                item['url'] = self.base_url + info_primary.css('a[href*=job_detail]::attr(href)').get()
                job_info_num = info_primary.xpath('./p/em').getall()
                if len(job_info_num) == 3:
                    # 实习生的情况，工作地点 | 5天/周 | 6个月 | 学历要求
                    # 用正则表达式，是因为工作地点可能会出现比如`厦门 思明区`和`厦门 `的情况
                    job_info = info_primary.re('<p>(.*?)<em class="vline"></em>(.*?)<em class="vline"></em>(.*?)<em class="vline"></em>(.*?)</p>')
                    item['address'] = job_info[0].strip()
                    item['experience'] = job_info[2]
                    item['education'] = job_info[3]
                if len(job_info_num) == 2:
                    item['address'], item['experience'], item['education'] = info_primary.re('<p>(.*?)<em class="vline"></em>(.*?)<em class="vline"></em>(.*?)</p>')
                    item['address'].strip()
# ------------------------------------------------------------------------------------------------------------------------------------------------
                info_company = job_primary.xpath('./div[@class="info-company"]')
                item['company_name'] = info_company.xpath('./div/h3/a/text()').get()
                item['company_url'] = self.base_url + info_company.xpath('./div/h3/a/@href').get()
                company_info = info_company.xpath('./div/p/text()').getall()
                if len(company_info) == 3:
                    item['industry'], item['company_finance'], item['company_size'] = company_info
                elif len(company_info) == 2:
                    item['industry'], item['company_size'] = company_info
                elif len(company_info) == 1:
                    item['industry'] = company_info[0]
# ------------------------------------------------------------------------------------------------------------------------------------------------
                yield item
        except:
            pass

        # 解析下一页的链接
        new_links = response.xpath('//div[@class="page"]/a[@class="next"]/@href').getall()
        if new_links and len(new_links) > 0:
            new_link = new_links[0]
            yield scrapy.Request("https://www.zhipin.com" + new_link, callback=self.parse)
