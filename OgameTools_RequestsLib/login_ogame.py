import requests
import re

def login_ogame(s):
    print("-------------------------------------------------------------------")
    print("Login".center(67))
    print("-------------------------------------------------------------------")
    cookies = post_login(s)
    
    accounts_info = get_accounts_info(s)
    playing_servers_info = get_playing_servers_info(s,accounts_info)
    
    show_servers(playing_servers_info,accounts_info)
    select_server = int(input("\nSelect Server Number : ")) - 1

    connect_server_payload = [accounts_info[2][select_server],\
                              accounts_info[0][select_server],\
                              accounts_info[1][select_server],\
                              playing_servers_info[0][select_server]]
    post_server(s, cookies, connect_server_payload)

def post_login(s):
    login_email = input("Input Email : ")
    login_password = input("Input Password : ")
    payload = {'credentials[email]':login_email,
               'credentials[password]':login_password,
               'autologin':'false',
               'language':'en',
               'kid':''}

    post_url = "https://lobby-api.ogame.gameforge.com/users"
    login_request = s.post(post_url, data=payload)

    if login_request.status_code == 200:
        print("Login... Done.")

    return login_request.cookies

def get_accounts_info(s):
    accounts_json_url = "https://lobby-api.ogame.gameforge.com/users/me/accounts"
    accounts_json = s.get(accounts_json_url)
    
    accounts = accounts_json.text.split("},")
    
    language = []
    server_number = []
    gameAccountId = []
    user_name = []

    for i in range(0,len(accounts)):
        if "language" in accounts[i]:
            language.append(re.sub(".*language\":\"|\".*","",accounts[i]))
            
        if "number" in accounts[i]:
            server_number.append(re.sub(".*number\":|\}.*","",accounts[i]))
            
        if "gameAccountId" in accounts[i]:
            gameAccountId.append(re.sub(".*gameAccountId\":|,.*","",accounts[i]))
            
        if "name" in accounts[i]:
            user_name.append(re.sub(".*name\":\"|\".*","",accounts[i]))
    
    accounts_info = [language,server_number,gameAccountId,user_name]

    return accounts_info

def get_playing_servers_info(s,accounts_info):
    server_name = []
    player_count = []
    players_online = []
    
    servers_json = s.get("https://lobby-api.ogame.gameforge.com/servers")
    servers = servers_json.text.split("},")

    for i in range(0,len(servers)):
        for j in range(0,len(accounts_info[0])):
            player_info = [accounts_info[0][j],accounts_info[1][j]]
            if is_playing_server(player_info, servers[i]):
                server_name.append(re.sub(".*name\":\"|\".*","",servers[i]))
                players_online.append(re.sub(".*playersOnline\":|,.*","",servers[i]))
                player_count.append(re.sub(".*playerCount\":|,.*","",servers[i]))
                
    playing_servers_info = [server_name,player_count,players_online]
    return playing_servers_info

def is_playing_server(player_info,server_info):
    return "number\":{},".format(player_info[1]) in server_info and "language\":\"{}".format(player_info[0]) in server_info

def show_servers(playing_servers_info,accounts_info):
    print("\n{} {} {} {} {} {}".format("Number","Server".ljust(12),"Username".ljust(25),"Langauge","Online","Total"))
        
    for i in range(0,len(playing_servers_info[0])):
        print("{} {} {} {} {} {}".format(\
            str(int(i)+1).ljust(6), playing_servers_info[0][i].ljust(12), accounts_info[3][i].ljust(25),\
            accounts_info[0][i].ljust(8), playing_servers_info[1][i].ljust(6), playing_servers_info[2][i]))

def post_server(s, cookies, connect_server_payload):
    game_account_id = connect_server_payload[0]
    server_language = connect_server_payload[1]
    server_number = connect_server_payload[2]
    server_name = connect_server_payload[3]

    url = ("https://lobby-api.ogame.gameforge.com/users/me/loginLink?id={}"
           "&server[language]={}"
           "&server[number]={}".format(game_account_id,server_language,server_number))

    res = requests.get(url,cookies=cookies)
    result = re.sub(pattern=".*url\":\"|\"}",repl="",string=res.text).replace("\\","")

    connection = s.get(result)
    if connection.status_code == 200:
        print("\nWelcome To {}!".format(server_name))
