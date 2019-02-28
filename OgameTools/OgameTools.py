import preparewebdriver
import loginogame
import espionage
import mailtocsv
import autoattack
import galaxytool
import util

from selenium import webdriver
import time

def OgameTools(URL,loginid,loginpw):
    browser = preparewebdriver.preparewebdriver()
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
        #galaxytool.enter_galaxy_tab(browser)
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

if __name__ == '__main__':
    OgameTools("https://en.ogame.gameforge.com/", "dfo@vomoto.com", "789456")
