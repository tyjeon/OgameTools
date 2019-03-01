import util

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import time
import datetime
import re

def mail_to_csv(browser):
    print("----------------------------------------")
    print("메일함으로 최초 이동")
    browser.get("https://s1-en.ogame.gameforge.com/game/index.php?page=messages")
    WebDriverWait(browser, 20). \
                   until(EC.presence_of_element_located((By.CSS_SELECTOR,"#ui-id-23")))
    
    __planet_name = []
    __planet_galaxy = []
    __planet_system = []
    __planet_number = []
    __player_name = []
    __metal = []
    __crystal = []
    __deuterium = []
    __number_of_large_cargo = []
    __number_of_large_cargo_5x = []
    __total_resources = []
    __defence = []
    __fleets = []
    

    if is_in_the_right_page(browser,1):
        source = browser.page_source
        bs_object = BeautifulSoup(source, "html.parser")
        total_page = get_total_page_number(bs_object)
    
    for i in range(0,int(total_page)):
        if is_in_the_right_page(browser,i+1):
            source = browser.page_source
            bs_object = BeautifulSoup(source, "html.parser")
            mailsSources = bs_object.findAll("li",{"class":"msg"})
        
        print(str(i+1) + "/" + str(int(total_page)*2) + " 메일함의 "+str(i+1)+"/"+str(total_page)+" 페이지 진행 중...", end = " ")
    
        for mailSource in mailsSources:
            mailHead = mailSource.find("div",{"class":"msg_head"}) # 정찰 미션 결과가 아닌 메세지는 넘김.
        if not "Espionage report from" in str(mailHead):
            continue
        
        __planet_name.append(get_planet_name_in_mail(mailSource))
        __planet_galaxy.append(get_planet_galaxy_in_mail(mailSource))
        __planet_system.append(get_planet_system_in_mail(mailSource))
        __planet_number.append(get_planet_number_in_mail(mailSource))
        __player_name.append(get_player_name_in_mail(mailSource))
        
        __metal.append(get_data_in_mail(mailSource,"__metal: "))
        __crystal.append(get_data_in_mail(mailSource,"Crystal: "))
        __deuterium.append(get_data_in_mail(mailSource,"Deuterium: "))
        __number_of_large_cargo.append(int(float(get_data_in_mail(mailSource,"Resources: "))/50000))
        __number_of_large_cargo_5x.append(int(float(get_data_in_mail(mailSource,"Resources: "))/250000)) # 카르고 대 숫자- 5대 단위로 끊어서
        __total_resources.append(get_data_in_mail(mailSource,"Resources: "))
        __defence.append(get_data_in_mail(mailSource,"Defence: "))
        __fleets.append(get_data_in_mail(mailSource,"Fleets: "))

        print("완료.")
        
        if int(total_page) != 1:
            browser.find_element_by_css_selector("#fleetsgenericpage > ul > ul:nth-child(1) > li:nth-child(4)").click()
            WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#ui-id-23")))
            time.sleep(5)

    filename = set_espionage_csv_title_row()
    for j in range(len(__planet_name)):
        print(str(int(total_page)+j+1) + "/" + str(int(total_page)*2) + \
              "메일함의 "+str(i+1)+"/"+str(total_page)+" 페이지 저장 중...", end = " ")
        with open(filename, encoding="utf-8",mode='a+') as f:
            print(",".join([__planet_name[j],__planet_galaxy[j],__planet_system[j],__planet_number[j],__player_name[j],\
                    __metal[j],__crystal[j],__deuterium[j],str(__number_of_large_cargo[j]),str(__number_of_large_cargo_5x[j]),\
                    __total_resources[j],__defence[j],__fleets[j]]),file=f)
        print("완료.")

def is_in_the_right_page(browser, page_number):
    while(True):
        source = browser.page_source
        bs_object = BeautifulSoup(source, "html.parser")
        if str(get_current_page_number(bs_object)) == str(page_number):
            return 1

def get_current_page_number(bs_object):
    arguments_for_parsing=[bs_object,["li","class","curPage"],"(.*data-tab=\"\d*\">|\/.*)"]
    return util.parse_using_regexp(arguments_for_parsing)

def get_total_page_number(bs_object):
    arguments_for_parsing=[bs_object,["li","class","curPage"],"(.*data-tab=\"\d*\">\d*\/|<\/li>.*)"]
    return util.parse_using_regexp(arguments_for_parsing)

def get_planet_name_in_mail(mailSource):
    arguments_for_parsing=[mailSource,["span","class","msg_title blue_txt"],"(.*figure>| .*)"]
    return util.parse_using_regexp(arguments_for_parsing)

def get_planet_galaxy_in_mail(mailSource):
    arguments_for_parsing=[mailSource,["span","class","msg_title blue_txt"],"(.*\[|:.*)"]
    return util.parse_using_regexp(arguments_for_parsing)

def get_planet_system_in_mail(mailSource):
    arguments_for_parsing=[mailSource,["span","class","msg_title blue_txt"],"(.*\[\d+:|:\d+].*)"]
    return util.parse_using_regexp(arguments_for_parsing)
    
def get_planet_number_in_mail(mailSource):
    arguments_for_parsing=[mailSource,["span","class","msg_title blue_txt"],"(.*:|\].*)"]
    return util.parse_using_regexp(arguments_for_parsing)

def get_player_name_in_mail(mailSource):
    arguments_for_parsing=[mailSource,["span","class",re.compile("status_*")],"(<span.*\">|<\/span>)"]
    return util.parse_using_regexp(arguments_for_parsing)

def get_data_in_mail(mailSource, string):
    arguments_for_parsing=[mailSource,["span","class",re.compile("msg_content")],"(.*"+string+"|<\/span>.*)|\."]
    data_in_html = util.parse_using_regexp(arguments_for_parsing)
    
    if "compacting" in data_in_html: # 정탐 레벨 낮음
        data = "Low_Espionage_Level"
    else:
        data = data_in_html

    return data

def set_espionage_csv_title_row():
    today = datetime.datetime.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    hour = str(today.hour)
    minute = str(today.minute)
    second = str(today.second)

    filename = "Espionage_"+year+"_"+month+"_"+day+"_"+hour+"_"+minute+".csv"

    with open(filename, encoding="utf-8",mode='a+') as f:
        print("Planet,Gal,Sys,Pla,Player,Metal,Crystal,Deuterium,LargeCargo,LargeCargo5x,Resources,Defence,Fleets",file=f)

    return filename
