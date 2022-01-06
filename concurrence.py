import logging
import random
import threading
import time
import sys

PASSENGERS = 1
CARS = 1

# Console colors
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	GRAY = '\u001b[38;5;240m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

logging.basicConfig(level=logging.DEBUG,format=f'{bcolors.OKCYAN}(%(threadName)-10s){bcolors.ENDC} %(message)s',)

class ActivePool(object):
	def __init__(self):
		super(ActivePool, self).__init__()
		self.active = []
		self.lock = threading.Lock()

	def giveARide(self, name):
		with self.lock:
			self.active.append(name)
			logging.debug(f"Car is riding {self.active}")

	def waitPassenger(self, name):
		with self.lock:
			self.active.remove(name)
			logging.debug(f"Cars are waiting passenger... {self.active}")

def passenger(s, pool, id):
	logging.debug(f"{bcolors.OKGREEN}Passenger {id} waiting... {bcolors.ENDC}")
	with s:
		name = threading.current_thread().name
		pool.giveARide(name)
		ride_time = random.randint(5,10)
		for r in range(ride_time):
			time.sleep(1)
		pool.waitPassenger(name)

if __name__ == '__main__':
	if len(sys.argv) >= 3:
		PASSENGERS = int(sys.argv[1])
		CARS = int(sys.argv[2])
	else:
		print("[E] Program usage: python concurrence.py <PASSENGERS> <CARS>")
		exit()
	pool = ActivePool()
	s = threading.Semaphore(CARS)
	for i in range(PASSENGERS):
		t = threading.Thread(target=passenger, name=f"Passenger {i + 1}", args=(s, pool, i))
		t.start()