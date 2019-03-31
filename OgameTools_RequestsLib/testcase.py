import main

from unittest.mock import patch
import unittest
import os

class Test(unittest.TestCase):

	def test_main(self):

		with open("espionage.csv",'w',encoding="utf-8") as f:
			print("8,479,4\n"
				  "8,481,10\n"
				  "8,483,12\n"
				  "8,484,8",file=f)
		
		user_input_1 = [
			"dfo@vomoto.com",
			"789456",
			"2",
			#"1", # 기능 테스트
			#"2",
			#"3", "1", "2", "1", "3", # 갤럭시툴 좌표 지정.
			#"4","212","2", # 태위 2대 생산.
			"5",1, # 빌드 추천
			"9"
		]
		
		with patch('builtins.input', side_effect=user_input_1):
			test = main.main()

		try:
			os.remove("espionage.csv")
		except:
			pass

if __name__ == '__main__':
	unittest.main()