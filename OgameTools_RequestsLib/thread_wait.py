import threading
import queue
import time

def worker(q):
	while True:
		threads = threading.enumerate()
		previous_index = threading.enumerate().index(threading.current_thread()) - 1
		
		if previous_index == 0:
			print(threads)
			item = q.get()
			time.sleep(2)
			print(item)
			break
		else:
			time.sleep(1)
			continue

if __name__ == "__main__":
	q = queue.Queue()
	while True:
		t = threading.Thread(target=worker, args=(q,))
		t.start()

		item = int(input(""))
		q.put(item)