#1. 건물 레벨 확인하고(연구도)#
#2. 자원 확인하고#
#3. 테크트리 확인하고#
#4. 대조해서가면서 다음 올려야 할 순서를 발견 시 반환

#5. yes no 입력, yes 반환시 build(값 넘기기)#

from investment_number import *
import invest

from bs4 import BeautifulSoup
import re

def recommend_next_investment(s,server_address):
	investment_level = {}
	investment_level = get_resource_investment_level(s,server_address,investment_level)
	investment_level = get_station_investment_level(s,server_address,investment_level)
	investment_level = get_research_investment_level(s,server_address,investment_level)

	recommend_investment_number = [
						4,1,4,1,4,
						2,4,1,2,4,
						3,2,4,1,4,
						2,3,4,3,4,
						3,14,31,21,2,
						21,4,3,1,113,
						115,4,2,1]
	recommend_investment_level = [
						1,2,2,4,3,
						1,4,5,3,5,
						1,4,6,7,7,
						5,2,8,4,9,
						5,2,1,1,6,
						2,10,6,8,1
						,1,11,7,9]

	argument_list = [investment_level,recommend_investment_number,recommend_investment_level]
	target_investment_number = get_uninvested_investment_number(argument_list)
	
	resources = get_resources(s,server_address)
	next_level = int(investment_level[target_investment_number])+1
	argument_list = [s,server_address,target_investment_number,next_level,investment_level]
	cost = get_cost(argument_list)
	show_receipt(resources,cost)

	ask_for_investment(s,server_address,target_investment_number)

def get_resource_investment_level(s,server_address,investment_level):
	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=resources".format(server_address))
	bs_object = BeautifulSoup(html.text,"html.parser")

	i = 1
	satellite_button = 6

	for key, value in resource_type.items():
		if i == satellite_button:
			i += 1
		building_raw_text = bs_object.find("li",{"id":"button{}".format(i)}) # 1~9까지 메/크/듀/태발/핵융/태위/메탱/크탱/듀탱
		level_raw_text = building_raw_text.find("span",{"class":"level"})
		investment_level[key] = re.compile("\d+").search(str(level_raw_text)).group()
		i += 1

	return investment_level

def get_station_investment_level(s,server_address,investment_level):
	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=station".format(server_address))
	bs_object = BeautifulSoup(html.text,"html.parser")

	i = 0
	for key, value in facility_type.items():
		station_raw_text = bs_object.find("li",{"id":"button{}".format(i)})
		level_raw_text = station_raw_text.find("span",{"class":"level"})
		investment_level[key] = re.compile("\d+").search(str(level_raw_text)).group()
		i += 1

	return investment_level

def get_research_investment_level(s,server_address,investment_level):
	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=research".format(server_address))
	bs_object = BeautifulSoup(html.text,"html.parser")

	for key, value in research_type.items():
		research_raw_text = bs_object.find("div",{"class":"item_box research{}".format(key)})
		level_raw_text = research_raw_text.find("span",{"class":"level"})
		investment_level[key] = re.compile("\d+").search(str(level_raw_text)).group()

	return investment_level

def get_uninvested_investment_number(argument_list):
	investment_level = argument_list[0]
	recommend_investment_number = argument_list[1]
	recommend_investment_level = argument_list[2]

	for i in range(len(recommend_investment_number)):
		if int(investment_level[recommend_investment_number[i]]) < recommend_investment_level[i]:
			print("{}이 업그레이드 필요. ({}<{})".format(all_type[recommend_investment_number[i]],\
														investment_level[recommend_investment_number[i]],
														recommend_investment_level[i]))
			break

	return recommend_investment_number[i]

def ask_for_investment(s,server_address,target_investment_number):
	invest_question = input("해당 시설(연구)을 개선합니까?(1/0)")

	if int(invest_question) == 1:
		invest.invest(s,target_investment_number,0,server_address)

def get_resources(s,server_address):
	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=resources".format(server_address))
	bs_object = BeautifulSoup(html.text,"html.parser")

	resources = {}

	resources_raw_text = bs_object.find("ul",{"id":"resources"})
	metal_raw_text = resources_raw_text.find("span",{"id":"resources_metal"})
	resources["metal"] = re.sub("\D","",str(metal_raw_text))

	crystal_raw_text = resources_raw_text.find("span",{"id":"resources_crystal"})
	resources["crystal"] = re.sub("\D","",str(crystal_raw_text))

	deuterium_raw_text = resources_raw_text.find("span",{"id":"resources_deuterium"})
	resources["deuterium"] = re.sub("\D","",str(deuterium_raw_text))

	energy_raw_text = resources_raw_text.find("span",{"id":"resources_energy"})
	resources["energy"] = re.sub("\D","",str(energy_raw_text))

	return resources

def get_cost(argument_list):
	s = argument_list[0]
	server_address = argument_list[1]
	investment_number = argument_list[2]
	next_level = argument_list[3]
	investment_level = argument_list[4]


	html= s.get("https://s1-en.ogame.gameforge.com/game/index.php?page=overview")
	universe_speed = int(re.compile("(?<=ogame-universe-speed\" content=\")\d+").search(html.text).group())
	base_cost_element = get_investment_cost_element(investment_number)

	cost = {}
	cost["metal"] = int(base_cost_element["metal"]*base_cost_element["base"]**(next_level-1))
	cost["crystal"] = int(base_cost_element["crystal"]*base_cost_element["base"]**(next_level-1))
	cost["deuterium"] = int(base_cost_element["deuterium"]*base_cost_element["base"]**(next_level-1))
	if investment_number == 1 or investment_number == 2:
		cost["energy"] = int(10*next_level*1.1**next_level - 10*(next_level-1)*1.1**(next_level-1))
	elif investment_number == 3:
		cost["energy"] = int(20*next_level*1.1**next_level - 20*(next_level-1)*1.1**(next_level-1))
	else:
		cost["energy"] = 0

	cost["time"] = (cost["metal"]+cost["crystal"])*3600/float(2500*(1+float(investment_level[14]))*2**float(investment_level[15])*float(universe_speed))
	cost["time"] = int(cost["time"])

	return cost

def get_investment_cost_element(investment_number): # TODO 딕셔너리 완성하기.
	base_cost_element = {}
	base_cost_element[1] = {"metal" : 60, "crystal" : 15, "deuterium" : 0, "base" : 1.5}
	base_cost_element[2] = {"metal" : 48, "crystal" : 24, "deuterium" : 0, "base" : 1.6}

	return base_cost_element[investment_number]
	

def show_receipt(resources,cost): # TODO 여기 PPRINT나 LJUST/RJUST로 꾸미기.
	print(resources)
	print(cost)