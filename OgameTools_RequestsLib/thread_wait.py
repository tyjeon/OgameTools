import threading
import time
import os
import shutil

class waitClass:
	def __init__(self):
		self.make_temp_directory()
		self.lock = threading.Lock()
		self.sem = {}
		for i in range(30):
			self.sem["R"+str(i+1)] = threading.Semaphore(1)
			self.sem["B"+str(i+1)] = threading.Semaphore(1)

	def main(self):
		while True:
			invest_type = input("R/B/show/kill")

			if invest_type == "R" or invest_type == "B":
				wait_time = int(input(""))
				semaphore_name = invest_type + "3"
				t = threading.Thread(target=self.wait_schedule, args=(invest_type,wait_time,self.sem[semaphore_name]))
				print(t)
				t.start()

			elif invest_type == "show":
				self.show_thread()

			elif invest_type == "kill":
				self.kill_thread()

	def make_temp_directory(self):
		try:
			shutil.rmtree("temp")
			os.mkdir("temp")
		except:
			os.mkdir("temp")

	def show_thread(self):
		file_list = os.listdir("temp")
		for i in range(len(file_list)):
			print("{} : {}".format(str(i+1),file_list[i]))

	def kill_thread(self):
		show_thread()
		target_index = input("")
		file_list = os.listdir("temp")
		with self.lock:
			os.remove("temp/{}".format(file_list[int(target_index)-1]))

	def wait_schedule(self,invest_type,wait_time,sem):
		sem.acquire()
		filename = "{}({}).txt".format(threading.current_thread().getName(),invest_type)
		file_path = "temp/{}".format(filename)

		self.create_file(filename,wait_time)
		print("시작 : 타입 {} {}".format(invest_type,filename))

		while True:
			with self.lock:
				try:
					with open(file_path,encoding="utf-8",mode="r") as f:
						duration = int(f.read())
						print(duration)
						duration = duration - 1

					with open(file_path,encoding="utf-8",mode="w") as f:
						f.write(str(duration))
				except:
					sem.release()
					return

			time.sleep(1)

			if duration == 0:
				os.remove(file_path)
				sem.release()
				return
			elif not os.path.isfile(file_path):
				print("중지됨.")
				sem.release()
				return

	def create_file(self,filename,wait_time):
		with open("temp/{}".format(filename),encoding="utf-8",mode="w+") as f:
			f.write(str(wait_time))

test = waitClass()
test.main()