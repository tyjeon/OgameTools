import preparewebdriver
import loginogame
import galaxytool
import util
from selenium import webdriver
import time

def OgameTools(URL,loginid,loginpw):
    browser = preparewebdriver.prepare_webdriver()
    loginogame.login_ogame(browser,URL,loginid,loginpw)
    util.cls()
    galaxytool.enter_galaxy_tab(browser)

if __name__ == '__main__':
    country = input("주소 앞 서브도메인을 입력하십시오.\n예시 : 영국 서버(https://en.ogame.gameforge.com/)라면 en을 입력하십시오.\n--> ")
    loginid = input("이메일을 입력하십시오.\n--> ")
    loginpw = input("암호를 입력하십시오.\n--> ")
    OgameTools("https://"+country+".ogame.gameforge.com/", loginid, loginpw)
    
