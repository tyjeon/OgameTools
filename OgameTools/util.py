from selenium import webdriver
from bs4 import BeautifulSoup
from operator import eq
import os
import re
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
def move_to_coordinates(browser,galaxyNumber,systemNumber):
    browser.find_element_by_css_selector("#galaxy_input").send_keys(galaxyNumber)
    browser.find_element_by_css_selector("#system_input").send_keys(systemNumber)
    browser.find_element_by_css_selector("#galaxyHeader > form > div:nth-child(9)").click()

def is_i_value_same_as_galaxy(source, i):
    isSame = 0
    bsObject = BeautifulSoup(source, "html.parser")

    argumentsForParsing=[bsObject,["div","id","mobileDiv"],".*data-galaxy=\"|\".*"]
    galaxyValue = parse_using_regexp(argumentsForParsing)

    if int(galaxyValue) == int(i):
        isSame = 1
    else:
        isSame = 0

    return isSame

def is_i_value_different_from_galaxy(source, i):
    bsObject = BeautifulSoup(source, "html.parser")

    argumentsForParsing=[bsObject,["div","id","mobileDiv"],".*data-galaxy=\"|\".*"]
    galaxyValue = parse_using_regexp(argumentsForParsing)

    if int(galaxyValue) != int(i):
        isDifferent = 1
    else:
        isDifferent = 0

    return isDifferent

def is_j_value_same_as_system(source,j):
    isSame = 0
    bsObject = BeautifulSoup(source, "html.parser")

    argumentsForParsing=[bsObject,["div","id","mobileDiv"],".*data-system=\"|\".*"]
    systemValue = parse_using_regexp(argumentsForParsing)

    if int(systemValue) == int(j):
        isSame = 1
    else:
        isSame = 0

    return isSame

def is_j_value_different_from_system(source,j):
    isEqual = 0
    bsObject = BeautifulSoup(source, "html.parser")

    argumentsForParsing=[bsObject,["div","id","mobileDiv"],".*data-system=\"|\".*"]
    systemValue = parse_using_regexp(argumentsForParsing)

    if int(systemValue) != int(j):
        isDifferent = 1
    else:
        isDifferent = 0

    return isDifferent

def parse_using_regexp(argumentsForParsing):
    dataSource = str(argumentsForParsing[0].find(argumentsForParsing[1][0],{argumentsForParsing[1][1]:argumentsForParsing[1][2]}))
    dataSource = re.sub(pattern="\n", repl="",string=dataSource)
    dataSource = str(re.sub(pattern=argumentsForParsing[2], repl="",string=dataSource))
    data = change_none_to_blank(dataSource)
    return data

def change_none_to_blank(string):
        if eq(string, "None") == True:
                return ""
        else:
                return string

def wait_time(): 
    hour = input("시간 입력\n--> ")
    minute = input("분\n--> ")
    second = input("초\n--> ")

    total_time = 3600*int(hour)+60*int(minute)+int(second)

    while(total_time !=0):
        time.sleep(1)
        total_time = int(totaltime) -1
        print(str(totaltime)+" 초 남음")
