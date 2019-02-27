from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
import re
from operator import eq
import datetime
import csv
import os


def OgameTools(URL,loginid,loginpw):
    browser = prepareWebdriver()
    loginOgame(browser,URL,loginid,loginpw)
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[-1])

    choice = 0
    while(choice!=8):
        cls()
        choice = input("작업 입력\n1 : 정찰\n2 : 정찰 내용을 Csv로 저장\n3 : 자동공격\n5 : 갤럭시툴\n8 : 종료\n--> ")
        if int(choice) == 1:
            espionage(browser)
        if int(choice) == 2:
            mailToCsv(browser)
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

def loginOgame(browser,URL,loginid,loginpw):
    print("로그인   1/4")
    browser.get(URL)
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#ui-id-1")))
    browser.find_element_by_css_selector("#ui-id-1").click()
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#usernameLogin")))
    browser.find_element_by_css_selector("#usernameLogin").send_keys(loginid)
    browser.find_element_by_css_selector("#passwordLogin").send_keys(loginpw)
    browser.find_element_by_css_selector("#loginSubmit").click()
    print("로비 입장   2/4")
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#joinGame > a > button > span")))
    browser.find_element_by_css_selector("#joinGame > a > button > span").click()
    print("게임으로 들어가는 중   3/4")
    WebDriverWait(browser, 15).until(EC.presence_of_element_located\
                                     ((By.CSS_SELECTOR,"#accountlist > div > div.rt-table > div.rt-tbody > div > div > div.rt-td.action-cell > button")))
    browser.find_element_by_css_selector("#accountlist > div > div.rt-table > div.rt-tbody > div > div > div.rt-td.action-cell > button").click()
    print("완료   4/4")
    
def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
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
        
    enterGalaxyTab(browser)
    
    for i in range(0,len(galaxyCoordinate)):
        while(True):
            source = browser.page_source
            moveToCoordinate(browser,galaxyCoordinate[i],systemCoordinate[i])
            if isIValueSameAsGalaxy(source, galaxyCoordinate[i]):
                if isJValueSameAsSystem(source, systemCoordinate[i]):
                  break

        targetEspionageIcon = browser.find_element_by_xpath("//*[@id=\"galaxytable\"]/tbody/tr["+str(planetNumberCoordinate[i])+"]/td[8]/span/a[1]/span")
        targetEspionageIcon.click()
        print(str(galaxyCoordinate[i])+":"+str(systemCoordinate[i])+":"+str(planetNumberCoordinate[i])+"에 대한 정찰 명령 수행 : "+str(i+1)+"/"+str(len(galaxyCoordinate))+" 완료.")
        time.sleep(random.randrange(10,20)*0.1)
        if int(i) == int(len(galaxyCoordinate)-1) :
            print("완료")

   
def mailToCsv(browser):
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
    return parseUsingRegExp(argumentsForParsing)

def getTotalPageNumber(bsObject):
    argumentsForParsing=[bsObject,["li","class","curPage"],"(.*data-tab=\"\d*\">\d*\/|<\/li>.*)"]
    return parseUsingRegExp(argumentsForParsing)

def getPlanetNameInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class","msg_title blue_txt"],"(.*figure>| .*)"]
    return parseUsingRegExp(argumentsForParsing)

def getPlanetGalaxyInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class","msg_title blue_txt"],"(.*\[|:.*)"]
    return parseUsingRegExp(argumentsForParsing)

def getPlanetSystemInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class","msg_title blue_txt"],"(.*\[\d+:|:\d+].*)"]
    return parseUsingRegExp(argumentsForParsing)
    
def getPlanetNumberInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class","msg_title blue_txt"],"(.*:|\].*)"]
    return parseUsingRegExp(argumentsForParsing)

def getPlayerNameInMail(mailSource):
    argumentsForParsing=[mailSource,["span","class",re.compile("status_*")],"(<span.*\">|<\/span>)"]
    return parseUsingRegExp(argumentsForParsing)

def getDataInMail(mailSource, string):
    argumentsForParsing=[mailSource,["span","class",re.compile("msg_content")],"(.*"+string+"|<\/span>.*)|\."]
    dataInHtml = parseUsingRegExp(argumentsForParsing)
    
    if "compacting" in dataInHtml: # 정탐 레벨 낮음
        data = "Low_Espionage_Level"
    else:
        data = NoneToBlank(dataInHtml)

    print(data)
    return data

def parseUsingRegExp(argumentsForParsing):
    dataSource = str(argumentsForParsing[0].find(argumentsForParsing[1][0],{argumentsForParsing[1][1]:argumentsForParsing[1][2]}))
    dataSource = re.sub(pattern="\n", repl="",string=dataSource)
    dataSource = str(re.sub(pattern=argumentsForParsing[2], repl="",string=dataSource))
    data = NoneToBlank(dataSource)
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

def autoAttack(browser):
    enterFleetTab(browser)

def enterFleetTab(browser):
    print("Fleet 메뉴로 이동")
    time.sleep(3)

    browser.find_element_by_css_selector("#menuTable > li:nth-child(8) > a > span").click()
    time.sleep(3)

    selectFleet(browser)

def selectFleet(browser):
    # csv에서 파일을 받아온 뒤, 카대 숫자를 입력하면 된다.
    # #ship_203 카대 숫자 입력칸. 
    # #ship_210 정위 숫자 입력칸.

    print("함대 선택")
    browser.find_element_by_css_selector("#ship_210").send_keys("2")

    time.sleep(random.randrage(10,20)*0.1)
    browser.find_element_by_css_selector("#continue > span").click()

    enterCoordinates(browser)

def enterCoordinates(browser):
    print("좌표 입력")
    browser.find_element_by_css_selector("#galaxy").send_keys("2")
    browser.find_element_by_css_selector("#system").send_keys("2")
    browser.find_element_by_css_selector("#position").send_keys("2")
    browser.find_element_by_css_selector("#continue > span").click()
    sendFleet(browser)

def sendFleet(browser):
    browser.find_element_by_css_selector("#missionButton1").click()
    browser.find_element_by_css_selector("#start > span").click()
    print("공격 미션 수행")

def enterGalaxyTab(browser):
    print("Galaxy 메뉴로 이동")
    time.sleep(3)

    browser.find_element_by_css_selector("#menuTable > li:nth-child(9) > a").click()
    time.sleep(3)

    loopGalaxy(browser)

def loopGalaxy(browser):
    for i in range(1,10): # 뒷자리 숫자 -1까지 순환한다. 10 입력시 1~9까지 순환.
        if(i>=2):
            while(True):
                if isIValueDifferentFromGalaxy(source[j-1],i):
                    moveToCoordinate(browser,i,1)
                    break
        else:
            moveToCoordinate(browser,1,1)

        source = []
        for j in range(1,500):
            momentWhenScrapingSystemStarts = time.time()
            source.append("")
            if j==1:
                while(True):
                    source[j-1]=browser.page_source
                    if isJValueSameAsSystem(source[j-1],1):
                        source[j-1]=browser.page_source
                        break
            elif j>=2:
                while(True):
                    if j>=2:
                        source[j-1]=browser.page_source
                                
                    if isJValueDifferentFromSystem(source[j-1],j):
                        moveSystem(browser,j)

                    if isIValueSameAsGalaxy(source[j-1],i) and isJValueSameAsSystem(source[j-1],j):
                        momentWhenScrapingSystemEnds = time.time()
                        periodOfScraping = momentWhenScrapingSystemEnds - momentWhenScrapingSystemStarts
                        print(str(i)+":"+str(j)+"/9:499 "+str(periodOfScraping)+" Sec")
                        break
        if i == 1:
            filename = ""
            filename = setCsvTitleRow()

        for j in range(1,500):
            parseOgameGalaxySource(source[j-1],i,j,filename)

def moveToCoordinate(browser,galaxyNumber,systemNumber):
    browser.find_element_by_css_selector("#galaxy_input").send_keys(galaxyNumber)
    browser.find_element_by_css_selector("#system_input").send_keys(systemNumber)
    browser.find_element_by_css_selector("#galaxyHeader > form > div:nth-child(9)").click()

def moveSystem(browser,systemNumber):
    browser.find_element_by_css_selector("#system_input").send_keys(systemNumber)
    browser.find_element_by_css_selector("#galaxyHeader > form > div:nth-child(9)").click()

def setCsvTitleRow():
    today = datetime.datetime.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    hour = str(today.hour)
    minute = str(today.minute)
    second = str(today.second)

    filename = "Galaxy_"+year+"_"+month+"_"+day+"_"+hour+"_"+minute+".csv"
    
    with open(filename, encoding="utf-8",mode='a+') as f:
        print("Gal,Sys,Pla,PlanetName,Moon,UserName,UserRank,AllianceName,AllianceRank,AllianceMember,Vacation,Inactive,LongInactive,Recyclers",file=f)

    return filename

def isIValueSameAsGalaxy(source, i):
    isSame = 0
    bsObject = BeautifulSoup(source, "html.parser")

    galaxyValue = str(bsObject.find("div",{"id":"mobileDiv"}))
    galaxyValue = re.sub(pattern="\n", repl="",string=galaxyValue)
    galaxyValue = re.sub(pattern=".*data-galaxy=\"|\".*", repl="",string=galaxyValue)

    if int(galaxyValue) == int(i):
        isSame = 1
    else:
        isSame = 0

    return isSame

def isIValueDifferentFromGalaxy(source, i):
    bsObject = BeautifulSoup(source, "html.parser")

    galaxyValue = str(bsObject.find("div",{"id":"mobileDiv"}))
    galaxyValue = re.sub(pattern="\n", repl="",string=galaxyValue)
    galaxyValue = re.sub(pattern=".*data-galaxy=\"|\".*", repl="",string=galaxyValue)

    if int(galaxyValue) != int(i):
        isDifferent = 1
    else:
        isDifferent = 0

    return isDifferent

def isJValueSameAsSystem(source,j):
    isSame = 0
    bsObject = BeautifulSoup(source, "html.parser")

    systemValue = str(bsObject.find("div",{"id":"mobileDiv"}))
    systemValue = re.sub(pattern="\n", repl="",string=systemValue)
    systemValue = re.sub(pattern=".*data-system=\"|\".*", repl="",string=systemValue)

    if int(systemValue) == int(j):
        isSame = 1
    else:
        isSame = 0

    return isSame

def isJValueDifferentFromSystem(source,j):
    isEqual = 0
    bsObject = BeautifulSoup(source, "html.parser")

    systemValue = str(bsObject.find("div",{"id":"mobileDiv"}))
    systemValue = re.sub(pattern="\n", repl="",string=systemValue)
    systemValue = re.sub(pattern=".*data-system=\"|\".*", repl="",string=systemValue)

    if int(systemValue) != int(j):
        isDifferent = 1
    else:
        isDifferent = 0

    return isDifferent

def parseOgameGalaxySource(html,galaxyNumber,systemNumber,filename):

        bsObject = BeautifulSoup(html, "html.parser")
            
        # 각 행성을 순환하기(1번~15번)  
        # 왜 그냥 findAll 각각해서 리스트 순환하며 csv 등록하지 않느냐면,
        # 어떤 행성번호는 빈 칸인데 이러면 다른 행성명, 행성유저 등의
        # 리스트가 당겨지기 때문이다.
        # 당연히 문제가 된다. 그래서 행성 1번의 행성명... 이런 식으로 구하는 것.
        

        planetNumber = []
        planetName = []
        isThereMoon = []
        recyclersForDebris = []
        userName = []
        userRank = []
        allianceName = []
        allianceRank = []
        allianceMember = []
        status_vacation = []
        status_inactive = []
        status_longinactive = []
        
        systemSource = bsObject.findAll("tr",{"class":re.compile("^row.*")})

        for planetSource in systemSource:
                # 행성 번호, 행성명, 달, 유저명, 유저랭크, 얼라이언스명, 얼라이언스 랭크, 얼라이언스 멤버,
                # 스테이터스(I광, 휴가), 데브리(수확선 필요량)
                planetNumber.append(getPlanetNumber(planetSource))
                planetName.append(getPlanetName(planetSource))
                isThereMoon.append(getMoon(planetSource))
                userName.append(getUserName(planetSource))
                userRank.append(getUserRank(planetSource))
                allianceName.append(getAllianceName(planetSource))
                allianceRank.append(getAllianceRank(planetSource))
                allianceMember.append(getAllianceMember(planetSource))
                status_vacation.append(getStatus(planetSource,"status_abbr_vacation"))
                status_inactive.append(getStatus(planetSource,"status_abbr_inactive"))
                status_longinactive.append(getStatus(planetSource,"status_abbr_longinactive"))
                recyclersForDebris.append(getRecyclersForDebris(planetSource))

        i = 0
        for i in range(len(planetName)):
                with open(filename, encoding="utf-8",mode='a+') as f:
                        print(",".join([str(galaxyNumber),str(systemNumber),planetNumber[i],planetName[i],isThereMoon[i],\
                                        userName[i],userRank[i],\
                                        allianceName[i],allianceRank[i],allianceMember[i],\
                                        status_vacation[i],status_inactive[i],status_longinactive[i],\
                                        recyclersForDebris[i],]),file=f)
                

def NoneToBlank(string):
        if eq(string, "None") == True:
                return ""
        else:
                return string

def getPlanetNumber(planetSource):
    planetNumber = ""
    planetNumberInHtml = str(planetSource.find("td",{"class":"position js_no_action"}))
    planetNumberInHtml = re.sub(pattern="(<td class=\"position js_no_action\">|</td>)", repl="",string=planetNumberInHtml)
    planetNumber = NoneToBlank(planetNumberInHtml)
    
    return planetNumber

def getPlanetName(planetSource):
    planetName = ""
    planetNameInHtml = str(planetSource.find("div",{"id":re.compile("planet\d+")}))
    planetNameInHtml = re.sub(pattern="\n", repl="",string=planetNameInHtml)
    planetNameInHtml = re.sub(pattern="(.*textNormal\">|<\/span.*div>)", repl="",string=planetNameInHtml)
    planetName = NoneToBlank(planetNameInHtml)
    
    return planetName

def getMoon(planetSource):
    moonStatus = ""
    isThereMoonInHtml = str(planetSource.find("div",{"class":re.compile("moon_a")}))
    if "moon" in isThereMoonInHtml:
        moonStatus = "1"
    else:
        moonStatus = ""

    return moonStatus

def getUserName(planetSource):
    userName = ""
    userNameInHtml = str(planetSource.find("div",{"id":re.compile("player\d+")}))
    userNameInHtml = re.sub(pattern="\n", repl="",string=userNameInHtml)
    userNameInHtml = re.sub(pattern="(.*<h1>|<\/h1>.*|Player: <span>|<\/span>)", repl="",string=userNameInHtml)
    userName = NoneToBlank(userNameInHtml)
    
    return userName

def getUserRank(planetSource):
    userRank = ""
    userRankInHtml = str(planetSource.find("div",{"id":re.compile("player\d+")}))
    userRankInHtml = re.sub(pattern="\n", repl="",string=userRankInHtml)
    userRankInHtml = re.sub(pattern="(.*searchRelId=\d+\">|<\/a><\/li>.*)", repl="",string=userRankInHtml)

    if "Support" in userRankInHtml: # 관리자 예외
        userRank = ""
    elif "sendMail" in userRankInHtml: # 밴 당한 사람은 랭크가 없음.
        userRank = ""
    else:
        userRank = NoneToBlank(userRankInHtml)

    return userRank

def getAllianceName(planetSource):
    allianceName = ""
    allianceNameInHtml = str(planetSource.find("div",{"id":re.compile("alliance\d+")}))
    allianceNameInHtml = re.sub(pattern="\n", repl="",string=allianceNameInHtml)
    allianceNameInHtml = re.sub(pattern="(.*<h1>|<\/h1>.*)", repl="",string=allianceNameInHtml)
    allianceName = NoneToBlank(allianceNameInHtml)
    
    return allianceName

def getAllianceRank(planetSource):
    allianceRank = ""
    allianceRankInHtml = str(planetSource.find("div",{"id":re.compile("alliance\d+")}))
    allianceRankInHtml = re.sub(pattern="\n", repl="",string=allianceRankInHtml)
    allianceRankInHtml = re.sub(pattern="(.*searchRelId=\d+\">|<\/a><\/li>).*", repl="",string=allianceRankInHtml)
    allianceRank = NoneToBlank(allianceRankInHtml)
    
    return allianceRank

def getAllianceMember(planetSource):
    allianceMember = ""
    allianceMemberInHtml = str(planetSource.find("div",{"id":re.compile("alliance\d+")}))
    allianceMemberInHtml = re.sub(pattern="\n", repl="",string=allianceMemberInHtml)
    allianceMemberInHtml = re.sub(pattern="(.*Member: |</li><li><a href=\"allianceInfo.*)", repl="",string=allianceMemberInHtml)
    allianceMember = NoneToBlank(allianceMemberInHtml)
    
    return allianceMember

def getStatus(planetSource, condition):
    status = ""
    statusInHtml = str(planetSource.find("span",{"class":"status"}))

    if condition in statusInHtml:
        status = "1"
    else:
        status = ""

    return status

def getRecyclersForDebris(planetSource):
    recyclersForDebris = ""
    recyclersForDebrisInHtml = str(planetSource.find("li",{"class":"debris-recyclers"}))
    recyclersForDebrisInHtml = recyclersForDebrisInHtml.replace("<li class=\"debris-recyclers\">Recyclers needed: ","").replace("</li>","")
    recyclersForDebris = NoneToBlank(recyclersForDebrisInHtml)
    
    return recyclersForDebris



OgameTools("https://en.ogame.gameforge.com/", "dfo@vomoto.com", "789456")
