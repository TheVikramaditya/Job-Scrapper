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

from utils.get_job_content import func_get_job_content
from utils.get_career_urls import *
from utils.get_excel import save_jobs_to_excel
from utils.send_email import func_send_email

current_directory = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_directory, '..', 'data')


setup = WebDriverSetup(cookie_setting=2,is_headless_mode=False)
driver = setup.initialize_driver()





def func_job_extractor():
    try:
        file_path = os.path.join(data_dir,'career_urls.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        # career_urls = data
        career_urls = [
                        {"company_name": "Ironcladapp", "links": {"career_url": "http://ironcladapp.com/careers/", "job_link": "http://ironcladapp.com/careers/#open-positions"}},
                       {"company_name": "Deel", "links": {"career_url": "https://www.deel.com/careers", "job_link": "https://jobs.ashbyhq.com/Deel?__hstc=29278755.0bc99ea862854c6413f505f4052d70e3.1727383892142.1727383892142.1727383892142.1&__hssc=29278755.1.1727383892142&__hsfp=3042269464"}},
                       {"company_name": "Amplitude", "links": {"career_url": "http://amplitude.com/careers", "job_link": "https://boards.greenhouse.io/amplitude"}},
                       {"company_name": "Careers", "links": {"career_url": "https://careers.snapeda.com/", "job_link": "https://careers.snapeda.com/#jobs-82f4bd1f"}}
                       ]
        # career_urls = [{"company_name": "Flocksafety", "links": {"career_url": "http://flocksafety.com/careers", "job_link": "http://flocksafety.com/careers/#ashby_embed"}},
        #     {"company_name": "Odeko", "links": {"career_url": "https://odeko.com/pages/careers", "job_link": "https://boards.greenhouse.io/odeko"}},
        #     {"company_name": "Amplitude", "links": {"career_url": "http://amplitude.com/careers", "job_link": "https://boards.greenhouse.io/amplitude"}},
        #                {"company_name": "Faire", "links": {"career_url": "http://faire.com/careers", "job_link": "http://faire.com/careers/openings"}},
        #                {"company_name": "Deel", "links": {"career_url": "https://www.deel.com/careers", "job_link": "https://jobs.ashbyhq.com/Deel?__hstc=29278755.0bc99ea862854c6413f505f4052d70e3.1727383892142.1727383892142.1727383892142.1&__hssc=29278755.1.1727383892142&__hsfp=3042269464"}}
        #             ]
        
        if career_urls:
            all_jobs = []
            for item in career_urls:
                company_name = item["company_name"]
                job_page_url = item["links"]["job_link"] 
                print(f"company name === {company_name}============")
                get_job_content = func_get_job_content(driver,job_page_url)
                if get_job_content:
                    all_jobs.append({"company_name":company_name,"jobs":get_job_content})
                    
        if all_jobs:
            create_excel = save_jobs_to_excel(all_jobs)
            if create_excel:
                file_path = os.path.join(data_dir, 'jobs_output.xlsx')
                res = func_send_email(file_path)
                
            
    except Exception as e:
        print(f"{str(e)}")
        traceback.print_exc() 
    finally:
        driver.quit() 
        
func_job_extractor()