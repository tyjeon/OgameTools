import util

from selenium import webdriver
import time
import re
import datetime
from bs4 import BeautifulSoup

def enter_galaxy_tab(browser):
    print("Galaxy 메뉴로 최초 이동")
    time.sleep(3)

    browser.find_element_by_css_selector("#menuTable > li:nth-child(9) > a").click()
    time.sleep(3)

    loop_galaxy(browser)

def loop_galaxy(browser):
    print("현재 테스트케이스로 갤럭시 1~2, 시스템 1~2까지만 순환합니다.")
    for i in range(1,3): # 뒷자리 숫자 -1까지 순환한다. 10 입력시 1~9까지 순환.
        if i==1:
            __move_to_coordinates(browser,1,1)
        else:
            while(True):
                if util.is_i_value_different_from_galaxy(source[j-1],i):
                    __move_to_coordinates(browser,i,1)
                    source = []
                    break
        source = []
        for j in range(1,3):
            __moment_when_scraping_system_starts = time.time()
            source.append("")
            while(True):
                source[j-1]=browser.page_source
                if util.is_j_value_different_from_system(source[j-1],j):
                    __move_system(browser,j)
                        
                if util.is_i_value_same_as_galaxy(source[j-1],i) and util.is_j_value_same_as_system(source[j-1],j):
                    __moment_when_scraping_system_ends = time.time()
                    periodOfScraping = __moment_when_scraping_system_ends - __moment_when_scraping_system_starts
                    print(str(i)+":"+str(j)+"/9:499 "+str(periodOfScraping)+" Sec")
                    break

        if i == 1:
            filename = __set_csv_title_row()

        for j in range(1,3):
            parseOgameGalaxySource(source[j-1],i,j,filename)

def __move_to_coordinates(browser,galaxyNumber,systemNumber):
    browser.find_element_by_css_selector("#galaxy_input").send_keys(galaxyNumber)
    browser.find_element_by_css_selector("#system_input").send_keys(systemNumber)
    browser.find_element_by_css_selector("#galaxyHeader > form > div:nth-child(9)").click()

def __move_system(browser,systemNumber):
    browser.find_element_by_css_selector("#system_input").send_keys(systemNumber)
    browser.find_element_by_css_selector("#galaxyHeader > form > div:nth-child(9)").click()

def __set_csv_title_row():
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

        for planet_source in systemSource:
                planetNumber.append(getPlanetNumber(planet_source))
                planetName.append(getPlanetName(planet_source))
                isThereMoon.append(getMoon(planet_source))
                userName.append(getUserName(planet_source))
                userRank.append(getUserRank(planet_source))
                allianceName.append(__get_alliance_name(planet_source))
                allianceRank.append(__get_alliance_rank(planet_source))
                allianceMember.append(__get_alliance_member(planet_source))
                status_vacation.append(getStatus(planet_source,"status_abbr_vacation"))
                status_inactive.append(getStatus(planet_source,"status_abbr_inactive"))
                status_longinactive.append(getStatus(planet_source,"status_abbr_longinactive"))
                recyclersForDebris.append(getRecyclersForDebris(planet_source))

        i = 0
        for i in range(len(planetName)):
                with open(filename, encoding="utf-8",mode='a+') as f:
                        print(",".join([str(galaxyNumber),str(systemNumber),planetNumber[i],planetName[i],isThereMoon[i],\
                                        userName[i],userRank[i],\
                                        allianceName[i],allianceRank[i],allianceMember[i],\
                                        status_vacation[i],status_inactive[i],status_longinactive[i],\
                                        recyclersForDebris[i],]),file=f)

def getPlanetNumber(planet_source):
    arguments_for_parsing=[planet_source,["td","class","position js_no_action"],"(<td class=\"position js_no_action\">|</td>)"]
    return util.parse_using_regexp(arguments_for_parsing)

def getPlanetName(planet_source):
    arguments_for_parsing=[planet_source,["div","id",re.compile("planet\d+")],"(.*textNormal\">|<\/span.*div>)"]
    return util.parse_using_regexp(arguments_for_parsing)

def getMoon(planet_source):
    arguments_for_parsing=[planet_source,["div","class",re.compile("moon_a")],""]
    isThereMoonInHtml = util.parse_using_regexp(arguments_for_parsing)
    if "moon" in isThereMoonInHtml:
        moonStatus = "1"
    else:
        moonStatus = ""

    return moonStatus

def getUserName(planet_source):
    arguments_for_parsing=[planet_source,["div","id",re.compile("player\d+")],"(.*<h1>|<\/h1>.*|Player: <span>|<\/span>)"]
    return util.parse_using_regexp(arguments_for_parsing)

def getUserRank(planet_source):
    arguments_for_parsing=[planet_source,["div","id",re.compile("player\d+")],"(.*searchRelId=\d+\">|<\/a><\/li>.*)"]
    userRankInHtml = util.parse_using_regexp(arguments_for_parsing)

    if "Support" in userRankInHtml: # 관리자 예외
        userRank = ""
    elif "sendMail" in userRankInHtml: # 밴 당한 사람은 랭크가 없음.
        userRank = ""
    else:
        userRank = userRankInHtml

    return userRank

def __get_alliance_name(planet_source):
    arguments_for_parsing=[planet_source,["div","id",re.compile("alliance\d+")],"(.*<h1>|<\/h1>.*)"]
    return util.parse_using_regexp(arguments_for_parsing)

def __get_alliance_rank(planet_source):
    arguments_for_parsing=[planet_source,["div","id",re.compile("alliance\d+")],"(.*searchRelId=\d+\">|<\/a><\/li>).*"]
    return util.parse_using_regexp(arguments_for_parsing)

def __get_alliance_member(planet_source):
    arguments_for_parsing=[planet_source,["div","id",re.compile("alliance\d+")],"(.*Member: |</li><li><a href=\"allianceInfo.*)"]
    return util.parse_using_regexp(arguments_for_parsing)

def getStatus(planet_source, condition):
    arguments_for_parsing=[planet_source,["span","class","status"],""]
    __status_in_html = util.parse_using_regexp(arguments_for_parsing)
    
    if condition in __status_in_html:
        status = "1"
    else:
        status = ""

    return status

def getRecyclersForDebris(planet_source):
    arguments_for_parsing=[planet_source,["li","class","debris-recyclers"],".*Recyclers needed: |</li>"]
    return util.parse_using_regexp(arguments_for_parsing)
