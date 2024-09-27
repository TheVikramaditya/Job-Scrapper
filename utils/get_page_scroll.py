
import time
import traceback







def func_page_scroll(driver):
    try:
        # Scroll until all results are loaded
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the page to load

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # break  # Break the loop if no more content is loaded
                return True
            last_height = new_height
            
    except Exception as e:
        print(f"{str(e)}")
        traceback.print_exc() 