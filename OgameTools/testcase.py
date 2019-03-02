import preparewebdriver
import loginogame
import espionage
import mailtocsv
import autoattack
import galaxytool
import util
from selenium import webdriver
import time

def testcase(URL,loginid,loginpw):
    test = input("1 : 정찰\n"
                 "2 : 대기\n"
                 "3 : 메일 정리\n"
                 "4 : 자동공격\n"
                 "5 : 갤럭시툴\n"
                 "1234와 같이 여러 작업 수행 가능\n")
    start_time = time.time()
    browser = preparewebdriver.prepare_webdriver()
    loginogame.login_ogame(browser,URL,loginid,loginpw)
    print("테스트 - 로그인 소요 시간 : "+str(time.time()-start_time))

    if "1" in test:
        espionage_test(browser)
    if "2" in test:
        wait_test()
    if "3" in test:
        mail_to_csv_test(browser)
    if "4" in test:
        autoattack_test(browser)
    if "5" in test:
        galaxytool_test(browser)

def espionage_test(browser):
    with open('espionage.csv', encoding="utf-8",mode='w') as f: # 테스트케이스입니다.
        print("8,479,8",file=f)
        print("8,480,8",file=f)

    start_time = time.time()            
    espionage.espionage(browser)    
    print("테스트 - 정찰 소요 시간 : "+str(time.time()-start_time))

def wait_test():
    util.wait_time()

def mail_to_csv_test(browser):
    start_time = time.time()
    mailtocsv.mail_to_csv(browser)
    print("테스트 - 메일 정리 소요 시간 : "+str(time.time()-start_time))

def autoattack_test(browser):
    start_time = time.time()
    autoattack.auto_attack(browser)
    print("테스트 - 공격 소요 시간 : "+str(time.time()-start_time))

def galaxytool_test(browser):
    with open('Espionage_2019_test.csv', encoding="utf-8",mode='w') as f: # 테스트케이스입니다.
        print("tst,tst,tst,tst,tst,tst,tst,tst,tst,tst,tst,tst,tst",file=f)
        print("Homeworld,8,480,8,  Chief Euler,10000,10000,0,0,0,20000,0,0",file=f)
        print("Homeworld,8,480,6,  Proconsul Midas,10000,10000,0,0,0,20000,0,0",file=f)
        print("Homeworld,8,479,4,  Constable Pallas,10000,10000,10000,0,0,30000,0,0",file=f)

    start_time = time.time()
    galaxytool.enter_galaxy_tab(browser)
    print("테스트 - 갤럭시툴 소요 시간 : "+str(time.time()-start_time))

if __name__ == '__main__':
    print("테스트 케이스 아이디로 대체")
    testcase("https://en.ogame.gameforge.com/", "dfo@vomoto.com", "789456")
