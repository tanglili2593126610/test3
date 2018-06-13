# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import requests
import json
import logging


class CookiesMiddleware(object):
    def __init__(self, cookies_pool_url):
        self.cookies = cookies_pool_url
        self.logger = logging.getLogger(__name__)

    def get_random_cookies(self):    # 从自定义的cookies池中获取一个cookies
        try:
            response = requests.get(self.cookies)
            if response.status_code == 200:
                return json.loads(response)
        except ConnectionError:
            return None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            cookies_pool_url=crawler.settings.get('COOKIES_POOL_URL')   # 从settings中获取到COOKIES_POOL_URL的值，return即可把获取到的值给类的构造函数——init——
        )

    def process_request(self, request, spider):
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            self.logger.debug('Using cookies~~~~~~~~~~')
        else:
            self.logger.debug('No cookies~~~~~~~~~~~~~~')

    def process_response(self,request,response,spider):
        if response.status_code in [300,301,302,303]:
            try:
                redirect_url = response.headers['location']
                if 'passport' in redirect_url:
                    self.logger.warning('Need Login, updating cookies')
                elif 'weibo.cn/security' in redirect_url:
                    self.logger.warning('被禁止')
                request.cookies = self.get_random_cookies()
                return request     # 换一个cookies重新加入请求队列
            except:
                raise IgnoreRequest
        else:
            return response

