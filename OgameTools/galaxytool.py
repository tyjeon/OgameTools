import util

from selenium import webdriver
import time
import re
import datetime
from bs4 import BeautifulSoup

def enter_galaxy_tab(browser):
    print("Galaxy 메뉴로 이동")
    time.sleep(3)

    browser.find_element_by_css_selector("#menuTable > li:nth-child(9) > a").click()
    time.sleep(3)

    loop_galaxy(browser)

def loop_galaxy(browser):
    print("현재 테스트케이스로 갤럭시 1~2, 시스템 1~2까지만 순환합니다.")
    for i in range(1,3): # 뒷자리 숫자 -1까지 순환한다. 10 입력시 1~9까지 순환.
        if(i>=2):
            while(True):
                if util.is_i_value_different_from_galaxy(source[j-1],i):
                    moveToCoordinate(browser,i,1)
                    break
        else:
            moveToCoordinate(browser,1,1)

        source = []
        for j in range(1,3):
            momentWhenScrapingSystemStarts = time.time()
            source.append("")
            if j==1:
                while(True):
                    source[j-1]=browser.page_source
                    if util.is_i_value_different_from_galaxy(source[j-1],1):
                        source[j-1]=browser.page_source
                        periodOfScraping = momentWhenScrapingSystemEnds - momentWhenScrapingSystemStarts
                        print(str(i)+":"+str(j)+"/9:499 "+str(periodOfScraping)+" Sec")
                        break
            elif j>=2:
                while(True):
                    if j>=2:
                        source[j-1]=browser.page_source
                                
                    if util.is_j_value_different_from_system(source[j-1],j):
                        moveSystem(browser,j)

                    if util.is_i_value_same_as_galaxy(source[j-1],i) and util.is_j_value_same_as_system(source[j-1],j):
                        momentWhenScrapingSystemEnds = time.time()
                        periodOfScraping = momentWhenScrapingSystemEnds - momentWhenScrapingSystemStarts
                        print(str(i)+":"+str(j)+"/9:499 "+str(periodOfScraping)+" Sec")
                        break
        if i == 1:
            filename = ""
            filename = setCsvTitleRow()

        for j in range(1,3):
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

def getPlanetNumber(planetSource):
    argumentsForParsing=[planetSource,["td","class","position js_no_action"],"(<td class=\"position js_no_action\">|</td>)"]
    return util.parse_using_regexp(argumentsForParsing)

def getPlanetName(planetSource):
    argumentsForParsing=[planetSource,["div","id",re.compile("planet\d+")],"(.*textNormal\">|<\/span.*div>)"]
    return util.parse_using_regexp(argumentsForParsing)

def getMoon(planetSource):
    argumentsForParsing=[planetSource,["div","class",re.compile("moon_a")],""]
    isThereMoonInHtml = util.parse_using_regexp(argumentsForParsing)
    if "moon" in isThereMoonInHtml:
        moonStatus = "1"
    else:
        moonStatus = ""

    return moonStatus

def getUserName(planetSource):
    argumentsForParsing=[planetSource,["div","id",re.compile("player\d+")],"(.*<h1>|<\/h1>.*|Player: <span>|<\/span>)"]
    return util.parse_using_regexp(argumentsForParsing)

def getUserRank(planetSource):
    argumentsForParsing=[planetSource,["div","id",re.compile("player\d+")],"(.*searchRelId=\d+\">|<\/a><\/li>.*)"]
    userRankInHtml = util.parse_using_regexp(argumentsForParsing)

    if "Support" in userRankInHtml: # 관리자 예외
        userRank = ""
    elif "sendMail" in userRankInHtml: # 밴 당한 사람은 랭크가 없음.
        userRank = ""
    else:
        userRank = userRankInHtml

    return userRank

def getAllianceName(planetSource):
    argumentsForParsing=[planetSource,["div","id",re.compile("alliance\d+")],"(.*<h1>|<\/h1>.*)"]
    return util.parse_using_regexp(argumentsForParsing)

def getAllianceRank(planetSource):
    argumentsForParsing=[planetSource,["div","id",re.compile("alliance\d+")],"(.*searchRelId=\d+\">|<\/a><\/li>).*"]
    return util.parse_using_regexp(argumentsForParsing)

def getAllianceMember(planetSource):
    argumentsForParsing=[planetSource,["div","id",re.compile("alliance\d+")],"(.*Member: |</li><li><a href=\"allianceInfo.*)"]
    return util.parse_using_regexp(argumentsForParsing)

def getStatus(planetSource, condition):
    argumentsForParsing=[planetSource,["span","class","status"],""]
    statusInHtml = util.parse_using_regexp(argumentsForParsing)
    
    if condition in statusInHtml:
        status = "1"
    else:
        status = ""

    return status

def getRecyclersForDebris(planetSource):
    argumentsForParsing=[planetSource,["li","class","debris-recyclers"],".*Recyclers needed: |</li>"]
    return util.parse_using_regexp(argumentsForParsing)
