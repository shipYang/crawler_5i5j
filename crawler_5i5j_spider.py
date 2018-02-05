from scrapy import Request
from crawler_5i5j.items import Product
import re
import scrapy
import requests
from lxml import etree

from crawler_5i5j import settings


class DmozSpider(scrapy.Spider):
    name = "5i5j"
    allowed_domains = "bj.5i5j.com"
    url = 'https://bj.5i5j.com'

    def start_requests(self):
        page_url = "https://bj.5i5j.com/ershoufang/daxingqu/n"
        max_page = self.fetch_max_page(page_url)

        for r in range(1, (int(max_page) + 1)):
            yield Request(url=page_url + str(r), callback=self.parse, dont_filter=True)

    @staticmethod
    def fetch_max_page(url):
        req = requests.post(url, headers=settings.DEFAULT_REQUEST_HEADERS)
        selector = etree.HTML(req.text)  # 将源码转化为能被XPath匹配的格式
        max_page = selector.xpath("/html/body/div[4]/div[1]/div[3]/div[2]/a[2]/text()")  # 返回为一列表
        return max_page[0]

    def parse(self, response):
        lis = response.xpath('/html/body/div[4]/div[1]/div[2]/ul/li')

        for li in lis:
            href = li.xpath("//div[@class='listImg']/a/@href")[0].extract()

            yield Request(url=self.url + str(href), callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):

        item = Product()
        housing_estate = response.xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[1]/a/text()")[0].extract()
        floor = response.xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[2]/text()")[0].extract()
        price_unit_num = response.xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div/p[1]/text()")[0].extract()
        rooms = response.xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div/p[1]/text()")[0].extract()
        floorage = response.xpath("/html/body/div[3]/div[2]/div[2]/div[1]/div[4]/div/p[1]/text()")[0].extract()
        orientation = response.xpath("/html/body/div[3]/div[2]/div[2]/div[2]/ul/li[3]/text()")[0].extract()

        decoration_situation =None  if  (response.xpath("//ul/li[span='装修：']/text()").extract())==[] else response.xpath("//ul/li[span='装修：']/text()")[0].extract()
        year= None if (response.xpath("//ul/li[span='年代：']/text()").extract())==[] else response.xpath("//ul/li[span='年代：']/text()")[0].extract()

        address=  None if (response.xpath("//ul/li[span='地铁：']/text()").extract())==[]  else response.xpath("//ul/li[span='地铁：']/text()")[0].extract()
        title = response.xpath("/html/body/div[3]/div[1]/div[1]/h1/text()")[0].extract()
        information = response.xpath("/html/body/div[3]/div[1]/div[1]/p/text()")[0].extract()
        s = information.split('|')[1]
        house_code = re.findall(r'\d{3,}', s)[0]
        term = None if len((information.split('|')[0]).split('·'))<2 else (information.split('|')[0]).split('·')[1]
        price_num = response.xpath('/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div/p[1]/text()')[0].extract()

        item['title'] = title
        item['address'] = address
        item['year'] = year
        item['decoration_situation'] = decoration_situation
        item['orientation'] = orientation
        item['floorage'] = floorage
        item['rooms'] = rooms
        item['price_unit_num'] = price_unit_num
        item['floor'] = floor
        item['housing_estate'] = housing_estate
        item['house_code'] = house_code
        item['price_num'] = price_num
        item['term'] = term

        return item
