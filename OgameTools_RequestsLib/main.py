import login_ogame
import espionage
import mail_to_csv
import galaxy_tool

import requests

def main():
	with requests.Session() as s:
		login_ogame.login_ogame(s)

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
			else:
				break
		

if __name__ == "__main__":
	main()