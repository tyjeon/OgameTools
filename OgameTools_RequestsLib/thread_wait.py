import threading
import time
import os

def worker(invest_type,wait_time):
	filename = "{}({}).txt".format(threading.current_thread().getName(),invest_type)
	with open(filename,encoding="utf-8",mode="w+") as f:
		f.write(invest_type+"\n")
		f.write(str(wait_time))

	while True:
		threads = threading.enumerate()
		previous_index = threading.enumerate().index(threading.current_thread()) - 1

		file_list = os.listdir(os.getcwd())
		file_list_invest_type = [file for file in file_list if file.endswith("({}).txt".format(invest_type))]
		created_time_of_current_thread = time.ctime(os.path.getctime(filename))

		my_turn = 1
		for item in file_list_invest_type:
			print("check",end=" ")
			print(time.ctime(os.path.getctime(item)))
			if created_time_of_current_thread > time.ctime(os.path.getctime(item)):
				my_turn = 0
				break


		if my_turn == 1:
			print("시작 : 타입 {} {}".format(invest_type,filename))
			time.sleep(5)
			os.remove(filename)
			break
		else:
			time.sleep(1)

def main():
	#lock = threading.Lock()
	while True:
		invest_type = input("R/B")
		wait_time = int(input(""))
		t = threading.Thread(target=worker, args=(invest_type,wait_time,))
		t.start()

main()