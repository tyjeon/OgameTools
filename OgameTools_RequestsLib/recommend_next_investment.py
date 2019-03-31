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
	resources = {}
	resources = get_resources(s,server_address,resources)

	investment_level = {}
	investment_level = get_resource_investment_level(s,server_address,investment_level)
	investment_level = get_station_investment_level(s,server_address,investment_level)
	investment_level = get_research_investment_level(s,server_address,investment_level)

	recommend_investment_type = [
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

	argument_list = [s,server_address,investment_level,recommend_investment_type,recommend_investment_level]
	compare_techtree(argument_list)


def get_resources(s,server_address,resources):
	html = s.get("https://{}.ogame.gameforge.com/game/index.php?page=resources".format(server_address))
	bs_object = BeautifulSoup(html.text,"html.parser")

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

def compare_techtree(argument_list):
	s = argument_list[0]
	server_address = argument_list[1]
	investment_level = argument_list[2]
	recommend_investment_type = argument_list[3]
	recommend_investment_level = argument_list[4]

	for i in range(len(recommend_investment_type)):
		if int(investment_level[recommend_investment_type[i]]) < recommend_investment_level[i]:
			print("{}이 업그레이드 필요. ({}<{})".format(all_type[recommend_investment_type[i]],investment_level[i],recommend_investment_level[i]))
			ask_for_investment(s,server_address,recommend_investment_type[i])
			break

def ask_for_investment(s,server_address,target_investment_number):
	invest_question = input("해당 시설(연구)을 개선합니까?(1/0)")

	if int(invest_question) == 1:
		invest.invest(s,target_investment_number,0,server_address)