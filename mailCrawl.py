from bs4 import BeautifulSoup 
from operator import eq
import re

def ParseHtmlFile():
#TODO 나중에 OgameTools에 합침.
        # 소스 가져오고 종료
        with open("mailCrawl.html",encoding="utf-8") as fp:
            bsObject = BeautifulSoup(fp, "html.parser")
            
        mailsSource = bsObject.findAll("li",{"class":"msg"})

        for mailSource in mailsSource:
            
            getPlanetName(mailSource)
            getPlanetGalaxy(mailSource)
            getPlanetSystem(mailSource)
            getPlanetNumber(mailSource)
            getData(mailSource,"  ") # 플레이어명
            
            getData(mailSource,"Metal: ")
            getData(mailSource,"Crystal: ")
            getData(mailSource,"Deuterium: ")
            print(int(float(getData(mailSource,"Resources: "))/250000)) # 카르고 대 숫자 - 5대 단위로 끊어서
            getData(mailSource,"Resources: ")
            getData(mailSource,"Defence: ")
            getData(mailSource,"Fleets: ")

def getPlanetName(mailSource):
    planetName = ""
    planetNameInHtml = str(mailSource.find("span",{"class":"msg_title blue_txt"}))
    planetNameInHtml = re.sub(pattern="\n", repl="",string=planetNameInHtml)
    planetName = re.sub(pattern="(.*figure>| .*)", repl="",string=planetNameInHtml)

    return planetName

def getPlanetGalaxy(mailSource):
    planetGalaxy = ""
    planetGalaxyInHtml = str(mailSource.find("span",{"class":"msg_title blue_txt"}))
    planetGalaxyInHtml = re.sub(pattern="\n", repl="",string=planetGalaxyInHtml)
    planetGalaxy = re.sub(pattern="(.*\[|:.*)", repl="",string=planetGalaxyInHtml)
    
    return planetGalaxy

def getPlanetSystem(mailSource):
    planetSystem = ""
    planetSystemInHtml = str(mailSource.find("span",{"class":"msg_title blue_txt"}))
    planetSystemInHtml = re.sub(pattern="\n", repl="",string=planetSystemInHtml)
    planetSystem = re.sub(pattern="(.*\[\d+:|:\d+].*)", repl="",string=planetSystemInHtml)

    return planetSystem

def getPlanetNumber(mailSource):
    planetNumber = ""
    planetNumberInHtml = str(mailSource.find("span",{"class":"msg_title blue_txt"}))
    planetNumberInHtml = re.sub(pattern="\n", repl="",string=planetNumberInHtml)
    planetNumber = re.sub(pattern="(.*:|\].*)", repl="",string=planetNumberInHtml)

    return planetNumber


def getData(mailSource, string):
    data = ""
    dataInHtml = str(mailSource.find("span",{"class":"msg_content"}))
    dataInHtml = re.sub(pattern="\n", repl="",string=dataInHtml)
    dataInHtml = re.sub(pattern="(.*"+string+"|<\/span>.*)|\.", repl="",string=dataInHtml)
    data = NoneToBlank(dataInHtml)

    return data

def NoneToBlank(string):
        if eq(string, "None") == True:
                return ""
        else:
                return string

ParseHtmlFile()
