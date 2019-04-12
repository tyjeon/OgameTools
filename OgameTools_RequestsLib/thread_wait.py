import threading
import time
import os
import shutil

def main():
	lock = threading.Lock()
	init_temp_directory()
	while True:
		invest_type = input("R/B/show/kill")
		if invest_type == "R" or invest_type == "B":
			pass
		elif invest_type == "show":
			show_thread()
			continue
		elif invest_type == "kill":
			kill_thread(lock)
			continue
		else:
			continue

		wait_time = int(input(""))
		t = threading.Thread(target=wait_schedule, args=(invest_type,wait_time,lock))
		t.start()

def init_temp_directory():
	if os.path.isdir("temp"):
		shutil.rmtree("temp")
	os.mkdir("temp")

def show_thread():
	file_list = os.listdir("temp")
	for i in range(len(file_list)):
		print("{} : {}".format(str(i+1),file_list[i]))

def kill_thread(lock):
	show_thread()
	target_index = input("")
	file_list = os.listdir("temp")
	with lock:
		os.remove("temp/{}".format(file_list[int(target_index)-1]))

def wait_schedule(invest_type,wait_time,lock):
	filename = "{}({}).txt".format(threading.current_thread().getName(),invest_type)
	create_file(filename,wait_time)

	while True: # 이부분 '컨디션'으로 처리 https://github.com/taeyongjeon/OgameTools/issues/19
		if is_my_turn(invest_type,filename):
			print("시작 : 타입 {} {}".format(invest_type,filename))
			while True:
				time.sleep(1) # 이부분을 파일과 엮어야 할 듯. Lock 걸어두고.
				with lock:
					try:
						with open("temp/{}".format(filename),encoding="utf-8",mode="r") as f:
							duration = int(f.read())
							if duration == 0:
								os.remove("temp/{}".format(filename))
								break
							duration = duration - 1
						with open("temp/{}".format(filename),encoding="utf-8",mode="w") as f:
							f.write(str(duration))
					except:
						break
		else:
			time.sleep(1)

		if not os.path.isfile("temp/{}".format(filename)):
			print("중지됨.")
			return

def create_file(filename,wait_time):
	with open("temp/{}".format(filename),encoding="utf-8",mode="w+") as f:
		f.write(str(wait_time))

def is_my_turn(invest_type,filename):
	file_list = os.listdir("temp")
	file_list_invest_type = [file for file in file_list if file.endswith("({}).txt".format(invest_type))]
	created_time_of_current_thread = time.ctime(os.path.getctime("temp/{}".format(filename)))

	for item in file_list_invest_type:
		if created_time_of_current_thread > time.ctime(os.path.getctime("temp/{}".format(item))):
			return False

	return True

main()