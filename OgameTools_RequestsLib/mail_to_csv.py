import util

import requests
from bs4 import BeautifulSoup

import time
import random
import datetime
import re
import os

def mail_to_csv(s,server_address):
    print("-------------------------------------------------------------------")
    print("Mail To Csv".center(67))
    print("-------------------------------------------------------------------")
    html = []
    page_number = 1
    while True:
        payload = {'messageId': '-1',
                   'tabid': '20',
                   'action': '107',
                   'pagination': page_number,
                   'ajax': '1'}
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        
        request_url = "https://{}.ogame.gameforge.com/game/index.php?page=messages".format(server_address)
        html_source = s.post(request_url, data=payload, headers=headers)
        bs_object = BeautifulSoup(html_source.text, "html.parser")
        last_page = get_total_page_number(bs_object)

        html.append(html_source.text)
        print("Proceeding page {}/{}...".format(str(page_number),str(last_page)))
        if int(page_number) == int(last_page):
            break
        else:
            page_number += 1
            time.sleep(random.randrange(10,20)*1)
            
    filename = set_title()
    for i in range(0,len(html)):
        save_information(html[i], filename)

def save_information(html, filename):
    
    bs_object = BeautifulSoup(html, "html.parser")
    mailsSources = bs_object.findAll("li",{"class":"msg"})
    
    for mailSource in mailsSources:
        mailHead = mailSource.find("div",{"class":"msg_head"}) # 정찰 미션 결과가 아닌 메세지는 넘김.
        if not "Espionage report from" in str(mailHead):
            continue
        
        planet_name = get_planet_name_in_mail(mailSource)
        planet_galaxy = get_planet_galaxy_in_mail(mailSource)
        planet_system = get_planet_system_in_mail(mailSource)
        planet_number = get_planet_number_in_mail(mailSource)
        player_name = get_player_name_in_mail(mailSource)
        metal = get_data_in_mail(mailSource,"Metal: ")
        crystal = get_data_in_mail(mailSource,"Crystal: ")
        deuterium = get_data_in_mail(mailSource,"Deuterium: ")
        number_of_large_cargo = str(int(float(get_data_in_mail(mailSource,"Resources: "))/50000))
        number_of_large_cargo_5x = str(int(float(get_data_in_mail(mailSource,"Resources: "))/250000))
        total_resources = get_data_in_mail(mailSource,"Resources: ")
        defence = get_data_in_mail(mailSource,"Defence: ")
        fleets = get_data_in_mail(mailSource,"Fleets: ")


        with open("Espionage/"+filename, encoding="utf-8",mode='a+') as f:
            print(",".join([planet_name,planet_galaxy,planet_system,planet_number,player_name,\
                            metal,crystal,deuterium,number_of_large_cargo,number_of_large_cargo_5x,\
                            total_resources,defence,fleets]),file=f)

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
    arguments_for_parsing=[mailSource,["span","class",re.compile("status_*")],"(<span.*\">\s+|<\/span>)"]
    return util.parse_using_regexp(arguments_for_parsing)

def get_data_in_mail(mailSource, string):
    arguments_for_parsing=[mailSource,["span","class",re.compile("msg_content")],"(.*"+string+"|<\/span>.*)|\."]
    data_in_html = util.parse_using_regexp(arguments_for_parsing)
    
    if "compacting" in data_in_html: # 정탐 레벨 낮음
        data = "Low_Espionage_Level"
    else:
        data = data_in_html

    return data

def set_title():
    if not os.path.isdir("Espionage"):
        os.mkdir("Espionage")
        
    today = datetime.datetime.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    hour = str(today.hour)
    minute = str(today.minute)
    second = str(today.second)

    filename = "Espionage_"+year+"_"+month+"_"+day+"_"+hour+"_"+minute+".csv"

    with open("Espionage/"+filename, encoding="utf-8",mode='a+') as f:
        print("Planet,Gal,Sys,Pla,Player,Metal,Crystal,Deuterium,LargeCargo,LargeCargo5x,Resources,Defence,Fleets",file=f)

    return filename
