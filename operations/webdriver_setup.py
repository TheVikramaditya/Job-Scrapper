from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options





class WebDriverSetup:
    def __init__(self, cookie_setting=1,is_headless_mode=True):  # Default to block third-party cookies (1)
        
        self.cookie_setting = cookie_setting
        self.is_headless_mode = is_headless_mode

    def initialize_driver(self):
        chrome_options = Options()
        print( self.cookie_setting , self.is_headless_mode)
        chrome_options.add_argument("--disable-notifications")  # Disable notifications
        chrome_options.add_argument("--disable-infobars")       # Disable infobars
        chrome_options.add_argument("--disable-popup-blocking") # Disable pop-up blocking
        chrome_options.add_argument("--incognito")              # Start in incognito mode
        chrome_options.add_argument("--disable-extensions") 
        if self.is_headless_mode:
            chrome_options.add_argument("--headless")                # Enable headless mode
            chrome_options.add_argument("--window-size=1920x1080")
        # Enable logging for debugging
        chrome_options.add_argument('--enable-logging')
        chrome_options.add_argument('--v=1')

        # Set cookie preferences dynamically based on the value passed when initializing the class
        chrome_options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.cookies": self.cookie_setting})

        # Setup WebDriver service
        service = Service('/usr/local/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Close any extra blank tabs
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
        
        return driver

# Function to initialize the WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-infobars")       # Disable infobars
    chrome_options.add_argument("--disable-popup-blocking") # Disable pop-up blocking
    chrome_options.add_argument("--incognito")              # Start in incognito mode
    chrome_options.add_argument("--disable-extensions") 
    

    # Enable logging for debugging
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--v=1')

    # Allow first-party cookies, block third-party cookies
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

    # Setup WebDriver service
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Close any extra blank tabs
    if len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[0])
        driver.close()
        driver.switch_to.window(driver.window_handles[1])
    
    return driver






# chrome_options = Options()
# chrome_options.add_argument("--disable-notifications")  # Disable notifications
# chrome_options.add_argument("--disable-infobars")       # Disable infobars
# chrome_options.add_argument("--disable-popup-blocking")  # Disable pop-up blocking
# chrome_options.add_argument("--incognito")               # Start in incognito mode
# chrome_options.add_argument("--disable-extensions") 

# chrome_options.add_argument('--enable-logging')
# chrome_options.add_argument('--v=1')

# chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 1})

# service = Service('/usr/local/bin/chromedriver')
# driver = webdriver.Chrome(service=service,options=chrome_options)
# # driver.set_page_load_timeout(30) 


# # Close any extra blank tabs
# if len(driver.window_handles) > 1:
#     driver.switch_to.window(driver.window_handles[0])
#     driver.close()
#     driver.switch_to.window(driver.window_handles[1]) 