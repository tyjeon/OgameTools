from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import csv
import os

def auto_attack(browser):
    __galaxy_coordinate = []
    __system_coordinate = []
    __planet_number_coordinate = []
    __number_of_large_cargo = []
    __attack_coordinates = []
    
    with open(__find_latest_created_filename(), 'r') as r:
        __csv_content = csv.reader(r)
        for row in __csv_content:
            __galaxy_coordinate.append(row[1])
            __system_coordinate.append(row[2])
            __planet_number_coordinate.append(row[3])
            __number_of_large_cargo.append(row[8])

    for i in range(1,len(__galaxy_coordinate)): # i = 0일때 리스트는 제목 행을 가리킴.
        
        __attack_coordinates=[__galaxy_coordinate[i],__system_coordinate[i], \
                          __planet_number_coordinate[i],__number_of_large_cargo[i]]
        print("좌표 : "+str(__attack_coordinates[0])+ \
              ":"+str(__attack_coordinates[1])+":"+str(__attack_coordinates[2])+"에 대한 공격...")
        
        __enter_fleet_tab(browser,__attack_coordinates)

def __find_latest_created_filename():
    __latest_created_filename = ""
    __latest_created_time = ""

    __file_list = os.listdir(os.getcwd()) # 현재 디렉토리
    
    for item in __file_list:
        if item.find('Espionage') is not -1:
            if __latest_created_filename =="":
                __latest_created_filename = item
                __latest_created_time = time.ctime(os.path.getctime(item))
            else:
                if __latest_created_time <= time.ctime(os.path.getctime(item)):
                    __latest_created_filename = item
                    __latest_created_time = time.ctime(os.path.getctime(item))
    print(str(__latest_created_filename)+" 파일을 적용합니다.")
    return __latest_created_filename

def __enter_fleet_tab(browser, __attack_coordinates):
    print("Fleet 메뉴로 이동")
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#menuTable > li:nth-child(8) > a")))
    browser.find_element_by_css_selector("#menuTable > li:nth-child(8) > a > span").click()

    __select_fleet(browser, __attack_coordinates)

def __select_fleet(browser, __attack_coordinates):
          
    # #ship_203 카대 숫자 입력칸.
    # #ship_210 정위 숫자 입력칸.
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#sendall")))
    print("함대 선택")
    
    print("테스트케이스로, 정위 1개만 보냅니다.")
    browser.find_element_by_css_selector("#ship_210").send_keys("1")
    
    #현재보유카대숫자구현하기
    #("현재 카대 숫자 : "+#현재보유카대숫자구현하기+" "+str(__attack_coordinates[3])+"만큼의 카대 선택")
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#continue")))
    browser.find_element_by_css_selector("#continue").click()
    
    __enter_coordinates(browser, __attack_coordinates)

def __enter_coordinates(browser, __attack_coordinates):
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#pbutton")))
    print("좌표 입력 : "+str(__attack_coordinates[0])+":"+str(__attack_coordinates[1])+ \
          ":"+str(__attack_coordinates[2]))
    browser.find_element_by_css_selector("#galaxy").click
    browser.find_element_by_css_selector("#galaxy").send_keys(Keys.BACKSPACE)
    browser.find_element_by_css_selector("#galaxy").send_keys(Keys.DELETE)
    browser.find_element_by_css_selector("#galaxy").send_keys(__attack_coordinates[0])
    browser.find_element_by_css_selector("#system").send_keys(__attack_coordinates[1])
    browser.find_element_by_css_selector("#position").send_keys(__attack_coordinates[2])
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#continue")))
    browser.find_element_by_css_selector("#continue").click()
    __send_fleet(browser)

def __send_fleet(browser):
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#missionButton1")))
    browser.find_element_by_css_selector("#missionButton1").click()
    time.sleep(random.randrange(20,30)*0.1)
    browser.find_element_by_css_selector("#start").click()
    time.sleep(random.randrange(10,20)*0.1)
    print("좌표 : "+str(__attack_coordinates[0])+":"+str(__attack_coordinates[1])+":"+str(__attack_coordinates[2])+"에 대한 공격 미션 수행")
