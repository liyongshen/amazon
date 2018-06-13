# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from amazon.items import AmazonItem

class AmazonspiderSpider(CrawlSpider):
    name = 'amazonspider'
    allowed_domains = ['amazon.cn']
    # 亚马逊首页的源代码商品分类的a标签url是通过渲染加成的，无法直接通过Rule提取,启用selenium
    start_urls = ['https://www.amazon.cn']
    rules = [
        # '/b/ref=sa_menu_office_l3_b114799071?ie=UTF8&node=114799071'
        # 提取除了kindle类的所有分类链接
        Rule(LinkExtractor(allow=r"/ref=sa_menu.*?l3",deny='kindle'),follow=True),
        # 提取商品列表中其他页面的链接，并使用回调函数提取商品信息
        Rule(LinkExtractor(allow=r"/s/ref=.*?page="),callback="parse_detail",follow=True)
            ]

    def parse_detail(self, response):
        li_list=response.xpath("//ul[@id = 's-results-list-atf']/li")

        for li in li_list:
            item = AmazonItem()
            # 所属分类
            item["type"] = response.xpath('//span[@class="a-color-state a-text-bold"]/text()').extract_first()
            # 商品图片
            item["img_url"]=li.xpath('.//img/@src').extract_first()
            # 商品名称
            item["product_name"]=li.xpath('.//h2/text()').extract_first()
            # 商品url
            item["product_url"]=li.xpath('.//div[@class = "a-row a-spacing-mini"]//a/@href').extract_first()
            # 商品价格
            item["product_price"]=li.xpath('.//a[@class="a-link-normal a-text-normal"]/span/text()').extract_first()
            # 商品评分
            item["product_score"]=li.xpath('.//a[@class="a-popover-trigger a-declarative"]//span[@class="a-icon-alt"]/text()').extract_first()
            # 商品运费
            item["product_freight"]=li.xpath('.//a[@class="a-link-normal a-text-normal"]/following-sibling::span[@class="a-size-small a-color-secondary"]/text()').extract_first()
            yield item
