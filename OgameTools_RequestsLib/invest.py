from bs4 import BeautifulSoup
import re

# 메탈,크리,듀테,태발,메탱,크탱,듀탱,핵융
resource_type = [1,2,3,4,22,23,24,12]
# 로봇,쉽야,연구소,동맹디팟,미사일,나노,테라포머,스페이스독
facility_type = [14,21,31,34,44,15,33,36]
# 에너지,레이저,이온,초공간,플라즈마,연소,핵추진,초공간,정찰,컴공,천물,넷워크,중력장,무,보,장
research_type = [113,120,121,114,122,115,117,118,106,108,124,123,199,109,110,111]
# 전투,공격,구축,배틀쉽,배틀쿠르저,폭격,디스트로이어,죽별,카소,카대,식민,수확,정찰,태발
fleet_type = [204,205,206,207,215,211,213,214,202,203,208,209,210,212]
# 로켓,레약,레강,가우스,이온,플라즈마,보호소형,보호대형,IPM,ABM
defence_type = [401,402,403,404,405,406,407,408,502,503]

def invest(s,target_type,amount,server_address):
	init()

	request_url_page_category = get_page_category(target_type)
	request_url = \
	"https://{}.ogame.gameforge.com/game/index.php?page={}&deprecated=1".format(server_address,request_url_page_category)

	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=".format(server_address)+request_url_page_category)
	hidden_token = get_token(html)
	payload = get_payload(target_type,hidden_token,amount)

	invest_request = s.post(request_url, data=payload)
	print(request_url)
	print(payload)
	print(invest_request.status_code)

def init():
	global resource_type
	global facility_type
	global research_type
	global fleet_type
	global defence_type

def get_token(html):
	bs_object = BeautifulSoup(html.text,"html.parser")
	token_raw_text = bs_object.find("input",{"name":"token"})
	token = re.compile("(?<=value=\").*?(?=\")").search(str(token_raw_text)).group()
	return token

def get_payload(target_type,hidden_token,amount):
	amount_form = fleet_type+defence_type

	try:
		target_type = int(target_type)
		if int(target_type) in amount_form:
		    payload = { "token":hidden_token,
		    			"modus":"1",
		    			"type":target_type,
		    			"menge":""}
		else:
		    payload = { "token":hidden_token,
		    			"modus":"1",
		    			"type":target_type}
		return payload
	except:
		return False

def get_page_category(target_type):
	target_type = int(target_type)
	if target_type in resource_type:
		return "resources"
	elif target_type in resource_type:
		return "station"
	elif target_type in research_type:
		return "research"
	elif target_type in fleet_type:
		return "shipyard"
	elif target_type in defence_type:
		return "defense"