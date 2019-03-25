import util

import requests
from bs4 import BeautifulSoup
import os
import re
import time
import datetime

def galaxy_tool(s):
	print("-------------------------------------------------------------------")
	print("GalaxyTool".center(67))
	print("-------------------------------------------------------------------")
	post_url = "https://s1-en.ogame.gameforge.com/game/index.php?page=galaxyContent&ajax=1"

	start_galaxy = int(input("Input Start Galaxy : "))
	end_galaxy = int(input("Input End Galaxy : "))

	start_system = int(input("Input Start System : "))
	end_system = int(input("Input End System : "))

	
	filename = set_csv_title_row()
	for i in range(start_galaxy,end_galaxy+1):
		galaxy_object = []
		for j in range(start_system,end_system+1):
			print("Scanning {}:{} ...".format(i,j))
			payload = {'galaxy':i,
					   'system':j}

			galaxy_requests = s.post(post_url, data=payload)
			galaxy_object.append(BeautifulSoup(galaxy_requests.text,"html.parser"))

		for j in range(start_system,end_system+1):
			parse_ogame_galaxy_source(galaxy_object[j-1],i,j,filename)

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
		print("Gal,Sys,Pla,PlanetName,Moon,UserName,__user_rank,__alliance_name,__alliance_rank,__alliance_member,Vacation,Inactive,LongInactive,Recyclers",file=f)

	return filename

def parse_ogame_galaxy_source(bs_object,galaxy_number,system_number,filename):
		planet_number = []
		planet_name = []
		is_there_moon = []
		recyclers_for_debris = []
		user_name = []
		user_rank = []
		alliance_name = []
		alliance_rank = []
		alliance_member = []
		status_vacation = []
		status_inactive = []
		status_longinactive = []
		
		system_source = bs_object.findAll("tr",{"class":re.compile("^row.*")})

		for planet_source in system_source:
				planet_number.append(get_planet_number(planet_source))
				planet_name.append(get_planet_name(planet_source))
				is_there_moon.append(get_moon(planet_source))
				user_name.append(get_user_name(planet_source))
				user_rank.append(get_user_rank(planet_source))
				alliance_name.append(get_alliance_name(planet_source))
				alliance_rank.append(get_alliance_rank(planet_source))
				alliance_member.append(get_alliance_member(planet_source))
				status_vacation.append(get_status(planet_source,"status_abbr_vacation"))
				status_inactive.append(get_status(planet_source,"status_abbr_inactive"))
				status_longinactive.append(get_status(planet_source,"status_abbr_longinactive"))
				recyclers_for_debris.append(get_recyclers_for_debris(planet_source))

		i = 0
		for i in range(len(planet_name)):
				with open("GalaxyTool/"+filename, encoding="utf-8",mode='a+') as f:
						print(",".join([
											str(galaxy_number),
											str(system_number),
											planet_number[i],
											planet_name[i],
											is_there_moon[i],
											user_name[i],
											user_rank[i],
											alliance_name[i],
											alliance_rank[i],
											alliance_member[i],
											status_vacation[i],
											status_inactive[i],
											status_longinactive[i],
											recyclers_for_debris[i],
										]),file=f)

def get_planet_number(planet_source):
	arguments_for_parsing=[planet_source,["td","class","position js_no_action"],"(<td class=\"position js_no_action\">|</td>)"]
	return util.parse_using_regexp(arguments_for_parsing)

def get_planet_name(planet_source):
	arguments_for_parsing=[planet_source,["div","id",re.compile("planet\d+")],"(.*textNormal\">|<\/span.*div>)"]
	return util.parse_using_regexp(arguments_for_parsing)

def get_moon(planet_source):
	arguments_for_parsing=[planet_source,["div","class",re.compile("moon_a")],""]
	is_there_moon_in_html = util.parse_using_regexp(arguments_for_parsing)
	if "moon" in is_there_moon_in_html:
		moon_status = "1"
	else:
		moon_status = ""

	return moon_status

def get_user_name(planet_source):
	arguments_for_parsing=[planetsource,["div","id",re.compile("player\d+")],".*: <span>|<\/span>.*"]
	return util.parse_using_regexp(arguments_for_parsing)

def get_user_rank(planet_source):
	arguments_for_parsing=[planet_source,["div","id",re.compile("player\d+")],"(.*searchRelId=\d+\">|<\/a><\/li>.*)"]
	user_rank_in_html = util.parse_using_regexp(arguments_for_parsing)

	if "page=support" in user_rank_in_html: # 관리자 예외
		user_rank = ""
	elif "sendMail" in user_rank_in_html: # 밴 당한 사람은 랭크가 없음.
		user_rank = ""
	else:
		user_rank = user_rank_in_html

	return user_rank

def get_alliance_name(planet_source):
	arguments_for_parsing=[planet_source,["div","id",re.compile("alliance\d+")],"(.*<h1>|<\/h1>.*)"]
	return util.parse_using_regexp(arguments_for_parsing)

def get_alliance_rank(planet_source):
	arguments_for_parsing=[planet_source,["div","id",re.compile("alliance\d+")],"(.*searchRelId=\d+\">|<\/a><\/li>).*"]
	return util.parse_using_regexp(arguments_for_parsing)

def get_alliance_member(planet_source):
	arguments_for_parsing=[planet_source,["div","id",re.compile("alliance\d+")],"(.*Member: |</li><li><a href=\"allianceInfo.*)"]
	return util.parse_using_regexp(arguments_for_parsing)

def get_status(planet_source, condition):
	arguments_for_parsing=[planet_source,["span","class","status"],""]
	status_in_html = util.parse_using_regexp(arguments_for_parsing)
	
	if condition in status_in_html:
		status = "1"
	else:
		status = ""

	return status

def get_recyclers_for_debris(planet_source):
	arguments_for_parsing=[planet_source,["li","class","debris-recyclers"],".*Recyclers needed: |</li>"]
	return util.parse_using_regexp(arguments_for_parsing)