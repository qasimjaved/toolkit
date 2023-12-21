from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def launch_browser():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def find_elements(driver, xpath):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """

    elements = driver.find_elements(by=By.XPATH, value=xpath)
    return elements


def find_element(driver, xpath):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """

    elements = find_elements(driver, xpath)
    if elements:
        return elements[0]


def find_clickable_element(driver, xpath, timeout=10):
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
        ...


def find_attributes(driver, xpath, attribute):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """

    elements = find_elements(driver, xpath)
    if elements:
        return [element.get_attribute(attribute) for element in elements]


def find_attribute(driver, xpath, attribute):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """

    elements = find_elements(driver, xpath)
    if elements:
        return elements[0].get_attribute(attribute)


def find_text(driver, xpath):
    """
    Get single_element matching xpath

    :param driver:
    :return: element
    """

    elements = find_elements(driver, xpath)
    if elements:
        return elements[0].text


def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def scroll_up(driver, limit=10):
    for i in range(limit):
        driver.execute_script("scrollBy(0,-500);")
