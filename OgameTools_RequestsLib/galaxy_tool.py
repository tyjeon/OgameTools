import util

import requests
from bs4 import BeautifulSoup
import os
import re
import time
import datetime

def galaxy_tool(s,server_address):
	print("-------------------------------------------------------------------")
	print("GalaxyTool".center(67))
	print("-------------------------------------------------------------------")
	post_url = "https://{}.ogame.gameforge.com/game/index.php?page=galaxyContent&ajax=1".format(server_address)

	start_galaxy = int(input("Input Start Galaxy : "))
	end_galaxy = int(input("Input End Galaxy : "))

	start_system = int(input("Input Start System : "))
	end_system = int(input("Input End System : "))

	filename = set_csv_title_row()

	for i in range(start_galaxy,end_galaxy+1):
		galaxy_text = []
		for j in range(start_system,end_system+1):
			print("Scanning {}:{} ...".format(i,j))
			payload = {'galaxy':i,
					   'system':j}

			galaxy_requests = s.post(post_url, data=payload)
			galaxy_text.append(galaxy_requests.text)

		for j in range(start_system,end_system+1):
			parse_ogame_galaxy_source(galaxy_text[j-1],i,j,filename)

def set_csv_title_row():
	if not os.path.isdir("GalaxyTool"):
		os.mkdir("GalaxyTool")
	
	today = datetime.datetime.today()
	year = str(today.year)
	month = str(today.month)
	day = str(today.day)
	hour = str(today.hour)
	minute = str(today.minute)
	second = str(today.second)

	filename = "Galaxy_"+year+"_"+month+"_"+day+"_"+hour+"_"+minute+".csv"
	
	with open("GalaxyTool/"+filename, encoding="utf-8",mode='a+') as f:
		print(
			"Gal,"
			"Sys,"
			"Pla,"
			"PlanetName,"
			"Moon,"
			"UserName,"
			"UserRank,"
			"AllianceName,"
			"AllianceRank,"
			"AllianceMember,"
			"Status,"
			"Debris"
			,file=f)

	return filename

def parse_ogame_galaxy_source(text,galaxy_number,system_number,filename):
		planet_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
		planet_name=get_planet_name(text)
		moon=get_moon(text)

		player_info=get_player_info(text)
		user_name=player_info[0]
		user_rank=player_info[1]
		status=player_info[2]

		alliance_info = get_alliance_info(text)
		alliance_name=alliance_info[0]
		alliance_rank=alliance_info[1]
		alliance_member=alliance_info[2]

		debris=get_debris(text)

		i = 0
		for i in range(15):
				with open("GalaxyTool/"+filename, encoding="utf-8",mode='a+') as f:
						print(",".join([
											str(galaxy_number),
											str(system_number),
											str(planet_number[i]),
											str(planet_name[i]),
											str(moon[i]),
											str(user_name[i]),
											str(user_rank[i]),
											str(alliance_name[i]),
											str(alliance_rank[i]),
											str(alliance_member[i]),
											str(status[i]),
											str(debris[i])
										]),file=f)

def get_planet_name(text):
	planet_name_slot_regexp = re.compile("<td class=\\\\\"planetname.*?td>")
	planet_name_slot_raw_text = planet_name_slot_regexp.findall(text)

	planet_name_regexp = re.compile("<h1>Planet.*?span>")
	planet_name_raw_text = planet_name_regexp.findall(text)
	planet_name = []
	j=0

	for i in range(15):
		if "js_planetNameEmpty" in planet_name_slot_raw_text[i]:
			planet_name.append("")
		else:
			planet_name.append(re.sub(".*textNormal..>|<.*","",planet_name_raw_text[j]))
			j+=1

	try:
		planet_name.append(re.sub(".*textNormal..>|<.*","",planet_name_raw_text[j]))
	except:
		planet_name.append("")
	return planet_name

def get_moon(text):
	moon_regexp = re.compile("<td class=\\\\\"moon.*?td>")
	moon_raw_text = moon_regexp.findall(text)
	moon = []

	for i in range(15):
		if "js_no_action" in moon_raw_text[i]:
			moon.append("")
		else:
			moon.append(1)
	return moon

def get_debris(text):
	debris_regexp = re.compile("<td class=\\\\\"debris.*?td>")
	debris_raw_text = debris_regexp.findall(text)
	debris = []

	for i in range(15):
		try:
			metal_in_debris = re.compile("(?<=Metal: )[\d\.]+").search(debris_raw_text[i]).group().replace(".","")
			crystal_in_debris = re.compile("(?<=Crystal: )[\d\.]+").search(debris_raw_text[i]).group().replace(".","")
			total_debris = int(metal_in_debris)+int(crystal_in_debris)
			debris.append(total_debris) 
		except:
			debris.append("")

	return debris

def get_player_info(text):
	player_regexp = re.compile("<td class=..playername.*?td>")
	player_raw_text = player_regexp.findall(text)

	player_name = []
	player_rank = []
	status = []

	for i in range(15):
		try:
			player_name.append(re.compile("(?<=<span>).*?(?=<)").search(player_raw_text[i]).group())
		except:
			player_name.append("")
		try:
			player_rank.append(re.compile("\d+(?=<\\\/a>)").search(player_raw_text[i]).group())
		except:
			player_rank.append("")

		try:
			if "status_abbr_vacation" in player_raw_text[i]:
				status.append("Vacation")
			else:
				status.append("")
		except:
			try:
				status[i] = ""
			except:
				status.append("")
		try:
			if "status_abbr_longinactive" in player_raw_text[i]:
				status[i] += "LongInactive"
			elif "status_abbr_inactive" in player_raw_text[i]:
				status[i] += "Inactive"
			else:
				status[i] += ""
		except:
			status[i] += ""


	player_info = [player_name, player_rank, status]
	return player_info

def get_alliance_info(text):
	alliance_regexp = re.compile("allytag.*?td>")
	alliance_raw_text = alliance_regexp.findall(text)
	alliance_name = []
	alliance_rank = []
	alliance_member = []

	for i in range(15):
		try:
			alliance_name.append(re.compile("(?<=h1>).*?(?=<)").search(alliance_raw_text[i]).group())
			alliance_rank.append(re.compile("\d+(?=<\\\/a>)").search(alliance_raw_text[i]).group())
			alliance_member.append(re.compile("(?<=Member: )\d+").search(alliance_raw_text[i]).group())
		except:
			alliance_name.append("")
			alliance_rank.append("")
			alliance_member.append("")

	alliance_info = [alliance_name, alliance_rank, alliance_member]
	return alliance_info