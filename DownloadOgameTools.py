# https://stackoverflow.com/questions/29563335/how-do-i-load-session-and-cookies-from-selenium-browser-to-requests-library-in-p

from selenium import webdriver
import time
import requests
import os
import shutil


def get_cookies(user_id,user_pw):
    browser = webdriver.Chrome()
    browser.get("https://github.com/login")

    id_css_selector = "#login_field"
    pw_css_selector = "#password"
    login_css_selector = "#login > form > div.auth-form-body.mt-3 > input.btn.btn-primary.btn-block"
    browser.find_element_by_css_selector(id_css_selector).send_keys(user_id)
    browser.find_element_by_css_selector(pw_css_selector).send_keys(user_pw)
    browser.find_element_by_css_selector(login_css_selector).click()
    time.sleep(3)
    cookies = browser.get_cookies()
    browser.quit()

    return cookies

def transfer_cookies(session, cookies):
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    
def download_driver():
    file_url = requests.Session().get("https://github.com/taeyongjeon/ScrapingCobeblocksPython/raw/master/chromedriver.exe")

    with open("chromedriver.exe", 'wb') as f:
        f.write(file_url.content)
    
def download_file(session,url,filename):
    file_url = session.get(url)

    with open("OgameTools/"+filename, 'wb') as f:
        f.write(file_url.content)

    print(filename+" downloaded.")

if __name__=='__main__':
    url = ["https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/autoattack.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/espionage.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/galaxytool.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/loginogame.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/mailtocsv.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/main.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/preparewebdriver.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/testcase.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/util.py",
           "https://github.com/taeyongjeon/ScrapingCobeblocksPython/raw/master/chromedriver.exe"]
    filename = ["autoattack.py",
                "espionage.py",
                "galaxytool.py",
                "loginogame.py",
                "mailtocsv.py",
                "main.py",
                "preparewebdriver.py",
                "testcase.py",
                "util.py",
                "chromedriver.exe"]

    if os.path.isdir("OgameTools"):
        shutil.rmtree("OgameTools")
    os.mkdir("OgameTools")
        
    if not os.path.isfile("chromedriver.exe"):
        download_driver()

    s = requests.Session()
    cookies = get_cookies('taeyongjeon','cilarnycstme24*') # ID, PW 입력
    transfer_cookies(s, cookies)
    for i in range(0,len(url)):
        download_file(s,url[i],filename[i])
