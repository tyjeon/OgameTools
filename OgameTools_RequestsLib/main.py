import login_ogame
import mail_to_csv
import espionage

import requests

def main():
    with requests.Session() as s:
        login_ogame.login_ogame(s)

        while True:
            choice = input("Espionage : 1 \n"
                           "Mail To Csv : 2 \n"
                           "Exit : 3 \n")

            try:
                choice = int(choice)
            except:
                continue

            if choice == 1:
                espionage.espionage(s)
            elif choice == 2:
                mail_to_csv.mail_to_csv(s)
            elif choice == 3:
                break
        

if __name__ == "__main__":
    main()
