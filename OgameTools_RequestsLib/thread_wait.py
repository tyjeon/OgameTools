import re
import time
import threading
import os
import shutil

def main():
	if os.path.isdir("temp"):
		shutil.rmtree("temp")
	os.mkdir("temp")

	while True:
		try:
			wait_time = input("")
		except:
			continue

		if wait_time == "p":
			show_current_thread()
			continue
		elif wait_time == "k":
			kill_thread()
			continue
		elif wait_time == "exit":
			return
		else:
			wait_time = int(wait_time)

		queue_thread = threading.Thread(target=wait_input_time, args = (wait_time,))
		queue_thread.start()

def wait_input_time(duration):
	thread_list = threading.enumerate()
	current_thread = thread_list[len(thread_list)-1]
	current_thread_number = re.compile("(?<=started )\d+").search(str(current_thread)).group()
	current_thread_file_path = "temp/{}.txt".format(current_thread_number)
	with open(current_thread_file_path,encoding="utf-8",mode="w+") as f:
		f.write(str(duration))

	countdown(duration,current_thread_number)
	print("앞 스레드가 끝났습니다.")
	os.remove(current_thread_file_path)

def countdown(duration,current_thread_number):
	current_thread_file_path = "temp/{}.txt".format(current_thread_number)

	while True:
		current_thread_index = get_current_thread_index(current_thread_number)

		time.sleep(1)

		if int(current_thread_index) == 1:
			if os.path.isfile("temp/stop_first_thread_flag.txt"):
				os.remove("temp/stop_first_thread_flag.txt")
				return

			with open(current_thread_file_path,encoding="utf-8",mode="w+") as f:
				duration = duration - 1
				f.write(str(duration))

		else:
			with open(current_thread_file_path,encoding="utf-8",mode="r+") as f:
				duration = int(f.read())

		if duration <= -999:
			return
		elif duration <= 0:
			break

def get_current_thread_index(current_thread_number):
	thread_list = threading.enumerate()
	for i in range(1,len(thread_list)):
		if str(current_thread_number) == re.compile("(?<=started )\d+").search(str(thread_list[i])).group():
			return i

def kill_thread():
	show_current_thread()
	kill_thread_index = int(input("Thread number : "))
	target_thread_number = re.compile("(?<=started )\d+").search(str(threading.enumerate()[kill_thread_index])).group()
	target_thread_file_path = "temp/{}.txt".format(target_thread_number)
	if kill_thread_index == 1:
		with open("temp/stop_first_thread_flag.txt",encoding="utf-8",mode="w+") as f:
			f.write("1")
	else:
		with open(target_thread_file_path,encoding="utf-8",mode="w+") as f:
			f.write("-999")

def show_current_thread():
	for i in range(1,len(threading.enumerate())):
		thread_name = re.compile("(?<=started )\d+").search(str(threading.enumerate()[i])).group()
		with open("temp/"+thread_name+".txt",encoding="utf-8",mode="r+") as f:
				time = f.read()

		print("Thread {} : {} sec left.".format(str(i),time))

main()