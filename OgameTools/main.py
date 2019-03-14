import preparewebdriver
import loginogame
import espionage
import mailtocsv
import autoattack
import galaxytool
import util
from selenium import webdriver
import time

def main(URL,loginid,loginpw):
    browser = preparewebdriver.prepare_webdriver()
    loginogame.login_ogame(browser,URL,loginid,loginpw)
    choice = 0
    while choice!=8 :
        util.cls()
        choice = input("작업 입력\n1 : 정찰\n2 : 시간 대기\n3 : 정찰 내용을 Csv로 저장\n4 : 자동공격\n5 : 갤럭시툴\n8 : 종료\n--> ")
        if int(choice) == 1:
            spionage.espionage(browser)
        if int(choice) == 2:
            util.wait_time()
        if int(choice) == 3:
            mailtocsv.mail_to_csv(browser)
        if int(choice) == 4:
            autoattack.auto_attack(browser)
        if int(choice) == 5:
            galaxytool.enter_galaxy_tab(browser)
        if int(choice) == 8:
           browser.quit()
           break


if __name__ == '__main__':
    #country = input("주소 앞 서브도메인을 입력하십시오.\n예시 : 영국 서버(https://en.ogame.gameforge.com/)라면 en을 입력하십시오.\n--> ")
    #loginid = input("이메일을 입력하십시오.\n--> ")
    #loginpw = input("암호를 입력하십시오.\n--> ")
    main("https://en.ogame.gameforge.com/", "dfo@vomoto.com", "789456")
