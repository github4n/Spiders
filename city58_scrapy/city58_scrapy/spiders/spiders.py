# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import City58ScrapyItem
import time


class Spiders(scrapy.Spider):
    name = 'city58'
    allowed_domains = ['gz.58.com']
    start_urls = ['http://gz.58.com/chuzu/pn1/']
    chiurl = []

    def parse(self, response):
        jpy = PyQuery(response.text)
        li_list = jpy('body > div.mainbox > div.main > div.content > div.listBox > ul > li').items()
        for li in li_list:
            item = City58ScrapyItem()
            a_tag = li('div.des > h2 > a')
            item['name'] = a_tag.text()
            item['url'] = a_tag.attr('href')
            item['price'] = li('div.listliright > div.money > b').text() + str('元/月')
            item['room'] = li('div.des > p').text().replace('\xa0', ' ')

            self.chiurl.append(a_tag.attr('href'))
            for i in range(len(self.chiurl)):
                url = self.chiurl[i]
                if url is not None:
                    time.sleep(0.2)
                    yield scrapy.Request(url, callback=self.parse_chiurl)

        for i in range(2, 71):
            next_page = 'http://gz.58.com/chuzu/pn' + str(i)
            if next_page is not None:
                time.sleep(0.1)
                yield scrapy.Request(next_page, callback=self.parse)  # 对下一页面发起请求，注册回调以处理第二页

    def parse_chiurl(self, response):
        item = City58ScrapyItem()
        jpy = PyQuery(response.text)
        li_list = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li').items()
        item['des'] = jpy('body > div.main-wrap > div.house-detail-desc > div.main-detail-info.fl > div.house-word-introduce.f16.c_555 > ul > li:nth-child(2) > span.a2 > ul > span').text()
        for li in li_list:
            item['type'] = li('span:nth-child(2)').text().replace('\xa0', ' ')
            item['dire'] = li('span:nth-child(2)').text().replace('\xa0', ' ')
        yield item
