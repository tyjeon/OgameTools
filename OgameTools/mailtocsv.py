import util

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import time
import datetime
import re

def mailtocsv(browser):
        print("메일함으로 이동")
        browser.get("https://s1-en.ogame.gameforge.com/game/index.php?page=messages")
        WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#ui-id-23")))
        time.sleep(5)
        
        planetName = []
        planetGalaxy = []
        planetSystem = []
        planetNumber = []
        playerName = []
        metal = []
        crystal = []
        deuterium = []
        numberOfLargeCargo = []
        numberOfLargeCargo5x = []
        totalResources = []
        defence = []
        fleets = []

        source = browser.page_source
        bsObject = BeautifulSoup(source, "html.parser")
        mailsSources = bsObject.findAll("li",{"class":"msg"})

        filename = ""
        filename = setEspionageCsvTitleRow()   

        totalPage = getTotalPageNumber(bsObject)
        for i in range(0,int(totalPage)):

            while(True):
                source = browser.page_source
                bsObject = BeautifulSoup(source, "html.parser")
                if str(getCurrentPageNumber(bsObject)) == str(i+1):
                    mailsSources = bsObject.findAll("li",{"class":"msg"})
                    break
            
            print("메일함의 "+str(i+1)+"/"+str(totalPage)+" 페이지 진행 중")
        
            for mailSource in mailsSources:
                mailHead = ""
                mailHead = mailSource.find("div",{"class":"msg_head"}) # 정찰 미션 결과가 아닌 메세지는 넘김.
                if not "Espionage report from" in str(mailHead):
                    continue
                
                planetName.append(getPlanetNameInMail(mailSource))
                planetGalaxy.append(getPlanetGalaxyInMail(mailSource))
                planetSystem.append(getPlanetSystemInMail(mailSource))
                planetNumber.append(getPlanetNumberInMail(mailSource))
                playerName.append(getPlayerNameInMail(mailSource))
                
                metal.append(getDataInMail(mailSource,"Metal: "))
                crystal.append(getDataInMail(mailSource,"Crystal: "))
                deuterium.append(getDataInMail(mailSource,"Deuterium: "))
                numberOfLargeCargo.append(int(float(getDataInMail(mailSource,"Resources: "))/50000))
                numberOfLargeCargo5x.append(int(float(getDataInMail(mailSource,"Resources: "))/250000)) # 카르고 대 숫자- 5대 단위로 끊어서
                totalResources.append(getDataInMail(mailSource,"Resources: "))
                defence.append(getDataInMail(mailSource,"Defence: "))
                fleets.append(getDataInMail(mailSource,"Fleets: "))

            print("메일함의 "+str(i+1)+"/"+str(totalPage)+" 페이지 완료.")
            
            if int(totalPage) != 1:
                browser.find_element_by_css_selector("#fleetsgenericpage > ul > ul:nth-child(1) > li:nth-child(4)").click()
                WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#ui-id-23")))
                time.sleep(5)

        for j in range(len(planetName)):
                with open(filename, encoding="utf-8",mode='a+') as f:
                        print(",".join([planetName[j],planetGalaxy[j],planetSystem[j],planetNumber[j],playerName[j],\
                                        metal[j],crystal[j],deuterium[j],str(numberOfLargeCargo[j]),str(numberOfLargeCargo5x[j]),\
                                        totalResources[j],defence[j],fleets[j]]),file=f)
            
def getCurrentPageNumber(bsObject):
    argumentsForParsing=[bsObject,["li","class","curPage"],"(.*data-tab=\"\d*\">|\/.*)"]
    return util.parse_using_regexp(argumentsForParsing)

def getTotalPageNumber(bsObject):
    argumentsForParsing=[bsObject,["li","class","curPage"],"(.*data-tab=\"\d*\">\d*\/|<\/li>.*)"]
    return util.parse_using_regexp(argumentsForParsing)

def getPlanetNameInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class","msg_title blue_txt"],"(.*figure>| .*)"]
    return util.parse_using_regexp(argumentsForParsing)

def getPlanetGalaxyInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class","msg_title blue_txt"],"(.*\[|:.*)"]
    return util.parse_using_regexp(argumentsForParsing)

def getPlanetSystemInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class","msg_title blue_txt"],"(.*\[\d+:|:\d+].*)"]
    return util.parse_using_regexp(argumentsForParsing)
    
def getPlanetNumberInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class","msg_title blue_txt"],"(.*:|\].*)"]
    return util.parse_using_regexp(argumentsForParsing)

def getPlayerNameInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class",re.compile("status_*")],"(<span.*\">|<\/span>)"]
    return util.parse_using_regexp(argumentsForParsing)

def getDataInMail(mailSource, string):
    argumentsForParsing=[mailSource,["span","class",re.compile("msg_content")],"(.*"+string+"|<\/span>.*)|\."]
    dataInHtml = util.parse_using_regexp(argumentsForParsing)
    
    if "compacting" in dataInHtml: # 정탐 레벨 낮음
        data = "Low_Espionage_Level"
    else:
        data = dataInHtml

    return data

def setEspionageCsvTitleRow():
    today = datetime.datetime.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    hour = str(today.hour)
    minute = str(today.minute)
    second = str(today.second)

    filename = "Espionage_"+year+"_"+month+"_"+day+"_"+hour+"_"+minute+".csv"

    print("파일 생성")

    with open(filename, encoding="utf-8",mode='a+') as f:
        print("Planet,Gal,Sys,Pla,Player,Metal,Crystal,Deuterium,LargeCargo,LargeCargo5x,Resources,Defence,Fleets",file=f)

    return filename
