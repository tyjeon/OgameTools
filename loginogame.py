from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_ogame(browser,URL,loginid,loginpw):
    print("1/3 홈페이지로 접속...")
    browser.get(URL)
    print("1/3 홈페이지로 접속... 완료.")
    
    __login_submit(browser,loginid,loginpw)
    
def __login_submit(browser,loginid,loginpw):
    print("2/3 로그인 시도...")
    WebDriverWait(browser, 20). \
                           until(EC.presence_of_element_located((By.CSS_SELECTOR,"#ui-id-1")))
    browser.find_element_by_css_selector("#ui-id-1").click()
    WebDriverWait(browser, 20). \
                           until(EC.presence_of_element_located((By.CSS_SELECTOR,"#usernameLogin")))
    browser.find_element_by_css_selector("#usernameLogin").send_keys(loginid)
    browser.find_element_by_css_selector("#passwordLogin").send_keys(loginpw)
    browser.find_element_by_css_selector("#loginSubmit").click()
    print("2/3 로그인 시도... 완료.")
    
    __click_play_button(browser)
    
def __click_play_button(browser):
    print("3/3 게임으로 들어가는 중...")
    WebDriverWait(browser, 20). \
                           until(EC.presence_of_element_located((By.CSS_SELECTOR,"#joinGame > a > button > span")))
    browser.find_element_by_css_selector("#joinGame > a > button > span").click()
    WebDriverWait(browser, 20). \
                           until(EC.presence_of_element_located \
                                 ((By.CSS_SELECTOR,"#accountlist > div > div.rt-table > div.rt-tbody > div > div > div.rt-td.action-cell > button")))
    browser.find_element_by_css_selector("#accountlist > div > div.rt-table > div.rt-tbody > div > div > div.rt-td.action-cell > button").click()
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 20). \
                           until(EC.presence_of_element_located((By.CSS_SELECTOR,"#menuTable > li:nth-child(9) > a")))
    print("3/3 게임으로 들어가는 중... 완료.")
