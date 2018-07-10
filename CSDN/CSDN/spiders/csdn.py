# -*- coding: utf-8 -*-
import scrapy
from CSDN.items import CsdnItem
from scrapy.selector import Selector

class CsdnSpider(scrapy.Spider):

    name = 'csdn'
    allowed_domains = ['blog.csdn.net', 'so.csdn.net']

    def __init__(self, search=None):
        super(CsdnSpider, self).__init__()
        self.start_urls = ['https://so.csdn.net/so/search/s.do']
        search = ' '.join(search.split('+'))
        self.post_data = {
            'q': search,
            't': 'blog',
            'o': '',
            's': '',
            'l': ''
        }

    def start_requests(self):
        yield scrapy.FormRequest(url=self.start_urls[0], method='GET', meta={'page': 1}, formdata=self.post_data, callback=self.parse, dont_filter=True)

    def parse(self, response):
        page = response.meta['page']
        if page > 20:
            return
        for url in response.xpath('//dl[contains(@class, "search-list")]'):
            url = url.xpath('./dt/a[1]/@href').extract()
            if url:
                yield scrapy.Request(url=url[0], meta={'data': url[0]}, callback=self.parse_detail, dont_filter=True)
        next_page = response.xpath('//span[@class="page-nav"]/a[last()]/@href').extract()[0]
        if next_page:
            yield scrapy.Request(url=r'https://so.csdn.net/so/search/s.do' + next_page, meta={'page': page + 1}, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        item = CsdnItem()
        item['url'] = response.meta['data']
        item['title'] = response.xpath('//*[@id="mainBox"]/main/div[1]/div[1]/h1/text()').extract()[0]
        item['Reading_number'] = response.xpath('//*[@id="mainBox"]/main/div[1]/div[2]/div/div/span/text()').extract()[0]
        yield item

