import login_ogame
import mail_to_csv

import requests

def main():
    with requests.Session() as s:
        login_ogame.login_ogame(s)
        mail_to_csv.mail_to_csv(s)
        
    
    

if __name__ == "__main__":
    main()
