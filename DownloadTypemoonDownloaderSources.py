import requests
from bs4 import BeautifulSoup
import os
import re

def main():
	folder_name = "TypemoonDownloader"
	user_id = "taeyongjeon"
	user_pw = "cilarnycstme24*"
	folder_url = "https://github.com/taeyongjeon/pycrawl/tree/master/typemoon"

	check_folder(folder_name)

	with requests.Session() as s:
		login_github(s,user_id,user_pw)
		file_name, file_link = get_file_information(s, folder_url)

		for i in range(len(file_name)):
		  download_file(s,file_link[i],file_name[i],folder_name)

def check_folder(folder_name):
	if not os.path.isdir(folder_name):
		os.mkdir(folder_name)

def login_github(s,user_id,user_pw):
	token = get_token(s)
	payload = {'authenticity_token':token,
			   'login':user_id,
			   'password':user_pw}

	login_request = s.post('https://github.com/session', data=payload)

def get_token(s):
	html = s.get('https://github.com/login')
	bs_object = BeautifulSoup(html.text,'html.parser')
	token_source = bs_object.findAll("",{"name":"authenticity_token"})
	token_source = re.sub(pattern="\n", repl="",string=str(token_source))
	token = str(re.sub(pattern=".*authenticity_token\" type=\"hidden\" value=\"|\".*", repl="",string=token_source))
	
	return token

def get_file_information(s, folder_url):
	folder_page_request = s.get(folder_url)
	files = re.compile("js-navigation-open. title.*?a>").findall(folder_page_request.text)
	file_name = []
	file_link = []

	for i in range(len(files)):
	  file_name.append(re.compile("(?<=title=\").*?(?=\")").search(files[i]).group())
	  link_format = "https://github.com"+re.compile("(?<=href=\").*?(?=\")").search(files[i]).group().replace("/blob/master/","/raw/master/")
	  file_link.append(link_format)

	return file_name,file_link

def download_file(s,url,file_name,folder_name):
	file_url = s.get(url)

	with open("{}/{}".format(folder_name,file_name), 'wb') as f:
		f.write(file_url.content)

	print(file_name+" downloaded.")		

if __name__=='__main__':
	main()