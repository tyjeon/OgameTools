from bs4 import BeautifulSoup 
from operator import eq
import re
import datetime

def ParseHtmlFile():
#TODO 나중에 OgameTools에 합침.

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
        
        with open("mailCrawl.html",encoding="utf-8") as fp:
            bsObject = BeautifulSoup(fp, "html.parser")
            
        mailsSource = bsObject.findAll("li",{"class":"msg"})
        for mailSource in mailsSource:
            
            planetName.append(getPlanetName(mailSource))
            planetGalaxy.append(getPlanetGalaxy(mailSource))
            planetSystem.append(getPlanetSystem(mailSource))
            planetNumber.append(getPlanetNumber(mailSource))
            playerName.append(getPlayerName(mailSource))
            
            metal.append(getData(mailSource,"Metal: "))
            crystal.append(getData(mailSource,"Crystal: "))
            deuterium.append(getData(mailSource,"Deuterium: "))
            numberOfLargeCargo.append(int(float(getData(mailSource,"Resources: "))/50000))
            numberOfLargeCargo5x.append(int(float(getData(mailSource,"Resources: "))/250000)) # 카르고 대 숫자- 5대 단위로 끊어서
            totalResources.append(getData(mailSource,"Resources: "))
            defence.append(getData(mailSource,"Defence: "))
            fleets.append(getData(mailSource,"Fleets: "))

        filename = ""
        filename = setEspionageCsvTitleRow()   
        for i in range(len(planetName)):
                with open(filename, encoding="utf-8",mode='a+') as f:
                        print(",".join([planetName[i],planetGalaxy[i],planetSystem[i],planetNumber[i],playerName[i],\
                                        metal[i],crystal[i],deuterium[i],str(numberOfLargeCargo[i]),str(numberOfLargeCargo5x[i]),\
                                        totalResources[i],defence[i],fleets[i]]),file=f)

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

def getPlayerName(mailSource):
    playerName = ""
    playerNameInHtml = str(mailSource.find("span",{"class":re.compile("status_*")}))
    playerNameInHtml = re.sub(pattern="\n", repl="",string=playerNameInHtml)
    playerNameInHtml = re.sub(pattern="(<span.*\">|<\/span>)", repl="",string=playerNameInHtml)
    playerName = playerNameInHtml.strip()

    return playerName

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

def setEspionageCsvTitleRow():
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

ParseHtmlFile()
