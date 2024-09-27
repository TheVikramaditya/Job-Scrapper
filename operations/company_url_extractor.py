import time
import re
import requests
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter

import os
import json

from operations.webdriver_setup import WebDriverSetup

from utils.get_company_urls import func_extract_website_url
from utils.get_page_scroll import func_page_scroll
from utils.get_most_common_class import func_extract_most_common_class

current_directory = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_directory, '..', 'data')


setup = WebDriverSetup(cookie_setting=1)
driver = setup.initialize_driver()

def func_company_url_extractor(main_url,param_url=""):
    try:
        
        driver.get(main_url+param_url)
        is_scrolled = func_page_scroll(driver)
        # is_scrolled = True
        if is_scrolled:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            result_div = soup.find('div', text=re.compile(r'showing \d+ of \d+|total results \d+| latest remote jobs', re.IGNORECASE))
            print(result_div)
            if result_div:
                parent_div = result_div.find_parent('div')
                if parent_div:
                    if parent_div.has_attr('class'):
                        print("Parent div class:", parent_div['class'])
                    else:
                        print("Parent div has no class.")
                        
                    # valid_href_pattern = re.compile(r'^\/[^?]*$')
                    
                    a_tags = parent_div.find_all('a',href=True)
                    total_results_text = result_div.get_text(strip=True)
                    # print(page_source[:100])
                    total_companies = int(re.search(r'\d+', total_results_text.split('of')[-1]).group())
            
                    most_common_class = func_extract_most_common_class(a_tags)
                    list_companies = func_extract_website_url(driver,soup,most_common_class,main_url)
                    print(len(list_companies))
                    return list_companies
                
                
    except Exception as e:
        print(f"Some Error {str(e)}")
        traceback.print_exc() 
        return None
    finally:
        driver.quit() 



main_url = "https://www.ycombinator.com"
param_url ="/companies?isHiring=true&regions=Remote"
# main_url = "https://wellfound.com"

# param_url = "/remote"
list_companies = func_company_url_extractor(main_url,param_url)

if list_companies:
    file_path = os.path.join(data_dir,'company_urls.json')
    json_data = {"company_urls": list_companies}
    with open(file_path, 'w') as json_file:
        json.dump(json_data, json_file)
else:
    print("No data found..")