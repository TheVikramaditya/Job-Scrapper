import time
import re
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import os
import json

from operations.webdriver_setup import WebDriverSetup

from utils.get_company_name_by_url import func_get_company_name
from utils.get_career_urls import *

current_directory = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_directory, '..', 'data')


setup = WebDriverSetup(cookie_setting=2)
driver = setup.initialize_driver()
# driver.set_page_load_timeout(20) 





def func_career_url_extractor():
    try:
        career_url_list = []
        job_links = []
        file_path = os.path.join(data_dir,'company_urls.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        company_urls = data.get('company_urls', [])
        
        if company_urls:
            # print(company_urls)
            for company_url in company_urls:
                
                career_url = func_scrap_company_page(driver,company_url)
                if career_url:
                    print(career_url)
                    if not career_url.startswith(('http://', 'https://')):
                        career_url = company_url+career_url
                    career_url_list.append(career_url)
                    print(career_url_list)
        
        if career_url_list:
            for career_url in career_url_list:
                company_name = func_get_company_name(career_url)
                get_job_obj = func_navigating_career_link(driver,career_url)
                if get_job_obj:
                    job_links.append({"company_name":company_name,"links":get_job_obj})
                    # print(job_links)
        if job_links:
            return job_links

            
    except Exception as e:
        print(f"{str(e)}")
        traceback.print_exc() 
    finally:
        driver.quit() 
        
list_careers = func_career_url_extractor()

if list_careers:
    file_path = os.path.join(data_dir,'career_urls.json')
    json_data = list_careers
    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file)
    print("successful ! the file is in data folder")