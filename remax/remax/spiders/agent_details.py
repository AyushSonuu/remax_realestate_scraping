import scrapy


class AgentDetailsSpider(scrapy.Spider):
    name = 'agent_details'
    allowed_domains = ['www.remax.com']
    start_urls = ['http://www.remax.com/']

    def parse(self, response):
        pass
