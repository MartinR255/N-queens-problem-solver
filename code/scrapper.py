from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class LinkedInScrapper:

    def __init__(self) -> None:
        ...


    """
    Logs into LinkedIn using the provided credentials.

    Args:
        driver (webdriver): The Selenium WebDriver instance used to navigate the page.
        username (str): The LinkedIn username or email address.
        password (str): The LinkedIn password.
    
    Returns:
        None
    """
    def _linkedin_login(self, driver: webdriver, username: str, password: str) -> None:
        driver.get('https://www.linkedin.com/login')

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        ).send_keys(username)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'password'))
        ).send_keys(password)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]'))
        ).click()

        time.sleep(5)
         

    """
    Scrapes content from a LinkedIn page given a URL and element class name to scrape.

    Args:
        driver (webdriver): The Selenium WebDriver instance used to navigate the page.
        url (str): The URL of the LinkedIn page to scrape.
        classname (str): The name of class to scrape from page.
    
    Returns:
        str: The HTML content of the div element with the specified class name.
    """
    def _scrape_linkedin_content(self, driver: webdriver, url: str, class_name: str) -> str:
        driver.get(url)
        time.sleep(5) 
        
        div_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))  # Replace with the actual class name
        )
        
        for div in div_elements:
            html_as_text = div.get_attribute('outerHTML')

        return html_as_text
    

    '''
    Extracts color numbers from the given text based on a specific pattern.

    Args: 
        text(str) : The text from which to extract color numbers.

    Returns:
        list[int]: List of numbers extracted from input text.
    '''
    def _grab_queen_color_numbers(self, text: str) -> list[int]:
        # cell-color-x is a part of queen element class and x is a color number 
        pattern = r'cell-color-(\d+)'

        matches = re.findall(pattern, text)

        numbers = [int(num) for num in matches]

        return numbers


    """
    Logs into LinkedIn, scrapes the content from a given URL, and extracts color numbers.

    Args:
        url (str): The URL of the LinkedIn page to scrape.
        username (str): The LinkedIn username or email address.
        password (str): The LinkedIn password.
        classname (str): The name of class to scrape from page.
    
    Returns:
        list[int]: A list of integers representing the extracted color numbers.
    """
    def scrape(self, url: str, username: str, password:str, class_name: str) -> list[int]:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=chrome_options)

        text = ''
        try:
            self._linkedin_login(driver, username, password)
            text = self._scrape_linkedin_content(driver, url, class_name)
        finally:
            driver.quit()

        return self._grab_queen_color_numbers(text)
        
