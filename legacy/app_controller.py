'''
Controller for app.pyz

'''
from PySide import QtCore, QtGui
import time, subprocess, os, sys, pprint
from config import Config
from app import Ui_WebShutter
import time, urllib
from threading import Thread

sys.path.append(os.path.join(os.getcwd(), "app/util"))
sys.path.append(os.path.join(os.getcwd(), "app/data"))
sys.path.append(os.path.join(os.getcwd(), "app/action"))

from db import SqliteCon
from urls import Url, Status
from shutter import Shutter 

class AppController():
	
	def __init__(self, _QMainWindow):
		#inserted widgets
		self.checkbox_all = QtGui.QCheckBox()
		_QMainWindow.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
		
		self.ui = Ui_WebShutter()
		self.ui.setupUi(_QMainWindow)
		self.config = Config()
		self.init_db()
		self.init_settings()
		self.init_signals()
		self.init_ui_layout()
		self.job_thread = None
		self.job_is_running = False

	def init_settings(self):
		self.config.load();
		#self.check_config();

		self.ui.textbox_output_dir.clear()
		self.ui.textbox_output_dir.appendHtml(self.config.OUTPUT_ROOT_DIR)

		if not os.path.exists(self.config.OUTPUT_ROOT_DIR):
			os.makedirs(self.config.OUTPUT_ROOT_DIR)
		 
	def init_signals(self):
		self.ui.btn_add.clicked.connect(self.btn_add_on_click)
		self.ui.btn_browse.clicked.connect(self.btn_browse_on_click)
		self.ui.table_urls.cellClicked.connect(self.table_urls_on_cell_clicked)
		self.checkbox_all.clicked.connect(self.checkbox_all_on_click)
		self.ui.btn_search.clicked.connect(self.btn_search_on_click)
		self.ui.btn_delete.clicked.connect(self.btn_delete_on_click)
		self.ui.btn_stop.clicked.connect(self.btn_stop_on_click)
		self.ui.btn_start.clicked.connect(self.btn_start_on_click)
	
	def check_config(self):
		if self.config.PYTHON_PATH == "":
			msg = "Python path not configured"
			msgBox = QtGui.QMessageBox()
			msgBox.setText(msg)
			msgBox.exec_()

			dialog = QtGui.QFileDialog()
			#dialog.labelText(msg)
			dialog.setDirectory(self.ui.textbox_output_dir.toPlainText())
			dialog.setFileMode(QtGui.QFileDialog.Directory)
			dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
			
			if dialog.exec_():
				self.config.PYTHON_PATH = dialog.directory().absolutePath()
				self.check_config()

	''' events '''
	def btn_add_on_click(self):
		#self.process_init()
		#get url/s
		#max # of urls to process is 20
		url_raw = self.ui.textbox_url.toPlainText()
		temp_raw = url_raw.replace(' ', ',')
		temp_raw = temp_raw.replace('\r\n', ',')
		temp_raw = temp_raw.replace('\n', ',')
		temp_urls = temp_raw.split(",")

		for url in temp_urls:
			if str(url).strip() != "":
				url_obj = Url()
				url_obj.url = url
				url_obj.status = Status.PENDING
				url_obj.status_label = self.get_status_label(Status.PENDING)
				url_obj.is_checked = 1
				id = self.insert_url(url_obj)
				if id > 0 :
					url_obj.id = id;
					self.add_url(url_obj)

	def btn_browse_on_click(self):
		dialog = QtGui.QFileDialog()
		dialog.setDirectory(self.ui.textbox_output_dir.toPlainText())
		dialog.setFileMode(QtGui.QFileDialog.Directory)
		dialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
		
		if dialog.exec_():
			self.ui.textbox_output_dir.clear()
			self.ui.textbox_output_dir.appendPlainText(dialog.directory().absolutePath())

	def table_urls_on_cell_clicked(self, row, column):
		if column == 0:
			url_obj = Url()
			item = self.ui.table_urls.item(row, 3)
			url_obj.id = item.text()
			item = self.ui.table_urls.item(row, 0)
			url_obj.is_checked = 1
			if item.checkState() == QtCore.Qt.Unchecked:
				url_obj.is_checked = 0
			item = self.ui.table_urls.item(row, 1)
			url_obj.url = item.text()
			url_obj.status = Status.PENDING
			if item.text() == self.get_status_label(Status.COMPLETED):
				url_obj.status = Status.COMPLETED
			elif item.text() == self.get_status_label(Status.ERROR):
				url_obj.status = Status.ERROR
			elif item.text() == self.get_status_label(Status.INPROGRESS):
				url_obj.status = Status.INPROGRESS

			self.update_url(url_obj)
	
	def checkbox_all_on_click(self):
		cur_val = self.checkbox_all.checkState()
		i = 0
		while i < self.ui.table_urls.rowCount():
			item = self.ui.table_urls.item(i, 0)
			item.setCheckState(cur_val)
			i = i + 1

	def btn_search_on_click(self):
		to_search = self.ui.textbox_search.toPlainText()
		to_search = to_search.strip()
		factor = self.ui.comboBox_search.currentText()
		self.fill_table(self.search(to_search, factor))

	def btn_delete_on_click(self):
		url_objs = self.get_urls_in_table()
		for url_obj in url_objs:
			if url_obj.is_checked == 1:
				self.delete_row(url_obj.id)
				self.delete_url(url_obj.id)

	def btn_stop_on_click(self):
		if self.job_thread != None:
			self.job_is_running = False

	def btn_start_on_click(self):
		#url_objs = self.get_urls_in_table()
		#for url_obj in url_objs:
		#	if url_obj.is_checked == 1:
		#		url_obj.status = Status.INPROGRESS
		#		url_obj.status_label = self.get_status_label(Status.INPROGRESS)
		#		self.update_url(url_obj)
		#		self.update_row(url_obj)
		self.process_init()

	''' UI rules '''
	def init_ui_layout(self):
		table = self.ui.table_urls
		table.setColumnWidth(0, 20)
		table.setColumnWidth(1, 400)
		table.setColumnWidth(2, 102)
		table.hideColumn(3)

		#position a checkbox on column 1
		header = self.ui.table_urls.horizontalHeader()
		self.checkbox_all.setParent(header)
		self.checkbox_all.setGeometry(3, 3, 17, 17)

		#get data from db and set up table
		data = self.get_all_data()
		self.fill_table(data)

	def add_url(self, url_obj):
		table = self.ui.table_urls
		rowCount = table.rowCount()
		table.insertRow(rowCount)

		row = rowCount;
		cell = QtGui.QTableWidgetItem()
		is_checked = QtCore.Qt.CheckState.Checked
		if url_obj.is_checked == 0:
			is_checked = QtCore.Qt.CheckState.Unchecked
		cell.setCheckState(is_checked)
		cell.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
		table.setItem(row, 0, cell)

		cell = QtGui.QTableWidgetItem(url_obj.url);
		cell.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsEnabled)
		table.setItem(row, 1, cell)
		
		cell = QtGui.QTableWidgetItem()
		cell.setText(url_obj.status_label)
		cell.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsEnabled)
		table.setItem(row, 2, cell)

		cell = QtGui.QTableWidgetItem()
		cell.setText(str(url_obj.id))
		cell.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsEnabled)
		table.setItem(row, 3, cell)

	def fill_table(self, data):
		#remove all rows
		while self.ui.table_urls.rowCount() != 0:
			self.ui.table_urls.removeRow(0)

		if data != None:
			for row in data:
				url_obj = Url()
				url_obj.id = row[0]
				url_obj.url = row[1]
				url_obj.status = row[2]
				url_obj.status_label = row[3]
				url_obj.is_checked = row[4]

				self.add_url(url_obj)

	def update_row(self, url_obj):
		table = self.ui.table_urls
		rows = table.rowCount
		row = 0
		while row < table.rowCount():
			id = table.item(row, 3).text()
			if int(url_obj.id) == int(id):
				
				cell = QtGui.QTableWidgetItem()
				is_checked = QtCore.Qt.CheckState.Checked
				if url_obj.is_checked == 0:
					is_checked = QtCore.Qt.CheckState.Unchecked
				cell.setCheckState(is_checked)
				cell.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
				self.ui.table_urls.setItem(row, 0, cell)

				cell = QtGui.QTableWidgetItem(url_obj.url);
				cell.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsEnabled)
				self.ui.table_urls.setItem(row, 1, cell)
				
				cell = QtGui.QTableWidgetItem()
				cell.setText(url_obj.status_label)
				cell.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsEnabled)
				self.ui.table_urls.setItem(row, 2, cell)

				cell = QtGui.QTableWidgetItem()
				cell.setText(str(url_obj.id))
				cell.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsEnabled)
				self.ui.table_urls.setItem(row, 3, cell)

				break
			
			row = row + 1

	def delete_row(self, url_id):
		table = self.ui.table_urls
		rows = table.rowCount
		row = 0
		while row < table.rowCount():
			item = table.item(row, 0)
			if item.checkState() == QtCore.Qt.Checked:
				table.removeRow(row)
				break
			row = row + 1

	def get_urls_in_table(self):
		table = self.ui.table_urls
		url_objs = []
		row = 0
		while row < table.rowCount():
			url_obj = Url()

			url_obj.is_checked = 1
			if table.item(row, 0).checkState() == QtCore.Qt.Unchecked:
				url_obj.is_checked = 0

			url_obj.url = table.item(row, 1).text()
			
			url_obj.status = self.get_status(table.item(row, 2).text())

			url_obj.status_label = table.item(row, 2).text()

			url_obj.id = table.item(row, 3).text()
			
			url_objs.append(url_obj)
			
			row = row + 1

		return url_objs

	def get_checked_urls_in_table(self):
		url_objs = self.get_urls_in_table()
		urls_result = []
		for url_obj in url_objs:
			if url_obj.is_checked == 1:
				urls_result.append(url_obj)
		return urls_result

	''' b-rules '''
	def set_job_settings(self, urls_to_process):
		self.job_settings = {
			'urls_to_process' : urls_to_process,
			'max_processes' : 2,
			'cur_processes' : 0
		}
	
	def default_job_settings(self):
		self.job_settings = {
			'urls_to_process' : None,
			'max_processes' : 5,
			'cur_processes' : 0
		}

	def process_init_old(self):
		print "Process : initialize"

		#use config
		is_mobile = False
		if self.ui.radio_mobile.isChecked()  == True:
			is_mobile = True
		
		size = { 'width': 1024, 'height' : 960}
		uc_width = self.ui.textbox_width.toPlainText()
		uc_height = self.ui.textbox_height.toPlainText()
		if uc_width.isdigit():
			size['width'] = uc_width
		if uc_height.isdigit():
			size['height'] = uc_height
		
		uc_output_dir = self.ui.textbox_output_dir.toPlainText()
		uc_sub_folder = self.ui.textbox_output_sub_dir.toPlainText()
		output_dir = os.path.join(uc_output_dir, uc_sub_folder)
		
		urls = []
		process_counter = 0
		for url in temp_urls:
			if process_counter >= self.config.MAX_PROCESSES:
				break
			if url == "":
				continue
			process_counter = process_counter + 1

			url_clean = url.replace("http://", "")	
			urls.append(url_clean)
			
			filename = url + "_" + time.strftime('%Y%M%d%H%M%S%Ms') + self.config.IMAGE_EXT

			size_args = "--size="+str(size['width'])+"x"+str(size['height'])
			is_mobile_args = "--desktop"
			if is_mobile == True:
				is_mobile_args = "--mobile"
			output_dir_args = "--output="+output_dir
			filename_args = "--filename="+filename

			cmd = ['python', self.config.CASPERJS_PATH, self.config.SCREENSHOT_SCRIPT_PATH, url,
				size_args, is_mobile_args, output_dir_args, filename_args
			]

			self.process_start(cmd)

	def process_init_old2(self):
		print "Process : initialize"

		#use config
		is_mobile = False
		if self.ui.radio_mobile.isChecked()  == True:
			is_mobile = True
		
		size = { 'width': 1024, 'height' : 960}
		uc_width = self.ui.textbox_width.toPlainText()
		uc_height = self.ui.textbox_height.toPlainText()
		if uc_width.isdigit():
			size['width'] = uc_width
		if uc_height.isdigit():
			size['height'] = uc_height
		
		uc_output_dir = self.ui.textbox_output_dir.toPlainText()
		uc_sub_folder = self.ui.textbox_output_sub_dir.toPlainText()
		output_dir = os.path.join(uc_output_dir, uc_sub_folder)
		
		self.set_job_settings(self.get_checked_urls_in_table())
		
		while len(self.job_settings['urls_to_process']) > 0:
			if self.job_settings['cur_processes'] < self.job_settings['max_processes']:
				url_obj = self.job_settings['urls_to_process'].pop()
				url = url_obj.url
				url_clean = url.replace("http://", "")	
				
				filename = url + "_" + time.strftime('%Y%M%d%H%M%S%Ms') + self.config.IMAGE_EXT

				size_args = "--size="+str(size['width'])+"x"+str(size['height'])
				is_mobile_args = "--desktop"
				if is_mobile == True:
					is_mobile_args = "--mobile"
				output_dir_args = "--output="+output_dir
				filename_args = "--filename="+filename

				cmd = ['python', self.config.CASPERJS_PATH, self.config.SCREENSHOT_SCRIPT_PATH, url,
					size_args, is_mobile_args, output_dir_args, filename_args
				]
				t = Thread(target=self.process_start, args=[cmd, url_obj, self])
				t.start()

			print 'Waiting : urls left - ' , len(self.job_settings['urls_to_process']) 
			time.sleep(10)

	def process_init(self):
		print "Process : initialize"

		#use config
		is_mobile = False
		if self.ui.radio_mobile.isChecked()  == True:
			is_mobile = True
		
		size = { 'width': 1024, 'height' : 960}
		uc_width = self.ui.textbox_width.toPlainText()
		uc_height = self.ui.textbox_height.toPlainText()
		if uc_width.isdigit():
			size['width'] = uc_width
		if uc_height.isdigit():
			size['height'] = uc_height
		
		uc_output_dir = self.ui.textbox_output_dir.toPlainText()
		uc_sub_folder = self.ui.textbox_output_sub_dir.toPlainText()
		output_dir = os.path.join(uc_output_dir, uc_sub_folder)
		
		checked_urls = self.get_checked_urls_in_table()
		urls_to_process = []

		for url_obj in checked_urls:
			url = url_obj.url
			url_clean = url.replace("http://", "")	
			
			filename = url + "_" + time.strftime('%Y%M%d%H%M%S%Ms') + self.config.IMAGE_EXT

			size_args = "--size="+str(size['width'])+"x"+str(size['height'])
			is_mobile_args = "--desktop"
			if is_mobile == True:
				is_mobile_args = "--mobile"
			output_dir_args = "--output="+output_dir
			filename_args = "--filename="+filename

			cmd = ['python', self.config.CASPERJS_PATH, self.config.SCREENSHOT_SCRIPT_PATH, url,
				size_args, is_mobile_args, output_dir_args, filename_args
			]

			url_dict = {}
			url_dict['url_obj'] = url_obj
			url_dict['cmd'] = cmd

			urls_to_process.append(url_dict)

		self.job_thread = Shutter()
		self.job_thread.urls_to_process = urls_to_process
		self.job_thread.config = self.config
		self.job_thread.app_controller = self
		self.job_thread.start()
		self.job_is_running = True

	''' db stuff '''
	def init_db(self):
		sql = """CREATE TABLE IF NOT EXISTS 'urls' (
			'id'	INTEGER PRIMARY KEY AUTOINCREMENT,
			'url'	TEXT,
			'status'	INTEGER,
			'status_label' TEXT,
			'is_checked'	INTEGER
		)"""
		db = SqliteCon()
		db.execute(sql)

	def insert_url(self, url_obj):
		sql = "INSERT INTO urls(url, status, status_label, is_checked) VALUES(?, ?, ?, ?)"
		params = (url_obj.url, url_obj.status.value, self.get_status_label(url_obj.status), url_obj.is_checked)
		con = SqliteCon()
		return con.insert(sql, params)

	def update_url(self, url_obj):
		sql = "UPDATE urls SET url = ?, is_checked = ?, status = ? , status_label = ? WHERE id = ?"
		params = (url_obj.url, url_obj.is_checked, url_obj.status.value, self.get_status_label(url_obj.status), url_obj.id)
		con = SqliteCon()
		con.update(sql, params)

	def search(self, to_search, factor):
		sql = "SELECT * FROM urls "
		params = ()
		if to_search != "":
			if factor.lower() == "url":
				sql = sql + "WHERE url LIKE ? "
				params = (to_search+'%',)
			elif factor.lower() == "status":
				sql = sql + "WHERE status LIKE ? "
				params = (to_search+'%',)
			else:
				sql = sql + "WHERE url LIKE ? OR status LIKE ? "
				params = (to_search+'%', to_search+'%')
		db = SqliteCon()
		return db.fetchall(sql, params)

	def get_checked_urls(self):
		sql = "SELECT * FROM urls WHERE is_checked = ?"
		params = (1,)
		db = SqliteCon()
		return db.fetchall(sql, params)

	def get_all_data(self):
		sql = ''' 
			SELECT * 
			FROM urls 
		'''
		db = SqliteCon()
		data = db.fetchall(sql)
		return data

	def delete_url(self, url_id):
		sql = "DELETE FROM urls WHERE id = ?"
		params = (url_id,)
		db = SqliteCon()
		db.delete(sql, params)
	
	''' others '''
	def get_status_label(self, status):
		if status == Status.PENDING:
			return "Pending"
		elif status == Status.COMPLETED:
			return "Completed"
		elif status == Status.ERROR:
			return "Error"
		elif status == Status.INPROGRESS:
			return "In Progress"
		return ""
	
	def get_status(self, status_label):
		if status_label.lower() == "error":
			return Status.Error
		if status_label.lower() == "pending":
			return Status.PENDING
		if status_label.lower() == "in progress":
			return Status.INPROGRESS
		if status_label.lower() == "completed":
			return Status.COMPLETED
		return Status.NONE
