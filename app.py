import sys
from website_analyse import WebData, WebAnalyse
from PyQt4 import QtGui
import validators


class Window(QtGui.QMainWindow):
	"""
		GUI window representation

		width: width of the window
		height: height of the window
		x_start_point: horizontal start poin
		y_start_point: vertical start point
		answers: possible statements in results area when there is no results
	"""	
	def __init__(self, width=500, height=500, x_start_point=50, y_start_point=100):
		super(Window, self).__init__()
		self.width = width
		self.height = height
		self.x_start_point = x_start_point
		self.y_start_point = y_start_point
		self.answers = ["Here the results will be shown.",
						"Waiting for the results...",
						"Url seems to be incorrect.\n\nPlease try again",
						"Couldn't find any keywords",
						"We encountered some problems; Error: "]

		self.setGeometry(x_start_point, y_start_point, width, height)
		self.setWindowTitle("keywords-analyse")
		self.setWindowIcon(QtGui.QIcon('logo.png'))

		self.insert_url_area = QtGui.QTextEdit('insert url', self)
		self.scrap_btn = QtGui.QPushButton("Scrap", self)
		self.results_area = QtGui.QTextEdit(self.answers[0], self)
		self.quit_btn = QtGui.QPushButton("Quit", self)

		self.home()
		self.show()

	def home(self):
		"""
			This func puts GUI elements on their places
		"""
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
	def scrap_website(self):
		"""
			Starts scraping part
			Inititated with scrap_btn
			First checks for confirmation and used agent
			Validates given by user url
			Adds 'http://' to url if 'http://' or 'https://' is not present, for scrapper to work correctly
			Scraps given site and analyzes it

		"""
		# pop up window for user agent choice and confirmation
		# return with None if window is closed or canceled
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

		# url validation part
		# if it's incorrect show message - self.answers[2] and return with None
		url = self.insert_url_area.toPlainText()
		url_validation = False
		if validators.url(url):
			url_validation = True
		elif validators.domain(url):
			url = 'http://' + url
			url_validation = True
		else:
			self.update_results_area(self.answers[2])
			return

		# scraping and data analysis part
		# shows results in results area
		if url_validation:
			self.update_results_area(self.answers[1])
			webdata = WebData(url=url, agent=agent)
			if webdata.have_data:
				results = WebAnalyse(webdata)
				self.update_results_area(str(results))
			else:
				text = self.answers[4] + webdata.http_error
				self.update_results_area(text)

	def update_results_area(self, message):
		self.results_area.setPlainText(message)

	def close_application(self):
		sys.exit()


def main():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec())


if __name__ == '__main__':
	main()