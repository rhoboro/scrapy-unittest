# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler.items import BlogItem


class MyBlogSpider(CrawlSpider):
    name = 'my_blog'
    allowed_domains = ['www.rhoboro.com']
    start_urls = ['http://www.rhoboro.com/']

    rules = (
        Rule(LinkExtractor(allow=r'/index\d+.html'), callback='parse_list', follow=True),
    )

    def parse_list(self, response):
        for detail in response.xpath('//div[@class="post-preview"]/a/@href').extract():
            yield Request(url=response.urljoin(detail), callback=self.parse_detail)

    def parse_detail(self, response):
        item = BlogItem()
        item['title'] = response.xpath('//div[@class="post-heading"]//h1/text()').extract_first()
        item['body'] = response.xpath('//article').xpath('string()').extract_first()
        item['tags'] = response.xpath('//div[@class="tags"]//a/text()').extract()
        yield item
