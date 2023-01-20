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
            url_ = f"https://www.remax.com/real-estate-agents/{end_url}"
            end = '?filters={"page":1}'
            url = url_+ end
            url_lst.append(url)
            # print(city)

        return url_lst

    


class AgentDetailsSpider(scrapy.Spider,url_extracter_class):
    name = 'agent_details'
    allowed_domains = ['www.remax.com']
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

    # start_urls = ['http://www.remax.com/']
    def start_requests(self):
        zip_codes = ["80237","55125","80111","20016","92604"]
        url_lst = url_extracter_class.urls_to_send(zip_codes)
        for ur in url_lst:
            yield(SeleniumRequest(url = ur,headers={
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
            yield SeleniumRequest(url=agent_absolute_url,callback=self.agent_,
                                    headers={
                                    'User-Agent': self.user_agent
                                    },meta = {'Agent URL':agent_absolute_url},)
            
        # with open('image.png', 'wb') as image_file:
        #     image_file.write(response.meta['screenshot'])

    def agent_(self,response):
        adress = response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/a/text()").getall()
        
        adr_lst = []
        for adr in adress:
            adr_lst.append(adr.strip())
        

        phones = response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/h4/span/a/text()").getall()
        
        phone_dic = {}
        for i,phone in enumerate(phones):
            p = phone.strip()
            key = f"phone {i}"
            phone_dic[key] = p

        specialities = response.selector.xpath("//div[@class='col md:max-w-1/2 lg:max-w-full']/div/div/h4[contains(text(),'Specia')]/following-sibling::node()/span/text()").getall()
        spe_lst = []
        for sep in specialities:
            s = sep.strip()
            spe_lst.append(s)
        
        spec_o = " ".join(spe_lst)

        about_lst = response.selector.xpath("(//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[2]/div/child::node()//text())").getall()
        a = []
        for ab in about_lst:
            b = ab.strip()
            b = " ".join(b.split())
            if len(b) > 25:
                a.append(b)

        zip = (adr_lst[0]+" "+adr_lst[1])
        zip_cd = ""
        if zip[-5:].isalnum():
            zip_cd = zip[-5:]
        else:
            zip_cd = zip[-10:]

        lang = response.selector.xpath("//div[@class='col md:max-w-1/2 lg:max-w-full']//h4[contains(text(),'Languages')]/following-sibling::p/span/text()").getall()
        language = " ".join(lang)

        yield{
            "Agent url":response.meta.get("Agent URL"),
            "Name":response.selector.xpath("normalize-space(//*[@id='__layout']/div/main/article/section/div/div[1]/h1/text())").get(),
            "Profile Pic":response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[1]/div/div[1]/img/@src").get(),
            "Role":response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[1]/h6/span[1]/text()").get(),
            "Lic No":response.selector.xpath("normalize-space(//*[@id='__layout']/div/main/article/section/div/div[1]/div[1]/h6/span[3])").get(),
            "Address":adr_lst[0]+", "+ adr_lst[1],
            "Office Name":response.selector.xpath("normalize-space(//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/h4/a/text())").get(),
            "Zip": str(zip_cd),  
            "Phone 1": phone_dic.get("phone 0"),
            "Phone 2": phone_dic.get("phone 1"),
            "Phone 3": phone_dic.get("phone 2"),
            "Languages " : language,
            "Designations " : response.selector.xpath("normalize-space(//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[1]/div/div[2]/div/div[2]/p/text())").get(),
            "Specialties " : spec_o ,
            "Agent Website " : response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/a/@href").get(),
            "Linkedin " : response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/a[@aria-label='RE/MAX on LINKEDIN']/@href").get(),
            "Facebook " : response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/a[@aria-label='RE/MAX on FACEBOOK']/@href").get(),
            "Twitter " : response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/a[@aria-label='RE/MAX on TWITTER']/@href").get(),
            "Instagram " : response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/a[@aria-label='RE/MAX on INSTAGRAM']/@href").get(),
            "Youtube " : response.selector.xpath("//*[@id='__layout']/div/main/article/section/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div/a[@aria-label='RE/MAX on YOUTUBE']/@href").get(),
            "About " : a[0],

        }



