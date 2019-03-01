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

    testcase = 1
    if testcase == 1:
        testcasestart(URL,loginid,loginpw)
        return 0
    browser = preparewebdriver.prepare_webdriver()
    loginogame.login_ogame(browser,URL,loginid,loginpw)
    while(choice!=8):
        cls()
        choice = input("작업 입력\n1 : 정찰\n2 : 시간 대기\n3 : 정찰 내용을 Csv로 저장\n4 : 자동공격\n5 : 갤럭시툴\n8 : 종료\n--> ")
        if int(choice) == 1:
            spionage.espionage(browser)
        if int(choice) == 2:
            util.wait_time(browser)
        if int(choice) == 3:
            mailtocsv.mail_to_csv(browser)
        if int(choice) == 4:
            autoattack.auto_attack(browser)
        if int(choice) == 5:
            galaxytool.enter_galaxy_tab(browser)
        if int(choice) == 8:
           browser.quit()
           break

def testcasestart(URL,loginid,loginpw):
        # 이 아래부터 테스트케이스
    testcase = 1
    if testcase == 1:
        print("테스트 - 시간 측정")
        start_time = time.time()
        browser = preparewebdriver.prepare_webdriver()
        loginogame.login_ogame(browser,URL,loginid,loginpw)
        print("테스트 - 로그인 시간 : "+str(time.time()-start_time))
        start_time = time.time()
        
        with open('espionage.csv', encoding="utf-8",mode='w') as f: # 테스트케이스입니다.
            print("8,480,6",file=f)
            print("8,479,8",file=f)
            print("8,480,8",file=f)
            
        #espionage.espionage(browser)
        #print("테스트 - 정찰 시간 : "+str(time.time()-start_time))
        #start_time = time.time()
        
        #mailtocsv.mail_to_csv(browser)
        #print("테스트 - 메일 정리 시간 : "+str(time.time()-start_time))
        #start_time = time.time()

        with open('Espionage_2019_test.csv', encoding="utf-8",mode='w') as f: # 테스트케이스입니다.
            print("tst,tst,tst,tst,tst,tst,tst,tst,tst,tst,tst,tst,tst",file=f)
            print("Homeworld,8,480,8,  Chief Euler,10000,10000,0,0,0,20000,0,0",file=f)
            print("Homeworld,8,480,6,  Proconsul Midas,10000,10000,0,0,0,20000,0,0",file=f)
            print("Homeworld,8,479,4,  Constable Pallas,10000,10000,10000,0,0,30000,0,0",file=f)
        #autoattack.auto_attack(browser)
        #print("테스트 - 공격 시간 : "+str(time.time()-start_time))
        #start_time = time.time()
        
        galaxytool.enter_galaxy_tab(browser)
        print("테스트 - 갤럭시툴 시간 : "+str(time.time()-start_time))
        start_time = time.time()


if __name__ == '__main__':
    country = input("주소 앞 서브도메인을 입력하십시오.\n예시 : 영국 서버(https://en.ogame.gameforge.com/)라면 en을 입력하십시오.\n--> ")
    loginid = input("이메일을 입력하십시오.\n--> ")
    loginpw = input("암호를 입력하십시오.\n--> ")
    #OgameTools("https://en.ogame.gameforge.com/", "dfo@vomoto.com", "789456")
    OgameTools("https://"+country+".ogame.gameforge.com/", loginid, loginpw)
