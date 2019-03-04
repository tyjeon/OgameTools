import util

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import datetime
from bs4 import BeautifulSoup

def enter_galaxy_tab(browser):
    print("---------------------------------------------")
    print("Galaxy 메뉴로 최초 이동")
    WebDriverWait(browser, 20). \
                               until(EC.presence_of_element_located((By.CSS_SELECTOR,"#menuTable > li:nth-child(9) > a")))
    browser.find_element_by_css_selector("#menuTable > li:nth-child(9) > a").click()

    loop_galaxy(browser)

def loop_galaxy(browser):
    __start_galaxy = input("시작할 은하 좌표를 입력해주십시오.\n--> ")
    __max_galaxy = input("마지막 은하 좌표를 입력해주십시오.\n--> ")
    __start_system = input("시작할 시스템 좌표를 입력해주십시오.\n--> ")
    __max_system = input("마지막 시스템 좌표를 입력해주십시오.\n--> ")
    
    filename = __set_csv_title_row()
    for i in range(int(__start_galaxy),int(__max_galaxy)+1): # 뒷자리 숫자 -1까지 순환한다. 10 입력시 1~9까지 순환.
        if i == int(__start_galaxy):
            __move_to_coordinates(browser,int(__start_galaxy),1)
        else:
            while(True):
                if util.is_i_value_different_from_galaxy(source[0],i):
                    __move_to_coordinates(browser,i,1)
                    break
        source = []

        if i == int(__start_galaxy):
            k = 1
            for j in range(int(__start_system),int(__max_system)+1):
                __moment_when_scraping_system_starts = time.time()
                source.append("")
                while(True):
                    source[k-1]=browser.page_source
                            
                    if util.is_i_value_same_as_galaxy(source[k-1],i) and util.is_j_value_same_as_system(source[k-1],j):
                        __moment_when_scraping_system_ends = time.time()
                        periodOfScraping = __moment_when_scraping_system_ends - __moment_when_scraping_system_starts
                        print(str(i)+":"+str(j)+"/"+str(__max_galaxy)+":"+str(__max_system)+" "+str(periodOfScraping)+" 초")
                        break
                    else:
                        __move_system(browser,j)
                    time.sleep(0.1)

                __parse_ogame_galaxy_source(source[k-1],i,int(k)-1+int(__start_system),filename)
                k = k+1

        else:
            for j in range(1,int(__max_system)+1):
                __moment_when_scraping_system_starts = time.time()
                source.append("")
                while(True):
                    source[j-1]=browser.page_source
                            
                    if util.is_i_value_same_as_galaxy(source[j-1],i) and util.is_j_value_same_as_system(source[j-1],j):
                        __moment_when_scraping_system_ends = time.time()
                        periodOfScraping = __moment_when_scraping_system_ends - __moment_when_scraping_system_starts
                        print(str(i)+":"+str(j)+"/"+str(__max_galaxy)+":"+str(__max_system)+" "+str(periodOfScraping)+" 초")
                        break
                    else:
                        __move_system(browser,j)
                    time.sleep(0.1)

                __parse_ogame_galaxy_source(source[j-1],i,j,filename)

def __move_to_coordinates(browser,__galaxy_number,__system_number):
    browser.find_element_by_css_selector("#galaxy_input").send_keys(__galaxy_number)
    browser.find_element_by_css_selector("#system_input").send_keys(__system_number)
    browser.find_element_by_css_selector("#galaxyHeader > form > div:nth-child(9)").click()

def __move_system(browser,__system_number):
    browser.find_element_by_css_selector("#system_input").send_keys(__system_number)
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
        print("Gal,Sys,Pla,PlanetName,Moon,UserName,__user_rank,__alliance_name,__alliance_rank,__alliance_member,Vacation,Inactive,LongInactive,Recyclers",file=f)

    return filename

def __parse_ogame_galaxy_source(html,__galaxy_number,__system_number,filename):

        __bs_object = BeautifulSoup(html, "html.parser")
        __planet_number = []
        __planet_name = []
        __is_there_moon = []
        __recyclers_for_debris = []
        __user_name = []
        __user_rank = []
        __alliance_name = []
        __alliance_rank = []
        __alliance_member = []
        __status_vacation = []
        __status_inactive = []
        __status_longinactive = []
        
        __system_source = __bs_object.findAll("tr",{"class":re.compile("^row.*")})

        for __planet_source in __system_source:
                __planet_number.append(__get_planet_number(__planet_source))
                __planet_name.append(__get_planet_name(__planet_source))
                __is_there_moon.append(__get_moon(__planet_source))
                __user_name.append(__get_user_name(__planet_source))
                __user_rank.append(__get_user_rank(__planet_source))
                __alliance_name.append(__get_alliance_name(__planet_source))
                __alliance_rank.append(__get_alliance_rank(__planet_source))
                __alliance_member.append(__get_alliance_member(__planet_source))
                __status_vacation.append(__get_status(__planet_source,"status_abbr_vacation"))
                __status_inactive.append(__get_status(__planet_source,"status_abbr_inactive"))
                __status_longinactive.append(__get_status(__planet_source,"status_abbr_longinactive"))
                __recyclers_for_debris.append(__get_recyclers_for_debris(__planet_source))

        i = 0
        for i in range(len(__planet_name)):
                with open(filename, encoding="utf-8",mode='a+') as f:
                        print(",".join([str(__galaxy_number),str(__system_number),__planet_number[i],__planet_name[i],__is_there_moon[i],\
                                        __user_name[i],__user_rank[i],\
                                        __alliance_name[i],__alliance_rank[i],__alliance_member[i],\
                                        __status_vacation[i],__status_inactive[i],__status_longinactive[i],\
                                        __recyclers_for_debris[i],]),file=f)

def __get_planet_number(__planet_source):
    __arguments_for_parsing=[__planet_source,["td","class","position js_no_action"],"(<td class=\"position js_no_action\">|</td>)"]
    return util.parse_using_regexp(__arguments_for_parsing)

def __get_planet_name(__planet_source):
    __arguments_for_parsing=[__planet_source,["div","id",re.compile("planet\d+")],"(.*textNormal\">|<\/span.*div>)"]
    return util.parse_using_regexp(__arguments_for_parsing)

def __get_moon(__planet_source):
    __arguments_for_parsing=[__planet_source,["div","class",re.compile("moon_a")],""]
    __is_there_moon_in_html = util.parse_using_regexp(__arguments_for_parsing)
    if "moon" in __is_there_moon_in_html:
        __moon_status = "1"
    else:
        __moon_status = ""

    return __moon_status

def __get_user_name(__planet_source):
    __arguments_for_parsing=[planetsource,["div","id",re.compile("player\d+")],".*: <span>|<\/span>.*"]
    return util.parse_using_regexp(__arguments_for_parsing)

def __get_user_rank(__planet_source):
    __arguments_for_parsing=[__planet_source,["div","id",re.compile("player\d+")],"(.*searchRelId=\d+\">|<\/a><\/li>.*)"]
    __user_rank_in_html = util.parse_using_regexp(__arguments_for_parsing)

    if "page=support" in __user_rank_in_html: # 관리자 예외
        __user_rank = ""
    elif "sendMail" in __user_rank_in_html: # 밴 당한 사람은 랭크가 없음.
        __user_rank = ""
    else:
        __user_rank = __user_rank_in_html

    return __user_rank

def __get_alliance_name(__planet_source):
    __arguments_for_parsing=[__planet_source,["div","id",re.compile("alliance\d+")],"(.*<h1>|<\/h1>.*)"]
    return util.parse_using_regexp(__arguments_for_parsing)

def __get_alliance_rank(__planet_source):
    __arguments_for_parsing=[__planet_source,["div","id",re.compile("alliance\d+")],"(.*searchRelId=\d+\">|<\/a><\/li>).*"]
    return util.parse_using_regexp(__arguments_for_parsing)

def __get_alliance_member(__planet_source):
    __arguments_for_parsing=[__planet_source,["div","id",re.compile("alliance\d+")],"(.*Member: |</li><li><a href=\"allianceInfo.*)"]
    return util.parse_using_regexp(__arguments_for_parsing)

def __get_status(__planet_source, condition):
    __arguments_for_parsing=[__planet_source,["span","class","status"],""]
    __status_in_html = util.parse_using_regexp(__arguments_for_parsing)
    
    if condition in __status_in_html:
        status = "1"
    else:
        status = ""

    return status

def __get_recyclers_for_debris(__planet_source):
    __arguments_for_parsing=[__planet_source,["li","class","debris-recyclers"],".*Recyclers needed: |</li>"]
    return util.parse_using_regexp(__arguments_for_parsing)
