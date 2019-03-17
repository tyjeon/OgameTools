from bs4 import BeautifulSoup
from operator import eq
import os
import re
import time

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

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
    hour = input("Hour\n--> ")
    minute = input("Minute\n--> ")
    second = input("Second\n--> ")

    total_time = 3600*int(hour)+60*int(minute)+int(second)

    while(total_time !=0):
        time.sleep(1)
        total_time = int(total_time) -1
        print(str(total_time)+" 초 남음")
