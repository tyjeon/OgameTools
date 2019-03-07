import os
import requests

os.mkdir("OgameTools")
os.mkdir("OgameTools/OgameTools")

def download_file(url,filename):
    s = requests.Session()
    file_url = s.get(url)
    
    with open("OgameTools/OgameTools/"+filename, 'wb') as f:
        f.write(file_url.content)

    print(filename+" downloaded.")

if __name__ == "__main__":
    url = ["https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/autoattack.py?token=AtNo3CQvaFVXzneCeF3Jn0C5YFQArDdNks5cgPQIwA%3D%3D",
           "https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/espionage.py?token=AtNo3FxL47_h0jAOJEnVJjD-QZh5a7u5ks5cgPRNwA%3D%3D",
           "https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/galaxytool.py?token=AtNo3AQyBJDjqlvlN8KA2NCNwa-tNodbks5cgPSawA%3D%3D",
           "https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/loginogame.py?token=AtNo3HOPyrvZZEehkDdy4vlC_SfVs59Jks5cgPSmwA%3D%3D",
           "https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/mailtocsv.py?token=AtNo3C6EJ_7MAm4hfj0aNlyRFT8X5sZyks5cgPSmwA%3D%3D",
           "https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/main.py?token=AtNo3AEGK-5tK4H4IZLSkk7F1sUO7Dzkks5cgPSnwA%3D%3D",
           "https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/preparewebdriver.py?token=AtNo3E2kEbkI4AXDEh7GO-xl9nAvNcRfks5cgPSnwA%3D%3D",
           "https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/testcase.py?token=AtNo3JfmkxPs4zMI-rHJtPOFxkWpQNdNks5cgPSowA%3D%3D",
           "https://raw.githubusercontent.com/taeyongjeon/OgameTools/master/OgameTools/util.py?token=AtNo3NR8hKMwf7NReneLjqRli14uuaioks5cgPSpwA%3D%3D",
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
    
    for i in range(0,len(url)):
        download_file(url[i],filename[i])
