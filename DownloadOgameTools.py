import time
import requests
import os
import shutil
from bs4 import BeautifulSoup
import re

def check_folder():
    if os.path.isdir("OgameTools"):
        shutil.rmtree("OgameTools")
    os.mkdir("OgameTools")
    
def download_driver():
    file_url = requests.Session().get("https://github.com/taeyongjeon/ScrapingCobeblocksPython/raw/master/chromedriver.exe")

    with open("chromedriver.exe", 'wb') as f:
        f.write(file_url.content)
    
def download_file(session,url,filename):
    file_url = session.get(url)

    with open("OgameTools/"+filename, 'wb') as f:
        f.write(file_url.content)

    print(filename+" downloaded.")

def get_token(s):
    html = s.get('https://github.com/login')
    bs_object = BeautifulSoup(html.text,'html.parser')
    token_source = bs_object.findAll("",{"name":"authenticity_token"})
    token_source = re.sub(pattern="\n", repl="",string=str(token_source))
    token = str(re.sub(pattern=".*authenticity_token\" type=\"hidden\" value=\"|\".*", repl="",string=token_source))
    
    return token        
    

if __name__=='__main__':
    url = ["https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/autoattack.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/espionage.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/galaxytool.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/loginogame.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/mailtocsv.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/main.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/preparewebdriver.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/testcase.py",
           "https://github.com/taeyongjeon/OgameTools/raw/master/OgameTools/util.py",
           "https://github.com/taeyongjeon/ScrapingCobeblocksPython/raw/master/chromedriver.exe"]
    filename = ["autoattack.py",
                "espionage.py",
                "galaxytool.py",
                "loginogame.py",
                "mailtocsv.py",
                "main.py",
                "preparewebdriver.py",
                "testcase.py",
                "util.py",
                "chromedriver.exe"]

    check_folder()
    with requests.Session() as s:
        token = get_token(s)
        payload = {'authenticity_token':token,
                   'login':'taeyongjeon',
                   'password':'cilarnycstme24*'}

        login_request = s.post('https://github.com/session', data=payload)
        
        for i in range(0,len(url)):
            download_file(s,url[i],filename[i])
