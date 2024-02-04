from undetected_chromedriver import Chrome
from selenium.webdriver import ChromeOptions

class Driver():
    
    def __init__(self):
        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        # options.add_argument("--headless")
        user_agent = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        options.add_argument(f'--user-agent={user_agent}')
        self.driver = Chrome(options=options)
        
        self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")