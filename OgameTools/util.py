import os
from selenium import webdriver
import re
from bs4 import BeautifulSoup
from operator import eq

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def moveToCoordinate(browser,galaxyNumber,systemNumber):
    browser.find_element_by_css_selector("#galaxy_input").send_keys(galaxyNumber)
    browser.find_element_by_css_selector("#system_input").send_keys(systemNumber)
    browser.find_element_by_css_selector("#galaxyHeader > form > div:nth-child(9)").click()

def isIValueSameAsGalaxy(source, i):
    isSame = 0
    bsObject = BeautifulSoup(source, "html.parser")

    argumentsForParsing=[bsObject,["div","id","mobileDiv"],".*data-galaxy=\"|\".*"]
    galaxyValue = parseUsingRegExp(argumentsForParsing)

    if int(galaxyValue) == int(i):
        isSame = 1
    else:
        isSame = 0

    return isSame

def isIValueDifferentFromGalaxy(source, i):
    bsObject = BeautifulSoup(source, "html.parser")

    argumentsForParsing=[bsObject,["div","id","mobileDiv"],".*data-galaxy=\"|\".*"]
    galaxyValue = parseUsingRegExp(argumentsForParsing)

    if int(galaxyValue) != int(i):
        isDifferent = 1
    else:
        isDifferent = 0

    return isDifferent

def isJValueSameAsSystem(source,j):
    isSame = 0
    bsObject = BeautifulSoup(source, "html.parser")

    argumentsForParsing=[bsObject,["div","id","mobileDiv"],".*data-system=\"|\".*"]
    systemValue = parseUsingRegExp(argumentsForParsing)

    if int(systemValue) == int(j):
        isSame = 1
    else:
        isSame = 0

    return isSame

def isJValueDifferentFromSystem(source,j):
    isEqual = 0
    bsObject = BeautifulSoup(source, "html.parser")

    argumentsForParsing=[bsObject,["div","id","mobileDiv"],".*data-system=\"|\".*"]
    systemValue = parseUsingRegExp(argumentsForParsing)

    if int(systemValue) != int(j):
        isDifferent = 1
    else:
        isDifferent = 0

    return isDifferent

def parseUsingRegExp(argumentsForParsing):
    dataSource = str(argumentsForParsing[0].find(argumentsForParsing[1][0],{argumentsForParsing[1][1]:argumentsForParsing[1][2]}))
    dataSource = re.sub(pattern="\n", repl="",string=dataSource)
    dataSource = str(re.sub(pattern=argumentsForParsing[2], repl="",string=dataSource))
    data = NoneToBlank(dataSource)
    return data

def NoneToBlank(string):
        if eq(string, "None") == True:
                return ""
        else:
                return string
