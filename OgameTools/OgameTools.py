import loginogame
import espionage
import mailtocsv
import autoattack
import galaxytool
import util

from selenium import webdriver
import time

def OgameTools(URL,loginid,loginpw):
    browser = prepareWebdriver()
    loginogame.loginogame(browser,URL,loginid,loginpw)
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[-1])

    choice = 0

    testcase = 1
    if testcase == 1:
        choice=8
        with open('espionage.csv', encoding="utf-8",mode='w') as f: # 테스트케이스입니다.
            print("8,480,6",file=f)
            print("8,479,8",file=f)
            print("8,480,8",file=f)
        #espionage.espionage(browser)
        #mailtocsv.mailtocsv(browser)
        #autoattack.autoattack(browser)
        galaxytool.enterGalaxyTab(browser)
        return 0
    
    while(choice!=8):
        cls()
        choice = input("작업 입력\n1 : 정찰\n2 : 정찰 내용을 Csv로 저장\n3 : 자동공격\n5 : 갤럭시툴\n8 : 종료\n--> ")
        if int(choice) == 1:
            espionage(browser)
        if int(choice) == 2:
            mailtocsv.mailtocsv(browser)
        if int(choice) == 3:
            autoAttack(browser)
        if int(choice) == 5:
            enterGalaxyTab(browser)
        if int(choice) == 8:
           browser.quit()
           break

def prepareWebdriver():
    headlessMode = 0
    proxyMode = 0
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    if headlessMode == 1:
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
        options.add_argument("--lang=en-us")

    if proxyMode == 1:
        # https://www.hide-my-ip.com/proxylist.shtml
        # Type:HTTPS, Anon:High, 그리고 속도 빠른 걸로 선택.
        PROXY = "5.135.164.72:3128"
        options.add_argument('--proxy-server=%s' % PROXY)
        
    browser = webdriver.Chrome(chrome_options=options)

    return browser

if __name__ == '__main__':
    OgameTools("https://en.ogame.gameforge.com/", "dfo@vomoto.com", "789456")
