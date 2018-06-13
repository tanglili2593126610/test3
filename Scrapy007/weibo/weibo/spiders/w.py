# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest

class WSpider(scrapy.Spider):
    name = 'w'
    allowed_domains = ['weibo.cn']
    start_urls = ['http://weibo.cn/']
    max_page = 100
    search_url = 'http://weibo.cn/search/mblog'

    def start_requests(self):
        keyword = '000001'   # 用户输入的查询关键字
        url = '{url}?hideSearchFrame=&keyword={keyword}'.format(url=self.search_url, keyword=keyword)
        for page in range(self.max_page+1):
            postdata = {
                'mp': self.max_page,
                'page': page
            }
            yield FormRequest(url=url, formdata=postdata, callback=self.parse_index)

    def parse_index(self, response):
        pass
