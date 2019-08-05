# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pypinyin
from Boss.items import BossItem


class BossPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, BossItem):
            # BossItem.__class__
            pass

        return item


class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT')
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
        self.cursor = self.db.cursor()
        self.city = spider.city
        self.keyword = spider.keyword
        self.table = ''.join(pypinyin.lazy_pinyin(self.city)) + '_' + ''.join(pypinyin.lazy_pinyin(self.keyword))
        self.cursor.execute('drop table if exists {}'.format(self.table))
        self.cursor.execute('''
        CREATE TABLE {} (
          id int(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
          job_title varchar(255),
          salary varchar(255),
          url varchar(255),
          address varchar(255),
          experience varchar(255),
          education varchar(255),
          company_name varchar(255),
          company_url varchar(255),
          industry varchar(255),
          company_finance varchar(255),
          company_size varchar(255)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        '''.format(self.table))

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (self.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
