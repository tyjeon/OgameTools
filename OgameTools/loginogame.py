from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def loginogame(browser,URL,loginid,loginpw):
    print("로그인   1/4")
    browser.get(URL)
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#ui-id-1")))
    browser.find_element_by_css_selector("#ui-id-1").click()
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#usernameLogin")))
    browser.find_element_by_css_selector("#usernameLogin").send_keys(loginid)
    browser.find_element_by_css_selector("#passwordLogin").send_keys(loginpw)
    browser.find_element_by_css_selector("#loginSubmit").click()
    print("로비 입장   2/4")
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#joinGame > a > button > span")))
    browser.find_element_by_css_selector("#joinGame > a > button > span").click()
    print("게임으로 들어가는 중   3/4")
    WebDriverWait(browser, 15).until(EC.presence_of_element_located\
                                     ((By.CSS_SELECTOR,"#accountlist > div > div.rt-table > div.rt-tbody > div > div > div.rt-td.action-cell > button")))
    browser.find_element_by_css_selector("#accountlist > div > div.rt-table > div.rt-tbody > div > div > div.rt-td.action-cell > button").click()
    print("완료   4/4")
