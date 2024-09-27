
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import traceback
from bs4 import BeautifulSoup
from utils.get_page_scroll import func_page_scroll
import re






def check_verification(soup):
    # Check for common verification indicators, e.g., CAPTCHA or modal
    verification_keywords = ['captcha', 'verification', 'please confirm', 'age verification']
    for keyword in verification_keywords:
        if soup.text.lower().find(keyword) != -1:
            return True
    return False


def func_find_career_link(soup):
    try:
        potential_keywords = ['careers', 'jobs', 'join-us', 'work-with-us', 'employment', 'opportunities','career']

        for keyword in potential_keywords:
            link = soup.find('a', href=True, text=lambda x: x and keyword.lower() in x.lower())
            if link:
                return link['href']

        return None
    
    except Exception as e:
        print(f"error from find_career_page ,{str(e)}")
        



def func_navigating_career_link(driver, career_url):
    try:
        driver.get(career_url)
        # WebDriverWait(driver, 30).until(
        #     EC.presence_of_element_located((By.TAG_NAME, 'body'))  # Adjust selector as needed
        # )
        is_scrolled = func_page_scroll(driver)
        
        if is_scrolled:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            keywords = ['view Jobs', 'view opening', 'explore jobs', 'job opportunities', "openings", "open positions","see opportunities"]
           

            for keyword in keywords:
                for link in soup.find_all('a', string=re.compile(keyword, re.IGNORECASE)):
                    job_link = link["href"]
                    # Initialize the full_job_link variable
                    full_job_link = ""

                    if not job_link.startswith(('http://', 'https://')):
                        # Extract base URL
                        match = re.search(r'https?://[^/]+', career_url)
                        if match:
                            base_url = match.group(0)  # Get base URL
                        else:
                            base_url = career_url.rstrip('/')
                        
                        remaining_path = career_url[len(base_url):].strip('/')
                        path_segments = remaining_path.split('/') if remaining_path else []
                        job_link_cleaned = job_link.lstrip('/')
                        
                        if any(segment in job_link_cleaned for segment in path_segments):
                            full_job_link = base_url + '/' + job_link_cleaned
                        else:
                            full_job_link = career_url.rstrip('/') + '/' + job_link_cleaned
                            
                        # Remove duplicate slashes if necessary
                        full_job_link = re.sub(r'(?<!:)//+', '/', full_job_link)
                        
                    else:
                        full_job_link = job_link  # Already a full URL

                    # Create the job entry
                    job_entry = {"career_url": career_url, "job_link": full_job_link}
                    
                            
                    return job_entry
                    
            
            # return job_entries  # Return all job entries found
        else:
            return None  # Return None if the page didn't scroll successfully

    # except TimeoutException:
    #         print(f"Timeout occurred while trying to access {career_url}.")
    #         driver.quit()  # Ensure the driver is closed
    #         return None  # Return None in case of a timeout

    # except WebDriverException as wd_ex:
    #     print(f"WebDriver error occurred: {str(wd_ex)}")
    #     driver.quit()  # Ensure the driver is closed
    #     return None  # Return None in case of a WebDriver error


    except Exception as e:
        print(f"Error in navigating_career_link {career_url}: {str(e)}")
        return None  # Return None in case of an error







def func_scrap_company_page(driver,company_url):
    try:
        driver.get(company_url)
        # func_handle_cookie_consent(driver)
        is_scrolled = func_page_scroll(driver)
        if is_scrolled:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            if check_verification(soup):
                print(f"Verification required for {company_url}. Skipping...")
                return None

            career_url= func_find_career_link(soup)
            
            return career_url
        return 
    
    except Exception as e:
        print(f"error from scrap_career_page ,{str(e)}")
        traceback.print_exc() 
        return None