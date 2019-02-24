
# Selenium의 웹드라이버 인스턴스를 함수끼리 주고받는 법
# Python
# https://stackoverflow.com/questions/51661710/how-to-pass-selenium-webdriver-instances-between-functions-in-python/51664362#51664362

"""
You would return the instance from the first function and call the second function with it.

In the example below, I define 2 functions.
A webdriver is instantiaterd inside func1, which returns the instance.
Then I call func2, which takes a driver instance as an argument.
"""
from selenium import webdriver

def func1():
    driver = webdriver.Chrome()
    driver.get('https://example.com')
    return driver

def func2(driver):
    return driver.title

if __name__ == '__main__':
    driver = func1()
    title = func2(driver)
    print(title)
    driver.quit()
