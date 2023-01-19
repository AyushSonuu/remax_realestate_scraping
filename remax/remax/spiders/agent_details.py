import scrapy
import requests
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy import Selector
from selenium import webdriver
# from shutil import which
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
class url_extracter_class:
    @classmethod
    def urls_to_send(cls,zip_codes:list):

        zip_dict_lst = []
        for zip in zip_codes:
            api_url = f"https://www.remax.com/api-v2/listings/autocomplete/?autocompleteValue={zip}&categories%5B0%5D=states&categories%5B1%5D=places&categories%5B2%5D=zips"
            a = ((requests.get(api_url).json()))
            zip_dict_lst.append(a)

        url_lst = []
        for dic in zip_dict_lst:
            state = dic["zips"][0]["state"].lower()
            city = dic["zips"][0]["city"].lower()
            city = city.replace(" ","-")
            end_url = city+"-"+state
            url = f"https://www.remax.com/real-estate-agents/{end_url}"
            url_lst.append(url)
            print(city)

        return url_lst

    


class AgentDetailsSpider(scrapy.Spider,url_extracter_class):
    name = 'agent_details'
    allowed_domains = ['www.remax.com']
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

    # start_urls = ['http://www.remax.com/']
    def start_requests(self):
        zip_codes = ["80237","55125","80111","20016","92604"]
        url_lst = url_extracter_class.urls_to_send(zip_codes)
        yield(SeleniumRequest(url = url_lst[0],headers={
                'User-Agent': self.user_agent
                },  callback = self.parse,
                    wait_time = 5,
                    screenshot=True,
                    ))

    def parse(self, response):
        driver =  response.request.meta['driver']
        # print(driver.page_source)
        
        for agents in response.selector.xpath("//div[@class='info']/a"):
            agent_relative_url = agents.xpath(".//@href").get()
            agent_absolute_url = f"https://www.remax.com{agent_relative_url}"
            yield SeleniumRequest(url=agent_absolute_url,callback=self._agent_,
                                    headers={
                                    'User-Agent': self.user_agent
                                    },meta = {'Agent URL':agent_absolute_url},)
            
        # with open('image.png', 'wb') as image_file:
        #     image_file.write(response.meta['screenshot'])

