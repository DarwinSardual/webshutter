from enum import Enum

class Url():

	def __init__(self):
		self.id = -1
		self.url = ""
		self.status = Status.PENDING,
		self.status_label = ""
		self.is_checked = 1



class Status(Enum):
	NONE = -2
	ERROR = -1
	PENDING = 0
	INPROGRESS = 1
	COMPLETED = 2
	