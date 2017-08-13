# -*- coding: utf-8 -*-

import re
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler.items import BlogItem

num_re = re.compile(r'\d+')


class MyBlogSpider(CrawlSpider):
    name = 'my_blog'
    allowed_domains = ['www.rhoboro.com']
    start_urls = ['http://www.rhoboro.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/index\d+.html'), callback='parse_list', follow=True),
    )

    def parse_list(self, response):
        """一覧画面のパース処理

        @url http://www.rhoboro.com/index2.html
        @returns item 0 0
        @returns requests 0 10
        """
        index = num_re.findall(response.url)
        cookies = {
            'index': int(index[0]) if index else 1
        }
        for detail in response.xpath('//div[@class="post-preview"]/a/@href').extract():
            yield Request(url=response.urljoin(detail), cookies=cookies, callback=self.parse_detail)

    def parse_detail(self, response):
        """詳細画面のパース処理

        @url http://www.rhoboro.com/2017/08/05/start-onomichi.html
        @returns item 1
        @scrapes title body tags index
        @item_validate
        @cookies index 2
        """
        item = BlogItem()
        item['title'] = response.xpath('//div[@class="post-heading"]//h1/text()').extract_first()
        item['body'] = response.xpath('//article').xpath('string()').extract_first()
        item['tags'] = response.xpath('//div[@class="tags"]//a/text()').extract()
        item['index'] = response.request.cookies['index']
        yield item
