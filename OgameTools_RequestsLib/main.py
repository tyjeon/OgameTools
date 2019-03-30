import login_ogame
import espionage
import mail_to_csv
import galaxy_tool
import invest

import requests

def main():
	with requests.Session() as s:
		server_address = login_ogame.login_ogame(s)

		while True:
			choice = input("Espionage : 1 \n"
						   "Mail To Csv : 2 \n"
						   "GalaxyTool : 3 \n"
						   "Exit : Else \n")

			try:
				choice = int(choice)
			except:
				continue

			if choice == 1:
				espionage.espionage(s)
			elif choice == 2:
				mail_to_csv.mail_to_csv(s)
			elif choice == 3:
				galaxy_tool.galaxy_tool(s)
			elif choice == 4:
				target_type = input("입력")
				amount = input("숫자 입력")
				invest.invest(s,target_type,amount,server_address)
			else:
				break
		

if __name__ == "__main__":
	main()