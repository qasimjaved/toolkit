from selenium import webdriver
from selenium.webdriver import Chrome as chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def launch_browser():
    """
    Launch chrome-browser

    :return: driver
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_up(driver, limit=10):
    for _ in range(limit):
        driver.execute_script("scrollBy(0,-500);")


def find_elements_per_xpath(driver: chrome_driver, xpath, timeout=0):
    """
    Get single_element matching xpath

    :param timeout:
    :param xpath:
    :param driver:
    :return: element
    """
    try:
        if timeout:
            elements = WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
        else:
            elements = driver.find_elements(by=By.XPATH, value=xpath)
        return elements
    except:
        print("Timed out waiting for the element to appear.")
        return []


def find_elements(driver, xpaths, timeout=0):
    """
    Get single_element matching xpath

    :param xpaths:
    :param driver:
    :return: element
    """
    for xpath in xpaths:
        elements = find_elements_per_xpath(driver, xpath, timeout=timeout)
        if elements:
            return elements


def find_element(driver, xpaths, timeout=0):
    """
    Get single_element matching xpath

    :param xpaths:
    :param driver:
    :return: element
    """
    elements = find_elements(driver, xpaths, timeout)
    if elements:
        return elements[0]


def find_clickable_element_per_xpath(driver, xpath, timeout=5):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return element
    except:
        print("Timed out waiting for clickable element to appear.")


def find_clickable_element(driver, xpaths, timeout=5):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """
    for xpath in xpaths:
        element = find_clickable_element_per_xpath(driver, xpath, timeout=timeout)
        if element:
            return element


def find_attributes(driver, xpaths, attribute, timeout=0):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """
    elements = find_elements(driver, xpaths, timeout)
    if elements:
        return [element.get_attribute(attribute) for element in elements if element.get_attribute(attribute)]


def find_attribute(driver, xpaths, attribute, timeout=0):
    """
    Get single_element matching xpath

    :param driver:
    :param xpaths:
    :param attribute:
    :param timeout:

    :return: element
    """

    elements = find_elements(driver, xpaths, timeout)
    for element in elements:
        if element.get_attribute(attribute):
            return element.get_attribute(attribute)


def find_all_text(driver, xpaths, timeout=0):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """
    elements = find_elements(driver, xpaths, timeout)
    all_text = [element.text for element in elements if element.text]
    return all_text


def find_text(driver, xpaths, timeout=0):
    """
    Get single_element matching xpath

    :param xpaths:
    :param driver:
    :return: element
    """
    elements = find_elements(driver, xpaths, timeout)
    for element in elements:
        if element.text:
            return element.text
