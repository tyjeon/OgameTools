import pprint

resource_type = {
	# 메탈,크리,듀테,태발,핵융
	1:"Metal Mine",
	2:"Crystal Mine",
	3:"Deuterium Synthesizer",
	4:"Solar Plant",
	12:"Fusion Reactor",

	# 메탱,크탱,듀탱
	22:"Metal Storage",
	23:"Crystal Storage",
	24:"Deuterium Tank"}

facility_type = {
	# 로봇,쉽야,연구소,동맹디팟,미사일
	14:"Robotics Factory",
	21:"Shipyard",
	31:"Research Lab",
	34:"Alliance Depot",
	44:"Missile Silo",

	# 나노,테라포머,스페이스독
	15:"Nanite Factory",
	33:"Terraformer",
	36:"Space Dock"}

research_type = {
	# 에너지,레이저,이온,초공간,플라즈마 
	113:"Energy Technology",
	120:"Laser Technology",
	121:"Ion Technology",
	114:"Hyperspace Technology",
	122:"Plasma Technology",

	# 연소,핵추진,초공간,정찰,컴공
	115:"Combustion Drive",
	117:"Impulse Drive",
	118:"Hyperspace Drive",
	106:"Espionage Technology",
	108:"Computer Technology",

	# 천물,넷워크,중력장,무,보
	124:"Astrophysics",
	123:"Intergalactic Research Network",
	199:"Graviton Technology",
	109:"Weapons Technology",
	110:"Shielding Technology",

	# 장
	111:"Armour Technology"}

fleet_type = {
	# 전투,공격,구축,배틀쉽,배틀쿠르저
	204:"Light Fighter",
	205:"Heavy Fighter",
	206:"Cruiser",
	207:"Battleship",
	215:"Battlecruiser",

	# 폭격,디스트로이어,죽별,카소,카대
	211:"Bomber",
	213:"Destroyer",
	214:"Deathstar",
	202:"Small Cargo",
	203:"Large Cargo",

	#식민,수확,정찰,태발
	208:"Colony Ship",
	209:"Recycler",
	210:"Espionage Probe",
	212:"Solar Satellite"}

defence_type = {
	# 로켓,레약,레강,가우스,이온
	401:"Rocket Launcher",
	402:"Light Laser",
	403:"Heavy Laser",
	404:"Gauss Cannon",
	405:"Ion Cannon",

	# 플라즈마,보호소형,보호대형,IPM,ABM
	406:"Plasma Turret",
	407:"Small Shield Dome",
	408:"Large Shield Dome",
	502:"Anti-Ballistic Missiles",
	503:"Interplanetary Missiles"}

all_type = {**resource_type,**facility_type,**research_type,**fleet_type,**defence_type}