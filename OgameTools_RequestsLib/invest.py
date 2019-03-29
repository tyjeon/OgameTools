from bs4 import BeautifulSoup
import re
import os
import csv
import time
import random

def build(s,target_type,amount=1):
	request_url_front = "https://s1-en.ogame.gameforge.com/game/index.php?page="
	request_url_back = "&deprecated=1"

	hidden_token = "" # token 받아오고..

	if is_type_with_amount_form(target_type):
	    payload = { "token":hidden_token,
	    			"modus":"1",
	    			"type":target_type}
	else:
	    payload = { "token":hidden_token,
	    			"modus":"1",
	    			"type":target_type,
	    			"menge":amount}

	request_url_page_category = "" # resource인지, station인지..를 구분하기. target type에 따라 무식하게 if문 하면 되지 않을까?
	request_url = request_url_front + request_url_page_category + request_url_back
	build_request = s.post(request_url, data=payload)

def is_type_with_amount_form(target_type):
	# 메탈,크리,듀테,태발,메탱,크탱,듀탱,핵융,로봇,쉽야,연구소,동맹디팟,미사일,나노,테라포머,스페이스독
	building_type = [1,2,3,4,22,23,24,12,14,21,31,34,44,15,33,36]
	# 에너지,레이저,이온,초공간,플라즈마,연소,핵추진,초공간,정찰,컴공,천물,넷워크,중력장,무,보,장
	research_type = [113,120,121,114.122,115,117,118,106,108,124,123,199,109,110,111]
	# 전투,공격,구축,배틀쉽,배틀쿠르저,폭격,디스트로이어,죽별,카소,카대,식민,수확,정찰,태발
	fleet_type = [204,205,206,207,215,211,213,214,202,203,208,209,210,212]
	# 로켓,레약,레강,가우스,이온,플라즈마,보호소형,보호대형,IPM,ABM
	defence_type = [401,402,403,404,405,406,407,408,502,503]

	amount_form = fleet_type+defence_type

	try:
		target_type = int(target_type)
		if int(target_type) in amount_form:
			return True
	except:
		return False

print(is_type_with_amount_form(222))
