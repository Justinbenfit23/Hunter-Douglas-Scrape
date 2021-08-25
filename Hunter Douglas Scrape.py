from os import link, name
from numpy.testing._private.utils import IgnoreException
from pandas.core import base
from pandas.core.arrays.categorical import contains
from requests.api import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import html5lib
import requests
import pandas as pd
from pandas import *
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, TimeoutException, StaleElementReferenceException, WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time
import re
from selenium.webdriver.chrome.options import Options
from pprint import PrettyPrinter
import csv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from openpyxl import workbook
from selenium.webdriver.common.keys import Keys

chrome_driver_path = '/Users/justinbenfit/Desktop/Python/chromedriver'
options = Options()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')
options.add_argument("--start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options = options, executable_path=chrome_driver_path)

with open('/Users/justinbenfit/.Trash/California Cities.csv', newline='\n') as f:
    reader = csv.reader(f)
    data = [k[0] for k in reader]

cities = ['San Ramon']#,'Portland']
test_links = ['http://www.creativeshades.net/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator', 'https://maps.google.com/?q=Creative%20Shades%20%26%20Cabinetry+12893%20Alcosta%20Blvd+San%20Ramon+CA+94583-1450&ll=37.779071612722,-121.96313072985', 'http://www.homesiteservices.hdwfdealer.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator', 'https://maps.google.com/?q=Homesite%20Services+2001%20Crow%20Canyon%20Rd+San%20Ramon+CA+94583-5388&ll=37.77259,-121.99403', 'http://www.firstchoicewindowcoverings.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator', 'https://maps.google.com/?q=Floortex%20Design%20-%20First%20Choice%20Abbey%20Carpet+101%20Town%20And%20Country%20Dr+Danville+CA+94526-3968&ll=37.8147206,-121.9980944', 'http://www.worleyshome.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator', 'https://maps.google.com/?q=Worley%27s%20Home%20Design%20Center+2751%20Castro%20Valley%20Blvd+Castro%20Valley+CA+94546-5411&ll=37.694616699299,-122.0855219409', 'http://www.carpetoneoakland.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator', 'https://maps.google.com/?q=Dick%27s%20Carpet%20One+36%20Hegenberger%20Ct+Oakland+CA+94621-1322&ll=37.736490344368,-122.19460671621', 'http://www.signaturec1.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator''http://www.parkplacedesignws.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator','http://www.havensfbay.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator','http://www.parkplacedesignws.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator','https://www.blindsonashoestring.hdwfdealer.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator','https://www.windowology-eastbay.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator','https://www.worleyshome.com/?utm_source=Hunter+Douglas&utm_medium=Locator&utm_campaign=Locator']
base_url = "https://www.hunterdouglas.com/locator"
driver.get(base_url)
contact_info = []


def pop_up_one(driver):
    try:
        submit_btn = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"[aria-label='No, I am not a California resident']")))
        submit_btn.click()
        url = driver.current_url
        submit_btn = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[aria-label="Close"]')))
        if(submit_btn):
            submit_btn[0].click()
    except Exception as t:
        url = driver.current_url
        print(t,f"Either no second pop_up or something else went wrong in {url} pop_up_one function")
        return url
    else:
        url = driver.current_url
        print("second pop_up clicked")
        return url 

def pop_up_back(driver):
    try: 
        close_button = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Close"]')))
    except TimeoutException:
        pass
    else:
        close_button.click()
#pop_up_one(base_url)
def submit(url,driver,c):
    try:
        text_box = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, "//input[@id='zip']")))
        text_box[0].click()
        text_box[0].send_keys(c)
        submit_btn = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//button[text()="Submit" and @class="full-width white-button button"]')))
    except Exception as t:
        print(t,f"Somewhere in {url} entered except block of submit function")
        try:
            element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'a[aria-label="Home"]')))
            driver.execute_script("return arguments[0].scrollIntoView(false);", element)
            text_box[0].click()
            text_box[0].clear()
            text_box[0].click()
            text_box[0].send_keys(c)  
            search_btn = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//button[text()="SEARCH"]')))
            search_btn[0].click()  
            select = Select(WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//div//select[@id='show-within']"))))
            time.sleep(3)
            selectLen = len(select.options)
        except Exception:
            element = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]')))
            driver.execute_script("return arguments[0].scrollIntoView(false);", element)
            element = WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'a[aria-label="Home"]')))
            driver.execute_script("return arguments[0].scrollIntoView(false);", element)
            text_box[0].click()
            text_box[0].clear()
            text_box[0].click()
            text_box[0].send_keys(c)  
            search_btn = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//button[text()="SEARCH"]')))
            search_btn[0].click()
        else:
            select.select_by_index(selectLen-1)


    else:   
        submit_btn[0].click()
        WebDriverWait(driver,5).until(EC.url_changes(url))
        select = Select(WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,"//div//select[@id='show-within']"))))
        selectLen = len(select.options)
        select.select_by_index(selectLen-1)   
        

def get_links(page,links_list):
    for p in page:
        for l in WebDriverWait(p,5).until(EC.presence_of_all_elements_located((By.TAG_NAME,"a"))):
            link = l.get_attribute('href')
            if link != None:
                link_split = link.split('\n')
                for l in link_split:
                    if "http" in link:
                        links_list.append(link)
    

def get_contact_info(link):
    if "maps.google.com" not in link:
        try:
            driver.get(link) #figure out why it's clicking to google maps
            about_us = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a[aria-label="About Us"]')))
            if about_us:
                about_us.click()
        except WebDriverException as w:
            print(w)
        else:
            get_data(driver)
    else:
        return

def get_data(link):
    link = driver.current_url
    teaser = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="body-copy cmp-teaser__description"]')))
    reviews = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gy-reviews__body"]')))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    company = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="cmp-footer__dealer-name cmp-footer__dealer-name--text"]')))
    address = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="cmp-footer__dealer-address cmp-footer__dealer-address--text"]')))
    phone = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//div[@class="cmp-footer__dealer-phone"]')))
    for r in reviews:
        lst = []
        lst.append(r.text)
    description =f"{lst[0]} {teaser.text}"    

    if '\n' in address.text:
        city = (list((address.text).split())[-3]).replace(",","")
        state = list((address.text).split())[-2]
        zip = list((address.text).split())[-1]
        street = address.text.split('\n')[0]
        my_dict = {"Name":"Unknown","Company":company.text,"Phone":phone.text,"Street":street,"City":city,"State":state,"Zip/Postal Code":zip,"Website":link,"Description": description,"Lead Source": "Direct", "Vertical": "Home Services",
                  "Sub-Vertical": "Interiors", "Acquisition Source": "Sales Ops Scrape", "Country": "United States"}
    
    else:
        city = (list((address.text).split())[-3]).replace(",","")
        state = list((address.text).split())[-2]
        zip = list((address.text).split())[-1]
        my_dict = {"Name":"Unknown","Company":company.text,"Phone":phone.text,"Street":None,"City":city,"State":state,"Zip/Postal Code":zip,"Website":link,"Description": description,"Lead Source": "Direct", "Vertical": "Home Services",
                  "Sub-Vertical": "Interiors", "Acquisition Source": "Sales Ops Scrape", "Country": "United States"}

    contact_info.append(my_dict)

def master_function(driver,cities):
    links_list = []
    for c in cities:
        url = pop_up_one(driver)
        submit(url,driver,c)
        loop = True
        while loop:
            try:
                current_url = driver.current_url
                next_btn = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]')))
                actions = ActionChains(driver)
                actions.move_to_element(next_btn).perform()
                if next_btn:
                    next_btn.click()
            except TimeoutException:
                current_url = driver.current_url
                print(f"somewhere in {current_url} while loop")
                #driver.back()
                #pop_up_back(driver)
                #driver.back()
                break    
            else:
                page = WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="loc-results"]')))
                get_links(page,links_list)
    return links_list

def to_excel(contact_list):
    df = pd.DataFrame(contact_list, columns=["Name", "Phone", "Website", "City", "Street", "Description", "State", "Company",
                                             "Lead Source", "Vertical", "Sub-Vertical", "Acquisition Source", "Country"])
    with ExcelWriter("Hunter_Douglas.xlsx") as writer:
        df.to_excel(writer)

def master_data_function(driver):
    links_list = master_function(driver,data)
    #print(links_list)
    time.sleep(3)
    for l in links_list:
        try: 
            get_contact_info(l)
        except WebDriverException:
            print(f"Connection Timed Out for {l}")
            continue
        else:
            pass
        finally:
            to_excel(contact_info)
            if l == test_links[-1]:
                driver.quit()
                                       
master_data_function(driver)
driver.quit()
#print(contact_info)
#print(test_list)
#print(links_list)



