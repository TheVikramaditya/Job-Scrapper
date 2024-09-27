import time
import re
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup






def func_extract_website_url(driver,soup, most_common_class,main_url):
    try:
        links = soup.find_all('a', class_=most_common_class, href=True)
        # company_websites = []
        matching_urls = []
        for link in links[:50]:
            href = link['href']
            complete_url = main_url+ href 
            
            company_name = href.split("/")
            print(f"Navigating to: {complete_url} , {company_name}")
            
            # original_window = driver.current_window_handle 
            driver.get(complete_url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            page_source = driver.page_source
            
            if page_source:
                # url_pattern = re.compile(r'https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})(?<!/))')
                url_pattern = re.compile(r'https?://(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})(?<!/))')

                matches = url_pattern.findall(page_source)
                # print(matches)
                filtered_urls = set()
                for match in matches:
                    # Reassemble the full URL
                    full_url = f'http://{match}' if not match.startswith('http') else match
                    
                    if full_url.endswith(('.com', '.in','.org','.co')) and main_url not in full_url:
                        filtered_urls.add(full_url)

                # Convert to a list (if needed) and print results
                filtered_urls_list = list(filtered_urls)
                
                
                for url in filtered_urls_list:
                    url_domain = url.split("//")[-1].split("/")[0]
                    if url not in matching_urls:
                        for company in company_name:
                            if not company:
                                continue
                            # Check if company name is in the URL (case insensitive)
                            if '-' in company:
                                company_parts = company.split('-')
                                if any(part in url_domain for part in company_parts):
                                    matching_urls.append(url)
                            else:    
                                if company.lower() in url.lower():
                                    matching_urls.append(url) 
        return matching_urls       
            
    except Exception as e:
        print(f"Some Error {print(str(e))}")
        traceback.print_exc() 
        return None