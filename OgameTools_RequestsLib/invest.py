from bs4 import BeautifulSoup
import re
import os
import csv
import time
import random

def build(s,target_type,amount=0):
	request_url_front = "https://s1-en.ogame.gameforge.com/game/index.php?page="
	request_url_back = "&deprecated=1"

	hidden_token = "" # token 받아오고..

	if is_bulding():
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
