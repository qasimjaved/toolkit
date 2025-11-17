from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException


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

    def find_elements_per_xpath(self, xpath: str, sub_element: WebElement = None, timeout: int = DEFAULT_TIMEOUT) -> list:
        """
        Finds all elements that match a given XPath. If a timeout is provided, it waits until elements are located.

        :param xpath: The XPath string to find the elements.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the elements to appear (default is 0, meaning no wait).
        :return: A list of WebElements matching the XPath. Returns an empty list if no elements are found or timeout occurs.
        """
        try:
            to_search_element = sub_element if sub_element else self.driver
            if timeout:
                elements = WebDriverWait(to_search_element, timeout).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath))
                )
            else:
                elements = to_search_element.find_elements(by=By.XPATH, value=xpath)
            return elements
        except TimeoutException:
            return []
        except Exception as e:
            logger.exception(f"Exception while finding elements: {e} for xpath ({xpath}) for URL: {self.driver.current_url}")
            return []

    def find_elements(self, xpaths: tuple, sub_element: WebElement = None , timeout: int = DEFAULT_TIMEOUT) -> list:
        """
        Finds elements that match any of the given XPaths and returns the first match.

        :param xpaths: A list of XPath strings to find the elements.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the elements to appear (default is 0, meaning no wait).
        :return: A list of WebElements for the first matching XPath. Returns an empty list if no elements are found.
        """
        for xpath in xpaths:
            elements = self.find_elements_per_xpath(xpath, sub_element=sub_element, timeout=timeout)
            if elements:
                return elements
        return []

    def find_element(self, xpaths: tuple, sub_element: WebElement = None, timeout: int = DEFAULT_TIMEOUT, index: int = 0) -> webdriver.remote.webelement.WebElement:
        """
        Finds a single element that matches any of the given XPaths and returns the element at the specified index.

        :param xpaths: A list of XPath strings to find the element.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the element to appear (default is 0, meaning no wait).
        :param index: Index of the element to return (default is 0, meaning first element).
        :return: The WebElement found at the specified index that matches any of the XPaths. Returns None if no elements are found or index is out of range.
        """
        elements = self.find_elements(xpaths, sub_element=sub_element, timeout=timeout)
        if elements and 0 <= index < len(elements):
            return elements[index]

    def find_clickable_element_per_xpath(self, xpath: str, sub_element: WebElement = None, timeout: int = 5) -> webdriver.remote.webelement.WebElement:
        """
        Finds a clickable element matching the given XPath, waiting up to a specified timeout.

        :param xpath: The XPath string to find the clickable element.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the element to become clickable (default is 5).
        :return: The WebElement found that is clickable. Returns None if no element is found within the timeout.
        """
        try:
            to_search_element = sub_element if sub_element else self.driver
            element = WebDriverWait(to_search_element, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            return element
        except TimeoutException:
            pass
        except Exception as e:
            logger.exception(f"Error while finding clickable element: {e}")

    def find_clickable_element(self, xpaths: tuple, sub_element: WebElement = None, timeout: int = CLICKABLE_TIMEOUT, index: int = 0) -> webdriver.remote.webelement.WebElement:
        """
        Finds clickable elements matching any of the given XPaths, waiting up to a specified timeout, and returns the element at the specified index.

        :param xpaths: A list of XPath strings to find the clickable element.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the element to become clickable (default is 5).
        :param index: Index of the clickable element to return (default is 0, meaning first element).
        :return: The clickable WebElement found at the specified index. Returns None if no clickable element is found within the timeout or index is out of range.
        """
        all_clickable_elements = []
        for xpath in xpaths:
            # First, wait for at least one clickable element to appear
            try:
                to_search_element = sub_element if sub_element else self.driver
                WebDriverWait(to_search_element, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
            except TimeoutException:
                continue
            
            # Now find all elements matching this xpath
            elements = self.find_elements_per_xpath(xpath, sub_element=sub_element, timeout=0)
            for element in elements:
                try:
                    # Check if element is displayed and enabled (basic clickability check)
                    if element.is_displayed() and element.is_enabled():
                        all_clickable_elements.append(element)
                except:
                    continue
            if all_clickable_elements:
                break
        
        if all_clickable_elements and 0 <= index < len(all_clickable_elements):
            return all_clickable_elements[index]

    def click(self, xpaths: tuple, sub_element: WebElement = None, timeout: int = CLICKABLE_TIMEOUT, index: int = 0) -> bool:
        """
        Finds a clickable element matching any of the given XPaths at the specified index, waiting up to a specified timeout.
        Then clicks on the element.

        :param xpaths: A list of XPath strings to find the clickable element.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the element to become clickable (default is 5).
        :param index: Index of the clickable element to click (default is 0, meaning first element).
        :return: True if the element was found and clicked, False otherwise.

        """
        element = self.find_clickable_element(xpaths, sub_element=sub_element, timeout=timeout, index=index)
        if element:
            logger.info("Clickable element found")
            element.click()
            return True
        logger.info("Element not found or not clickable")
        return False

    def find_attributes(self, xpaths: tuple, attribute: str = 'href', sub_element: WebElement = None, timeout: int = DEFAULT_TIMEOUT) -> list:
        """
        Finds elements matching any of the given XPaths and retrieves the specified attribute for each element.

        :param xpaths: A list of XPath strings to find the elements.
        :param attribute: The attribute name to retrieve from each found element.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the elements to appear (default is 0, meaning no wait).
        :return: A list of attribute values for the found elements. Returns an empty list if no elements are found.
        """
        elements = self.find_elements(xpaths, sub_element=sub_element, timeout=timeout)
        return [element.get_attribute(attribute) for element in elements if element.get_attribute(attribute)]

    def find_attribute(self, xpaths: tuple, attribute: str = 'href', sub_element: WebElement = None, timeout: int = DEFAULT_TIMEOUT, index: int = 0) -> str:
        """
        Finds a single element matching any of the given XPaths at the specified index and retrieves the specified attribute.

        :param xpaths: A list of XPath strings to find the element.
        :param attribute: The attribute name to retrieve from the found element.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the element to appear (default is 0, meaning no wait).
        :param index: Index of the element to get the attribute from (default is 0, meaning first element).
        :return: The attribute value of the element at the specified index. Returns None if no element is found, index is out of range, or attribute is missing.
        """
        elements = self.find_elements(xpaths, sub_element=sub_element, timeout=timeout)
        if elements and 0 <= index < len(elements):
            return elements[index].get_attribute(attribute)

    def find_all_text(self, xpaths: tuple, sub_element: WebElement = None, timeout: int = DEFAULT_TIMEOUT) -> list:
        """
        Finds all elements matching any of the given XPaths and retrieves the visible text for each element.

        :param xpaths: A list of XPath strings to find the elements.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the elements to appear (default is 0, meaning no wait).
        :return: A list of visible text values for the found elements. Returns an empty list if no elements are found.
        """
        elements = self.find_elements(xpaths, sub_element=sub_element, timeout=timeout)
        return [element.text for element in elements if element.text]

    def find_text(self, xpaths: tuple, sub_element: WebElement = None, timeout: int = DEFAULT_TIMEOUT, index: int = 0) -> str:
        """
        Finds a single element matching any of the given XPaths at the specified index and retrieves the visible text.

        :param xpaths: A list of XPath strings to find the element.
        :param sub_element: The parent element to search within (default is None).
        :param timeout: Time in seconds to wait for the element to appear (default is 0, meaning no wait).
        :param index: Index of the element to get the text from (default is 0, meaning first element).
        :return: The visible text of the element at the specified index. Returns None if no elements are found, index is out of range, or element has no text.
        """
        elements = self.find_elements(xpaths, sub_element=sub_element, timeout=timeout)
        if elements and 0 <= index < len(elements):
            return elements[index].text

    def quit_browser(self) -> None:
        """
        Closes the browser and quits the WebDriver session.

        :return: None
        """
        self.driver.quit()
