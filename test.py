# from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapy import Selector
from selenium import webdriver
# from shutil import which
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
options = webdriver.ChromeOptions()
options.add_experimental_option("detach",True)
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options,service= Service(ChromeDriverManager().install()))
driver.maximize_window()
zip_codes = ["80237","55125","11428","20016","92604"]
url_lst =[]
    # for zip_code in zip_codes:
# url = "https://www.remax.com/api-v2/listings/autocomplete/?autocompleteValue=80237&categories%5B0%5D=states&categories%5B1%5D=places&categories%5B2%5D=zips"
# a = requests.get(url).json()
# print(a)
driver.get("https://www.remax.com/real-estate-agents/denver-co")
driver.find_element(By.XPATH,"//*[@id='__layout']/div/main/div/section[1]/div[2]/div/div[1]/button[4]").click()
# srch_box = driver.find_element(By.XPATH,"//*[@id='__layout']/div/main/div/section[1]/div[2]/div/div[2]/div/div/div/label/input")
# driver.implicitly_wait(2)
# srch_box.send_keys("80237")
# srch_box.click()
# driver.find_element(By.XPATH,"//button[@class='search-button dbutton dbutton-remax']").click()
# url = driver.current_url
# url_lst.append(url)
# //*[@id="__layout"]/div/main/div/section[1]/div[2]/div/div[2]/div/div/div/label/input
driver.find_element(By.XPATH,"//*[@id='__layout']/div/main/div/form/div[2]/div/div[2]/div/div[4]/svg").click()


# ?filters={"page":3,"count":24,"sortKey":{"random":"h8jehdpW"}}
# ?filters={"page":4,"count":24,"sortKey":{"random":"h8jehdpW"}}
# ?filters={"page":1,"count":24,"sortKey":{"random":"h8jehdpW"}}