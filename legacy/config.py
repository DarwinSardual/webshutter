import json, os, StringIO

class Config:
	def __init__(self):
		self.curr_dir = os.getcwd()
		self.PYTHON_PATH = "";
		self.PHANTOMJS_EXECUTABLE = os.path.join(self.curr_dir, "scripts/phantomjs/phantomjs.exe")
		self.CASPERJS_PATH = os.path.join(self.curr_dir, "scripts/casperjs/bin/casperjs")
		self.SCREENSHOT_SCRIPT_PATH = os.path.join(self.curr_dir, "scripts/capture.js") 
		self.IMAGE_EXT =".png"
		self.OUTPUT_ROOT_DIR = os.path.join(self.curr_dir, "save")
		self.MAX_PROCESSES = 20

	def load(self):
		self.read();

	def to_Object(self,json_string):
		self.__dict__ = json.loads(json_string)

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def write(self):
		try:
			with open(os.path.join(self.curr_dir, 'config.json'),'w') as f:
				f.write(self.to_JSON())
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)

	def read(self):
		try:
			if not os.path.exists(os.path.join(self.curr_dir, 'config.json')):
				self.write()
			with open(os.path.join(self.curr_dir, 'config.json'), 'r') as f:
				self.to_Object(f.read())
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
