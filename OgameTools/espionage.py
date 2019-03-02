import util

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import datetime
import time
import random
import os

def espionage(browser):
    __galaxy_coordinate = []
    __system_coordinate = []
    __planet_number_coordinate = []
    __espionage_coordinates = []

    __file_list = os.listdir(os.getcwd())
    is_there_espionage_file = 0
    for item in __file_list:
        if item.find('espionage.csv') is not -1:
            with open('espionage.csv', 'r') as r:
                __csv_content=csv.reader(r)
                for row in __csv_content:
                    __galaxy_coordinate.append(row[0])
                    __system_coordinate.append(row[1])
                    __planet_number_coordinate.append(row[2])
            is_there_espionage_file = 1
    if is_there_espionage_file == 0:
            print("이 작업을 진행하기 위해서는 갤럭시,시스템,행성번호만으로 이루어진(제목 행 불필요) 'espionage.csv' 파일이 필요합니다.")
            return 0

    __enter_galaxy_tab(browser)

    for i in range(0,len(__galaxy_coordinate)):
        __espionage_coordinates=[__galaxy_coordinate[i],__system_coordinate[i],__planet_number_coordinate[i]]
        print("-------------------------------------------------")
        print(str(len(__galaxy_coordinate)) + "개 좌표 중 " + str(i+1) + "번째 - 좌표 : "+str(__espionage_coordinates[0])+ \
              ":" + str(__espionage_coordinates[1]) + ":" + str(__espionage_coordinates[2]) + "에 대한 정탐...")

        __move_to_espionage_coordinates(browser, __espionage_coordinates)

    # 정탐 시간 체크
    browser.find_element_by_css_selector("#menuTable > li:nth-child(1) > a").click()
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#js_eventDetailsClosed")))
    browser.find_element_by_css_selector("#js_eventDetailsClosed").click()
    time.sleep(2)
    source = browser.page_source
    bs_object = BeautifulSoup(source, "html.parser")
    fleet_movements = bs_object.findAll("td",{"class":"countDown friendly textBeefy"})
    for fleet in fleet_movements:
        print(fleet.get_text())
    
        
def __enter_galaxy_tab(browser):
    print("Galaxy 메뉴로 최초 이동")
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#menuTable > li:nth-child(9) > a")))
    browser.find_element_by_css_selector("#menuTable > li:nth-child(9) > a").click()

def __move_to_espionage_coordinates(browser, __espionage_coordinates):
    print("1/2 좌표로 이동...", end = " ")
    while(True):
        util.move_to_coordinates(browser,__espionage_coordinates[0],__espionage_coordinates[1])
        if __is_in_the_right_coordinates(browser, __espionage_coordinates):
            break
    print("완료.")
    
    __espionage_target_coordinates(browser, __espionage_coordinates)

def __espionage_target_coordinates(browser, __espionage_coordinates):
    print("2/2 좌표에 대한 정탐 미션 수행...", end = " ")
    time.sleep(random.randrange(10,20)*0.1)
    target_espionage_icon = browser.find_element_by_xpath("//*[@id=\"galaxytable\"]/tbody/tr["+str(__espionage_coordinates[2])+"]/td[8]/span/a[1]/span")
    target_espionage_icon.click()
    print("완료.")
    time.sleep(random.randrange(10,20)*0.1)

def __is_in_the_right_coordinates(browser, __espionage_coordinates):
    while(True):
        source = browser.page_source
        if util.is_i_value_same_as_galaxy(source, __espionage_coordinates[0]):
            if util.is_j_value_same_as_system(source, __espionage_coordinates[1]):
                return 1
