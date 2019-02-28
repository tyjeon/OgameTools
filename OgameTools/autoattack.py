from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import csv
import os

def autoattack(browser):
    galaxyCoordinate = []
    systemCoordinate = []
    planetNumberCoordinate = []
    numberOfLargeCargo = []
    attackCoordinate = []
    
    with open(find_latest_created_filename(), 'r') as r:
        csvContent=csv.reader(r)
        for row in csvContent:
            galaxyCoordinate.append(row[1])
            systemCoordinate.append(row[2])
            planetNumberCoordinate.append(row[3])
            numberOfLargeCargo.append(row[8])

    for i in range(1,len(galaxyCoordinate)): # i = 0일때 리스트는 제목 행을 가리킴.
        attackCoordinate=[galaxyCoordinate[i],systemCoordinate[i], \
                          planetNumberCoordinate[i],numberOfLargeCargo[i]]
        print("좌표 : "+str(attackCoordinate[0])+":"+str(attackCoordinate[1])+":"+str(attackCoordinate[2])+"에 대한 공격")
        
        enterFleetTab(browser,attackCoordinate)

def find_latest_created_filename():
    latestCreatedFileName = ""
    latestCreatedTime =""

    file_list = os.listdir(os.getcwd()) # 현재 디렉토리
    
    for item in file_list:
        if item.find('Espionage') is not -1:
            if latestCreatedFileName =="":
                latestCreatedFileName = item
                latestCreatedTime = time.ctime(os.path.getctime(item))
            else:
                if latestCreatedTime <= time.ctime(os.path.getctime(item)):
                    latestCreatedFileName = item
                    latestCreatedTime = time.ctime(os.path.getctime(item))
    print(str(latestCreatedFileName)+" 파일을 적용합니다.")
    return latestCreatedFileName

def enterFleetTab(browser, attackCoordinate):
    print("Fleet 메뉴로 이동")
    time.sleep(3)

    browser.find_element_by_css_selector("#menuTable > li:nth-child(8) > a > span").click()
    time.sleep(3)

    selectFleet(browser, attackCoordinate)

def selectFleet(browser, attackCoordinate):
          
    # #ship_203 카대 숫자 입력칸. 
    # #ship_210 정위 숫자 입력칸.

    print("함대 선택")
    browser.find_element_by_css_selector("#ship_210").send_keys(attackCoordinate[3])
    #현재보유카대숫자구현하기
    #("현재 카대 숫자 : "+#현재보유카대숫자구현하기+" "+str(attackCoordinate[3])+"만큼의 카대 선택")

    time.sleep(random.randrange(30,40)*0.1)
    browser.find_element_by_css_selector("#continue").click()

    enterCoordinates(browser, attackCoordinate)

def enterCoordinates(browser, attackCoordinate):
    print("좌표 입력 : "+str(attackCoordinate[0])+":"+str(attackCoordinate[1])+":"+str(attackCoordinate[2]))
    time.sleep(random.randrange(10,20)*0.1)

    browser.find_element_by_css_selector("#galaxy").click
    browser.find_element_by_css_selector("#galaxy").send_keys(Keys.BACKSPACE)
    browser.find_element_by_css_selector("#galaxy").send_keys(Keys.DELETE)
    browser.find_element_by_css_selector("#galaxy").send_keys(attackCoordinate[0])
    browser.find_element_by_css_selector("#system").send_keys(attackCoordinate[1])
    browser.find_element_by_css_selector("#position").send_keys(attackCoordinate[2])
    time.sleep(random.randrange(20,30)*0.1)
    browser.find_element_by_css_selector("#continue").click()
    sendFleet(browser)

def sendFleet(browser):
    time.sleep(random.randrange(30,40)*0.1)
    browser.find_element_by_css_selector("#missionButton1").click()
    time.sleep(random.randrange(10,20)*0.1)
    browser.find_element_by_css_selector("#start").click()
    time.sleep(random.randrange(10,20)*0.1)
    print("좌표 : "+str(attackCoordinate[0])+":"+str(attackCoordinate[1])+":"+str(attackCoordinate[2])+"에 대한 공격 미션 수행")
