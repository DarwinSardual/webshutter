from threading import Thread, Lock
import time, os, subprocess, sys
from config import Config

sys.path.append(os.path.join(os.getcwd(), "app/data"))
from urls import Status

class Shutter():
	__lock = Lock()
	def __init__(self):
		self.max_processes = 5
		self.count_processes = 0
		self.urls_to_process = []
		self.config = None
		self.app_controller = None

	def start(self):
		main = Thread(target=self.start_threading)
		main.start()
		
	def start_threading(self):
		while len(self.urls_to_process) > 0 and self.app_controller.job_is_running:
			if self.count_processes < self.max_processes:
				self.count_processes += 1
				
				url_dict = self.urls_to_process.pop(0)
				url_dict['url_obj'].status = Status.INPROGRESS
				url_dict['url_obj'].is_checked = 0
				self.update_url(url_dict['url_obj'])
				
				t = Thread(target=self.run, args=[url_dict['cmd'], url_dict['url_obj']])
				t.start()

			time.sleep(1)

	def run(self, cmd, url_obj):
		print 'urls now ', len(self.urls_to_process) , ' processing ', self.count_processes
		os.environ["PHANTOMJS_EXECUTABLE"] = str(self.config.PHANTOMJS_EXECUTABLE)
		p = subprocess.Popen(cmd, env=os.environ, stdout=subprocess.PIPE, shell=True)
		
		while True:
			line = p.stdout.readline()
			if not line:
				break
			else:
				print line

		url_obj.status = Status.COMPLETED
		self.update_url(url_obj)
		self.count_processes -= 1
		print ' processing left', self.count_processes

	def update_url(self, url_obj):
		url_obj.status_label = self.app_controller.get_status_label(url_obj.status)
		self.app_controller.update_url(url_obj)
		self.app_controller.update_row(url_obj)
