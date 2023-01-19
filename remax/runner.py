import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from remax.spiders.agent_details import AgentDetailsSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(AgentDetailsSpider)
process.start()

