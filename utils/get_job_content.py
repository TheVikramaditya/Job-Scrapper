



from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import traceback
from collections import Counter
from bs4 import BeautifulSoup

from utils.get_page_scroll import func_page_scroll
from utils.send_email import func_send_email

import re




def func_get_job_content_details_backup(driver,soup,most_common_class):
    try:
        obj =[]
        print(f"checking for  job content ")
        print(most_common_class)
        links = soup.find_all('div', class_=most_common_class)
        
        for idx, link in enumerate(links):
            # print(link)
            link_text = link.get_text(strip=True)  # Get the text inside the <a> tag, stripping extra whitespace
            # link_href = link['href']  # Get the href attribute
            # print(f"Link {idx + 1}:")
            print(f"Text: {link_text}")
            # print(f"Href: {link_href}")
            if 'remote' in link_text.lower() or 'anywhere' in link_text.lower():
                obj.append(link_text)
            
        return obj
        # res = func_send_email('\n'.join(obj)) 
    except Exception as e:
        print(f"{str(e)}")
        traceback.print_exc()
        return 



def extract_base_url(url):
    """
    Extract the base URL till '.com' or similar domain suffix.
    """
    match = re.match(r'(https?://[^/]+)', url)
    return match.group(1) if match else None





def is_remote(job_text,div_text=None):
    """
    Checks if the job_text contains 'remote' or 'anywhere'.
    Returns True if found, otherwise False.
    """
    if div_text is not None and ('remote' in div_text.lower() or 'anywhere' in div_text.lower()):
        return True
    return 'remote' in job_text.lower() or 'anywhere' in job_text.lower()




def func_get_job_content_details(driver, soup, most_common_class, base_url=None):
    try:
        obj = []
        print("Checking for job content...")
        
        # Find all <div> elements with the given class
        divs = soup.find_all('div', class_=most_common_class)
        
        if not divs:
            print(f"No <div> elements found with class: {most_common_class}")
        
        for idx, div in enumerate(divs):
            div_text = div.get_text(strip=True)  # Get the text inside the <div> tag
            print(f"Div {idx + 1}: Text: {div_text}")
            
            # Initialize link variable
            link = None
            job_text = None

            # Check if the <div> has any <a> tags inside it (child)
            a_tags_in_div = div.find_all('a', href=True)
            for a_tag in a_tags_in_div:
                a_text = a_tag.get_text(strip=True)
                a_href = a_tag['href']
                
                # Save the job text and link (for potential appending later)
                print(f"atext ==== {a_text}")
                if not any(phrase in a_text.lower() for phrase in ["more", "view job"]):
                    job_text = a_text
                    link = a_href

            # If there's no <a> inside the <div>, check for sibling or parent
            if not link:
                # Check if there's an <a> tag as a sibling of the <div>
                sibling_a_tag = div.find_next_sibling('a', href=True)
                if sibling_a_tag:
                    sibling_a_text = sibling_a_tag.get_text(strip=True)
                    sibling_a_href = sibling_a_tag['href']
                    
                    job_text = sibling_a_text
                    link = sibling_a_href

            # If still no link, check if <div> is inside an <a> tag (parent)
            if not link:
                parent_a_tag = div.find_parent('a', href=True)
                if parent_a_tag:
                    parent_a_text = parent_a_tag.get_text(strip=True)
                    parent_a_href = parent_a_tag['href']
                    
                    job_text = parent_a_text
                    link = parent_a_href

            # Check if link is relative (i.e., doesn't start with http/https)
            if link and not link.startswith('http'):
                # If base_url is not provided, get it from the current page URL (driver.current_url)
                base_url_to_use = base_url or extract_base_url(driver.current_url)
                
                # Add the relative link to the base URL
                if base_url_to_use:
                    link = base_url_to_use + link
            
            # Final check to see if 'remote' or 'anywhere' is in the job text
            if is_remote(job_text,div_text):
                truncated_job_text = job_text[:50] + '...' if len(job_text) > 50 else job_text
                obj.append({"job": truncated_job_text, "link": link})

        # Convert each dictionary in obj to a string for sending via email
        # email_content = '\n'.join([f"Job: {entry['job']}, Link: {entry['link']}" for entry in obj])
        
        # Send the email (assuming func_send_email is your email function)
        # res = func_send_email(email_content)
        
        return obj
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return []



def func_check_with_select_tag(soup,select_element,all_div):
    try:
        
        # Get the parent div of this select element
        parent_div = select_element.find_parent('div')
        print(select_element['class'])
        if parent_div.has_attr('class'):
            print("Parent div class:", parent_div['class'])
        else:
            print("Parent div has no class.")
        
        for sibling in parent_div.find_all_next('div'):
            # print(f"Found following div with class: {sibling.get('class')}")
            if sibling.get('class') is not None:
                sibling_text = sibling.get_text(strip=True)
                if is_remote(sibling_text):
                    all_div = all_div + sibling.get('class')

        if all_div:
            return all_div
            
            # return {"most_frequent_class":most_frequent_class,"soup":soup,"driver":driver}
        else:
            print("No classes found in following divs.")
            return None

    except Exception as e:
        pass
    




def func_check_with_open_position_divs(soup,open_position_divs, all_div):
    try:
        for open_position in open_position_divs:
            # Print class names of the current open position div
            print("Open position div class:", open_position.get('class'))
            
            # Iterate through all following sibling divs
            for sibling in open_position.find_all_next('div'):
                if sibling.get('class') is not None:
                    sibling_text = sibling.get_text(strip=True)
                    if is_remote(sibling_text):  # Check if the job is remote
                        all_div.extend(sibling.get('class'))  # Append classes to all_div

        if all_div:
            return all_div
        else:
            print("No classes found in following divs.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None





def func_get_job_content(driver,url):
    try:
        driver.get(url)
        is_scrolled = func_page_scroll(driver)

        if is_scrolled:
            
            # time.sleep(2)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            select_element = soup.find(lambda tag: tag.name in ['select', 'input'] and 
                                (re.search(r'department', tag.get('name', ''), re.IGNORECASE) or 
                                 re.search(r'department', tag.get('id', ''), re.IGNORECASE)))
            
            open_position_divs = soup.find_all(lambda tag: tag.name == 'div' and 
                                         re.search(r'open positions|available jobs|job openings', tag.text, re.IGNORECASE))

            all_div = []
            if select_element:
                all_div +=  func_check_with_select_tag(soup,select_element,all_div)
                
                
            if open_position_divs:
                all_div += func_check_with_open_position_divs(soup,open_position_divs,all_div)
                
                
                
            print(all_div)
            if all_div:  # Check if the list is not empty
                class_counts = Counter(all_div)  # Count occurrences of each class
                most_frequent_class = class_counts.most_common(1)[0][0]  # Get the most frequent class
                print("Most frequent class name in all_div:", most_frequent_class)
                # return most_frequent_class
            
            is_content = func_get_job_content_details(driver,soup,most_frequent_class)
            print(f"is content ======= {is_content}")
            if is_content:
                return is_content
                
                
            
    except Exception as e:
        print(f"{str(e)}")
        traceback.print_exc()