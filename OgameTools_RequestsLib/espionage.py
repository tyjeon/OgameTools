from bs4 import BeautifulSoup
import re
import os
import csv
import time
import random

def espionage(s,server_address):
    print("-------------------------------------------------------------------")
    print("Espionage".center(67))
    print("-------------------------------------------------------------------")
    target_coordinates = get_target_info()
    post_url = "https://{}.ogame.gameforge.com/game/index.php?page=minifleet&ajax=1".format(server_address)
    
    for i in range(len(target_coordinates)):
        fleet_token = get_fleet_token(s)
        
        payload = {'mission':'6',
                   'galaxy':target_coordinates[i][0],
                   'system':target_coordinates[i][1],
                   'position':target_coordinates[i][2],
                   'type':'1',
                   'shipCount':'1',
                   'token':fleet_token}

        espionage_request = s.post(post_url, data=payload)
        if espionage_request.status_code == 200:
            print("Espionage mission to {}:{}:{}.".format(target_coordinates[i][0],target_coordinates[i][1],target_coordinates[i][2]))
        else:
            print("Error Occurred.")
        time.sleep(random.randrange(10,20)*0.1)

def get_target_info():
    galaxys = []
    systems = []
    positions = []
    if os.path.isfile("espionage.csv"):
        with open('espionage.csv', 'r') as r:
            csv_content=csv.reader(r)
            for row in csv_content:
                galaxys.append(row[0])
                systems.append(row[1])
                positions.append(row[2])
    else:
            print("We need 'espionage.csv' which has target coordinates.")
            return 0

    target_coordinates = []
    print("Target Coordinates")
    for i in range(len(galaxys)):
        target_coordinates.append([galaxys[i],systems[i],positions[i]])
        print(target_coordinates[i])

    return target_coordinates

def get_fleet_token(s):
    html = s.get("https://s1-en.ogame.gameforge.com/game/index.php?page=galaxy")
    bs_object = BeautifulSoup(html.text,"html.parser")
    scripts = bs_object.findAll("script",{"type":"text/javascript"})

    for script in scripts:
        if "miniFleetToken" in str(script):
            script = re.sub("\n","",str(script))
            fleet_token = re.sub(".*miniFleetToken=\"|\".*","",script)
            return fleet_token
