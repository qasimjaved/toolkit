from selenium import webdriver
from selenium.webdriver import Chrome as chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from toolkit.logger import logger


class SeleniumHandler:
    DEFAULT_TIMEOUT = 0
    CLICKABLE_TIMEOUT = 5

    def __init__(self):
        """
        Initializes the SeleniumHandler and launches the Chrome WebDriver instance.
        """
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def login(self, email: str, password: str, email_input_xpaths: tuple, password_input_xpaths: tuple, login_button_xpaths: tuple) -> None:
        """
        Logs into a website using the provided email and password. The XPaths for the email, password, and login button
        must be provided to locate the corresponding elements.

        :param email: The email address to log in with.
        :param password: The password to log in with.
        :param email_input_xpaths: A tuple of XPaths to locate the email input field.
        :param password_input_xpaths: A tuple of XPaths to locate the password input field.
        :param login_button_xpaths: A tuple of XPaths to locate the login button.
        :return: None
        """
        email_input = self.find_element(email_input_xpaths)
        password_input = self.find_element(password_input_xpaths)
        login_button = self.find_clickable_element(login_button_xpaths)

        if email_input:
            email_input.send_keys(email)
        if password_input:
            password_input.send_keys(password)
        if login_button:
            login_button.click()


    def scroll_down(self) -> None:
        """
        Scrolls down to the bottom of the page using the WebDriver instance.

        :return: None
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_up(self, limit: int = 10) -> None:
        """
        Scrolls up the page by a specified number of iterations.

        :param limit: Number of iterations to scroll up (default is 10).
        :return: None
        """
        for _ in range(limit):
            self.driver.execute_script("scrollBy(0,-500);")

    def find_elements_per_xpath(self, xpath: str, timeout: int = DEFAULT_TIMEOUT) -> list:
        """
        Finds all elements that match a given XPath. If a timeout is provided, it waits until elements are located.

        :param xpath: The XPath string to find the elements.
        :param timeout: Time in seconds to wait for the elements to appear (default is 0, meaning no wait).
        :return: A list of WebElements matching the XPath. Returns an empty list if no elements are found or timeout occurs.
        """
        try:
            if timeout:
                elements = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath))
                )
            else:
                elements = self.driver.find_elements(by=By.XPATH, value=xpath)
            return elements
        except Exception as e:
            print(f"Error while finding elements: {e}")
            return []

    def find_elements(self, xpaths: tuple, timeout: int = DEFAULT_TIMEOUT) -> list:
        """
        Finds elements that match any of the given XPaths and returns the first match.

        :param xpaths: A list of XPath strings to find the elements.
        :param timeout: Time in seconds to wait for the elements to appear (default is 0, meaning no wait).
        :return: A list of WebElements for the first matching XPath. Returns an empty list if no elements are found.
        """
        for xpath in xpaths:
            elements = self.find_elements_per_xpath(xpath, timeout=timeout)
            if elements:
                return elements
        return []

    def find_element(self, xpaths: tuple, timeout: int = DEFAULT_TIMEOUT) -> webdriver.remote.webelement.WebElement:
        """
        Finds a single element that matches any of the given XPaths and returns the first match.

        :param xpaths: A list of XPath strings to find the element.
        :param timeout: Time in seconds to wait for the element to appear (default is 0, meaning no wait).
        :return: The first WebElement found that matches any of the XPaths. Returns None if no elements are found.
        """
        elements = self.find_elements(xpaths, timeout)
        if elements:
            return elements[0]
        return None

    def find_clickable_element_per_xpath(self, xpath: str, timeout: int = 5) -> webdriver.remote.webelement.WebElement:
        """
        Finds a clickable element matching the given XPath, waiting up to a specified timeout.

        :param xpath: The XPath string to find the clickable element.
        :param timeout: Time in seconds to wait for the element to become clickable (default is 5).
        :return: The WebElement found that is clickable. Returns None if no element is found within the timeout.
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            return element
        except Exception as e:
            print(f"Error while finding clickable element: {e}")
            return None

    def find_clickable_element(self, xpaths: tuple, timeout: int = CLICKABLE_TIMEOUT) -> webdriver.remote.webelement.WebElement:
        """
        Finds a clickable element matching any of the given XPaths, waiting up to a specified timeout.

        :param xpaths: A list of XPath strings to find the clickable element.
        :param timeout: Time in seconds to wait for the element to become clickable (default is 5).
        :return: The first clickable WebElement found. Returns None if no clickable element is found within the timeout.
        """
        for xpath in xpaths:
            element = self.find_clickable_element_per_xpath(xpath, timeout=timeout)
            if element:
                return element
        return None

    def click(self, xpaths: tuple, timeout: int = CLICKABLE_TIMEOUT) -> bool:
        """
        Finds a clickable element matching any of the given XPaths, waiting up to a specified timeout.
        Then clicks on the element.

        :param xpaths: A list of XPath strings to find the clickable element.
        :param timeout: Time in seconds to wait for the element to become clickable (default is 5).
        :return: True if the element was found and clicked, False otherwise.

        """
        element = self.find_clickable_element(xpaths, timeout)
        if element:
            logger.info("Clickable element found")
            element.click()
            return True
        logger.info("Element not found or not clickable")
        return False

    def find_attributes(self, xpaths: tuple, attribute: str, timeout: int = DEFAULT_TIMEOUT) -> list:
        """
        Finds elements matching any of the given XPaths and retrieves the specified attribute for each element.

        :param xpaths: A list of XPath strings to find the elements.
        :param attribute: The attribute name to retrieve from each found element.
        :param timeout: Time in seconds to wait for the elements to appear (default is 0, meaning no wait).
        :return: A list of attribute values for the found elements. Returns an empty list if no elements are found.
        """
        elements = self.find_elements(xpaths, timeout)
        return [element.get_attribute(attribute) for element in elements if element.get_attribute(attribute)]

    def find_attribute(self, xpaths: tuple, attribute: str, timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        Finds a single element matching any of the given XPaths and retrieves the specified attribute.

        :param xpaths: A list of XPath strings to find the element.
        :param attribute: The attribute name to retrieve from the found element.
        :param timeout: Time in seconds to wait for the element to appear (default is 0, meaning no wait).
        :return: The attribute value of the first matching element. Returns None if no element is found or attribute is missing.
        """
        elements = self.find_elements(xpaths, timeout)
        for element in elements:
            attr = element.get_attribute(attribute)
            if attr:
                return attr
        return None

    def find_all_text(self, xpaths: tuple, timeout: int = DEFAULT_TIMEOUT) -> list:
        """
        Finds all elements matching any of the given XPaths and retrieves the visible text for each element.

        :param xpaths: A list of XPath strings to find the elements.
        :param timeout: Time in seconds to wait for the elements to appear (default is 0, meaning no wait).
        :return: A list of visible text values for the found elements. Returns an empty list if no elements are found.
        """
        elements = self.find_elements(xpaths, timeout)
        return [element.text for element in elements if element.text]

    def find_text(self, xpaths: tuple, timeout: int = DEFAULT_TIMEOUT) -> str:
        """
        Finds a single element matching any of the given XPaths and retrieves the visible text.

        :param xpaths: A list of XPath strings to find the element.
        :param timeout: Time in seconds to wait for the element to appear (default is 0, meaning no wait).
        :return: The visible text of the first matching element. Returns None if no elements are found or have no text.
        """
        elements = self.find_elements(xpaths, timeout)
        for element in elements:
            if element.text:
                return element.text
        return None

    def quit_browser(self) -> None:
        """
        Closes the browser and quits the WebDriver session.

        :return: None
        """
        self.driver.quit()
