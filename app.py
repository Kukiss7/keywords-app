import sys
from website_analyse import WebData, WebAnalyse
from PyQt4 import QtGui, QtCore
import validators


class Window(QtGui.QMainWindow):

	
	def __init__(self, width=500, height=500, x_start_point=50, y_start_point=100):
		super(Window, self).__init__()
		self.width = width
		self.height = height
		self.x_start_point = x_start_point
		self.y_start_point = y_start_point
		self.answers = ["Here the results will be shown.",
						"Waiting for the results...",
						"Url seems to be incorrect.\n\nPlease try again",
						"Couldn't find any keywords"]

		self.setGeometry(x_start_point, y_start_point, width, height)
		self.setWindowTitle("keywords-analyse")
		self.setWindowIcon(QtGui.QIcon('logo.png'))

		self.insert_url_area = QtGui.QTextEdit('insert url', self)
		self.scrap_btn = QtGui.QPushButton("Scrap", self)
		self.results_area = QtGui.QTextEdit(self.answers[0], self)
		self.quit_btn = QtGui.QPushButton("Quit", self)
		
		self.home()


	def home(self):
		self.insert_url_area.resize(self.width//2, 40)
		self.insert_url_area.move(self.width//4, 20)

		self.scrap_btn.clicked.connect(self.scrap_website)
		self.scrap_btn.resize(40, 30)
		self.scrap_btn.move(self.width//2-20, 70)

		self.results_area.resize(int(self.width*0.8), self.height-200)
		self.results_area.move(self.width*(1-0.8)//2, 120)
		self.results_area.setReadOnly(True)

		self.quit_btn.clicked.connect(self.close_application)
		self.quit_btn.resize(100, 20)
		self.quit_btn.move(self.width//2-50, self.height-40)

		self.show()

	def scrap_website(self):
		choice = QtGui.QMessageBox.question(self, 
											"robot/user_agent", 
											"Simulate to visit the site as a user agent?",
											 QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | QtGui.QMessageBox.Cancel)
		if choice == QtGui.QMessageBox.Yes:
			agent = 'user_agent'
		elif choice == QtGui.QMessageBox.No:
			agent = 'robot'
		else:
			return
		print('here1')
		url = self.insert_url_area.toPlainText()
		url_validation = False
		if validators.url(url):
			url_validation = True
		elif validators.domain(url):
			url = 'http://' + url
			url_validation = True

		if url_validation:
			print('here2')
			self.update_results_area(self.answers[1])
			print('here3')
			webdata = WebData(url=url, agent=agent)
			results = WebAnalyse(webdata)
			print(type(results))
			self.update_results_area(str(results))
			print('here3')
		else:
			self.update_results_area(self.answers[2])
			return

	def update_results_area(self, text):
		self.results_area.setPlainText(text)


	def close_application(self):
		sys.exit()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec())