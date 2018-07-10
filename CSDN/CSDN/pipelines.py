# -*- coding: utf-8 -*-
import re
import csv
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CsdnPipeline(object):

    def __init__(self):
        self.source = {}
        self.file = open('result.txt', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        detail = {}
        detail['url'] = item['url']
        detail['title'] = item['title']
        detail['Reading_number'] = item['Reading_number']
        # 整理数据
        number = re.search('\d+', detail['Reading_number']).group()
        self.source.update({number: detail['title'] + ' '*3 + detail['url']})
        return item

    def close_spider(self, spider):
        max_list = []
        for i in self.source.keys():
            max_list.append(int(i))
        max_list.sort(reverse=True)
        for i in max_list:
            number = str(i)
            self.file.write(number + ' '*3 + self.source[number] + '\n')

        self.file.close()




