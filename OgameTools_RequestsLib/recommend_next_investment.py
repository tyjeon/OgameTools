#1. 건물 레벨 확인하고(연구도)#
#2. 자원 확인하고#
#3. 테크트리 확인하고#
#4. 대조해서가면서 다음 올려야 할 순서를 발견 시 반환

#5. yes no 입력, yes 반환시 build(값 넘기기)#

from investment_number import *
import invest

from bs4 import BeautifulSoup
import re
import time
import threading

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
		research_raw_text = bs_object.find("a",{"id":"details{}".format(key)})
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

def get_resources(s,server_address):
	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=resources".format(server_address))
	bs_object = BeautifulSoup(html.text,"html.parser")

	resources = {"metal" : 0, "crystal" : 0, "deuterium" : 0, "energy" : 0}
	resources_raw_text = bs_object.find("ul",{"id":"resources"})
	for key, value in resources.items():
		raw_text = resources_raw_text.find("span",{"id":"resources_{}".format(key)})
		resources[key] = re.sub("\D","",str(raw_text))

	return resources

def get_cost(argument_list):
	s = argument_list[0]
	server_address = argument_list[1]
	investment_number = argument_list[2]
	next_level = argument_list[3]
	investment_level = argument_list[4]


	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=overview".format(server_address))
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
	elif investment_number ==33:
		cost["energy"] = 1000*2**(next_level-1)
	elif investment_number == 199:
		cost["energy"] = 300000*3**(next_level-1)
	else:
		cost["energy"] = 0

	if investment_number < 100:
		cost["time"] = (cost["metal"]+cost["crystal"])*3600/float(2500*(1+float(investment_level[14]))*2**float(investment_level[15])*float(universe_speed))
	else:
		cost["time"] = (cost["metal"]+cost["crystal"])/(float(universe_speed)*1000*(1+float(investment_level[31])))

	cost["time"] = int(cost["time"])

	return cost

def get_investment_cost_element(investment_number): # TODO 딕셔너리 완성하기.
	base_cost_element = {}
	base_cost_element[1] = {"metal" : 60, "crystal" : 15, "deuterium" : 0, "base" : 1.5}
	base_cost_element[2] = {"metal" : 48, "crystal" : 24, "deuterium" : 0, "base" : 1.6}
	base_cost_element[3] = {"metal" : 225, "crystal" : 75, "deuterium" : 0, "base" : 1.5}
	base_cost_element[4] = {"metal" : 75, "crystal" : 30, "deuterium" : 0, "base" : 1.5}
	base_cost_element[12] = {"metal" : 900, "crystal" : 360, "deuterium" : 180, "base" : 1.8}

	base_cost_element[22] = {"metal" : 1000, "crystal" : 0, "deuterium" : 0, "base" : 2}
	base_cost_element[23] = {"metal" : 1000, "crystal" : 500, "deuterium" : 0, "base" : 2}
	base_cost_element[24] = {"metal" : 1000, "crystal" : 1000, "deuterium" : 0, "base" : 2}

	base_cost_element[14] = {"metal" : 400, "crystal" : 120, "deuterium" : 200, "base" : 2}
	base_cost_element[21] = {"metal" : 400, "crystal" : 200, "deuterium" : 100, "base" : 2}
	base_cost_element[31] = {"metal" : 200, "crystal" : 400, "deuterium" : 200, "base" : 2}
	base_cost_element[34] = {"metal" : 20000, "crystal" : 40000, "deuterium" : 0, "base" : 2}
	base_cost_element[44] = {"metal" : 20000, "crystal" : 20000, "deuterium" : 1000, "base" : 2}
	base_cost_element[15] = {"metal" : 1000000, "crystal" : 500000, "deuterium" : 100000, "base" : 2}

	base_cost_element[33] = {"metal" : 0, "crystal" : 50000, "deuterium" : 100000, "base" : 2}
	base_cost_element[36] = {"metal" : 200, "crystal" : 50, "deuterium" : 50, "base" : 2}

	base_cost_element[113] = {"metal" : 0, "crystal" : 800, "deuterium" : 400, "base" : 2}
	base_cost_element[120] = {"metal" : 200, "crystal" : 100, "deuterium" : 0, "base" : 2}
	base_cost_element[121] = {"metal" : 1000, "crystal" : 300, "deuterium" : 100, "base" : 2}
	base_cost_element[114] = {"metal" : 0, "crystal" : 4000, "deuterium" : 2000, "base" : 2}
	base_cost_element[122] = {"metal" : 2000, "crystal" : 4000, "deuterium" : 1000, "base" : 2}

	base_cost_element[115] = {"metal" : 400, "crystal" : 0, "deuterium" : 600, "base" : 2}
	base_cost_element[117] = {"metal" : 2000, "crystal" : 4000, "deuterium" : 600, "base" : 2}
	base_cost_element[118] = {"metal" : 10000, "crystal" : 20000, "deuterium" : 6000, "base" : 2}
	base_cost_element[106] = {"metal" : 200, "crystal" : 1000, "deuterium" : 200, "base" : 2}
	base_cost_element[108] = {"metal" : 0, "crystal" : 400, "deuterium" : 600, "base" : 2}

	base_cost_element[124] = {"metal" : 4000, "crystal" : 8000, "deuterium" : 4000, "base" : 1.75}
	base_cost_element[123] = {"metal" : 240000, "crystal" : 400000, "deuterium" : 160000, "base" : 2}
	base_cost_element[199] = {"metal" : 0, "crystal" : 0, "deuterium" : 0, "base" : 2}
	base_cost_element[109] = {"metal" : 800, "crystal" : 200, "deuterium" : 0, "base" : 2}
	base_cost_element[110] = {"metal" : 200, "crystal" : 600, "deuterium" : 0, "base" : 2}

	base_cost_element[111] = {"metal" : 1000, "crystal" : 0, "deuterium" : 0, "base" : 2}
	
	return base_cost_element[investment_number]

def show_receipt(resources,cost):
	length = {"metal":5,"crystal":7,"deuterium":9,"energy":6}
	for key in resources:
		if len(resources[key]) < len(str(cost[key])):
			if length[key] < len(str(cost[key])):
				length[key] = len(str(cost[key]))
		else:
			if length[key] < len(resources[key]):
				length[key] = len(resources[key])

	print("     {:>{}}     {:>{}}     {:>{}}     {:>{}}".format("Metal",length["metal"],
																"Crystal",length["crystal"],
																"Deuterium",length["deuterium"],
																"Energy",length["energy"]))
	print("     {:>{}}     {:>{}}     {:>{}}     {:>{}}".format(resources["metal"],length["metal"],
																resources["crystal"],length["crystal"],
																resources["deuterium"],length["deuterium"],
																resources["energy"],length["energy"]))
	print("-    {:>{}}     {:>{}}     {:>{}}     {:>{}}".format(cost["metal"],length["metal"],
																cost["crystal"],length["crystal"],
																cost["deuterium"],length["deuterium"],
																cost["energy"],length["energy"],))

	print("".center(20+length["metal"]+length["crystal"]+length["deuterium"]+length["energy"],"-"))

	print("     {:>{}}     {:>{}}     {:>{}}     {:>{}}".format(int(resources["metal"])-cost["metal"],length["metal"],
																int(resources["crystal"])-cost["crystal"],length["crystal"],
																int(resources["deuterium"])-cost["deuterium"],length["deuterium"],
																int(resources["energy"])-cost["energy"],length["energy"]))

def ask_for_investment(s,server_address,target_investment_number):
	invest_question = input("해당 시설(연구)을 개선합니까?(1/0)")

	if int(invest_question) == 1:
		make_invest_queue(s,target_investment_number,server_address)

def make_invest_queue(s,target_investment_number,server_address):
	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=overview".format(server_address))

	if target_investment_number < 100:
		try:
			left_duration_raw_text = re.compile("(?=Cache\(\"Countdown\"\),).*?https").search(html.text).group()
			left_duration = int(re.compile("\d+").search(left_duration_raw_text).group())
			print("다른 건설이 이미 진행중이므로 {}초 이후에 진행합니다.".format(left_duration))
		except:
			left_duration = 0
		
	else:
		try:
			left_duration_raw_text = re.compile("(?=Cache\(\"researchCountdown\"\),).*?https").search(html.text).group()
			left_duration = int(re.compile("\d+").search(left_duration_raw_text).group())
			print("다른 연구가 이미 진행중이므로 {}초 이후에 진행합니다.".format(left_duration))
		except:
			left_duration = 0


	invest_queue_thread = threading.Thread(target=invest.invest, args = (s,target_investment_number,0,server_address,left_duration))
	invest_queue_thread.start()
