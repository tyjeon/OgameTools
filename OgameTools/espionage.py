import util

from selenium import webdriver
import csv
import datetime
import time
import random


def espionage(browser):

    checkForCsvFile = 0
    checkForCsvFile = input("이 작업을 진행하기 위해서는 갤럭시,시스템,행성번호만으로 이루어진(제목 행 불필요) 'espionage.csv' 파일이 필요합니다.\n준비되어 있는 경우 1을 입력하세요.\n--> ")

    if int(checkForCsvFile) != 1:
        return 0
    
    galaxyCoordinate = []
    systemCoordinate = []
    planetNumberCoordinate = []
    with open('espionage.csv', 'r') as r:
        csvContent=csv.reader(r)
        for row in csvContent:
            galaxyCoordinate.append(row[0])
            systemCoordinate.append(row[1])
            planetNumberCoordinate.append(row[2])
        
    print("Galaxy 메뉴로 이동")
    time.sleep(3)

    browser.find_element_by_css_selector("#menuTable > li:nth-child(9) > a").click()
    time.sleep(3)
    
    for i in range(0,len(galaxyCoordinate)):
        while(True):
            source = browser.page_source
            util.moveToCoordinate(browser,galaxyCoordinate[i],systemCoordinate[i])
            if util.isIValueSameAsGalaxy(source, galaxyCoordinate[i]):
                if util.isJValueSameAsSystem(source, systemCoordinate[i]):
                  break
        time.sleep(3)
        targetEspionageIcon = browser.find_element_by_xpath("//*[@id=\"galaxytable\"]/tbody/tr["+str(planetNumberCoordinate[i])+"]/td[8]/span/a[1]/span")
        targetEspionageIcon.click()
        print(str(galaxyCoordinate[i])+":"+str(systemCoordinate[i])+":"+str(planetNumberCoordinate[i])+"에 대한 정찰 명령 수행 : "+str(i+1)+"/"+str(len(galaxyCoordinate))+" 완료.")
        time.sleep(random.randrange(10,20)*0.1)
        if int(i) == int(len(galaxyCoordinate)-1) :
            print("완료")
