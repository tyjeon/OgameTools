import requests
import re
import json

def login_ogame(s):
	print("-------------------------------------------------------------------")
	print("Login".center(67))
	print("-------------------------------------------------------------------")
	cookies = post_login(s)
	
	accounts_info_json = get_accounts_info(s)
	playing_servers_info_json = get_playing_servers_info(s,accounts_info_json)
	show_servers(accounts_info_json,playing_servers_info_json)
	connect_server_payload = select_server_number(accounts_info_json,playing_servers_info_json)
	post_server(s, cookies, connect_server_payload)

	server_address = "s{}-{}".format(connect_server_payload[2],connect_server_payload[1])

	return server_address

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
	accounts_info_request_url = "https://lobby-api.ogame.gameforge.com/users/me/accounts"
	accounts_info_request = s.get(accounts_info_request_url)
	accounts_info_json = json.loads(accounts_info_request.text)
	return accounts_info_json

def get_playing_servers_info(s,accounts_info_json):
	playing_servers_info_json = []
	servers_info_request_url = "https://lobby-api.ogame.gameforge.com/servers"
	servers_info_request = s.get(servers_info_request_url)
	servers_info_json = json.loads(servers_info_request.text)

	for j in range(len(accounts_info_json)):
		for i in range(len(servers_info_json)):
			if is_playing_server(accounts_info_json[j],servers_info_json[i]):
				playing_servers_info_json.append({
					'server_name':servers_info_json[i]['name'],
					'player_count':servers_info_json[i]['playerCount'],
					'players_online':servers_info_json[i]['playersOnline']})
				break

	return playing_servers_info_json

def is_playing_server(player_info,server_info):
	if player_info['server']['language'] == server_info['language']:
		if player_info['server']['number'] == server_info['number']:
			return True

	return False

def show_servers(accounts_info_json,playing_servers_info_json):
	print("\n{} {} {} {} {} {}".format("Number","Server".ljust(12),"Username".ljust(25),"Langauge","Online","Total"))
		
	for i in range(0,len(accounts_info_json)):
		print("{} {} {} {} {} {}".format(\
			str(int(i)+1).ljust(6),
			playing_servers_info_json[i]['server_name'].ljust(12),
			accounts_info_json[i]['name'].ljust(25),
			accounts_info_json[i]['server']['language'].ljust(8),
			str(playing_servers_info_json[i]['players_online']).ljust(6),
			playing_servers_info_json[i]['player_count']))

def select_server_number(accounts_info_json,playing_servers_info_json):
	select_server = int(input("\nSelect Server Number : ")) - 1
	connect_server_payload =[	accounts_info_json[select_server]['gameAccountId'],
								accounts_info_json[select_server]['server']['language'],
								accounts_info_json[select_server]['server']['number'],
								playing_servers_info_json[select_server]['server_name']]

	return connect_server_payload

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