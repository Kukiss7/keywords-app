import sys
from website_analyse import WebData, WebAnalyse, UrlValidation
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QMessageBox
from PyQt5 import QtGui
import validators


class Window(QMainWindow):
	"""
		GUI window representation

		width: width of the window
		height: height of the window
		x_start_point: horizontal start poin
		y_start_point: vertical start point
		messages: possible statements in results area when there is no result

		GUI elements:
		insert_url_area: QTextEdit;
		results_area: QTextEdit; 
		scrap_btn: QPushButton;
		quit_btn: QPushButton;

		scrap_preparation: ScarpPreparation object when scrapping is activated
	"""	
	
	def __init__(self, width=500, height=500, x_start_point=50, y_start_point=100):
		super(Window, self).__init__()
		self.width = width
		self.height = height
		self.x_start_point = x_start_point
		self.y_start_point = y_start_point
		self.messages = ["Here the results will be shown.",
						"Waiting for the results...",
						"Url seems to be incorrect.\n\nPlease try again",
						"Couldn't find any keywords",
						"We encountered some problems; Error: ",
						"We encountered some problems.\n\nPlease try again"]

		self.setGeometry(x_start_point, y_start_point, width, height)
		self.setWindowTitle("keywords-analyse")
		self.setWindowIcon(QtGui.QIcon('logo.png'))

		self.insert_url_area = QTextEdit('insert url', self)
		self.results_area = QTextEdit(self.messages[0], self)
		self.scrap_btn = QPushButton("Scrap", self)
		self.quit_btn = QPushButton("Quit", self)
		self.scrap_preparation = None

		self.home()
		self.show()


	def home(self):
		"""	Puts GUI elements on their places
		"""
		self.insert_url_area.resize(self.width//2, 40)
		self.insert_url_area.move(self.width//4, 20)

		self.scrap_btn.clicked.connect(self.scrap_procedure)
		self.scrap_btn.resize(40, 30)
		self.scrap_btn.move(self.width//2-20, 70)

		self.results_area.resize(int(self.width*0.8), self.height-200)
		self.results_area.move(self.width*(1-0.8)//2, 120)
		self.results_area.setReadOnly(True)

		self.quit_btn.clicked.connect(self.close_application)
		self.quit_btn.resize(100, 20)
		self.quit_btn.move(self.width//2-50, self.height-40)


	def scrap_procedure(self):
		"""
			Starts scraping part
			Initiated with scrap_btn
		"""
		user_answer = self.ask_for_agent()
		if Window.is_canceled(user_answer):
			return
		else:
			given_url = self.read_insert_url_area()
			self.scrap_preparation = ScrapPreparation(given_url, user_answer)
			if self.scrap_preparation.validation:
				self.update_results_area(self.messages[1])
				webdata = WebData(url=self.scrap_preparation.validation.http_url, 
								  use_user_agent=self.scrap_preparation.use_user_agent)
				webdata.open_url()
				text = ''
				if webdata.have_data:
					results = WebAnalyse(webdata)
					text = str(results)
				else:
					if webdata.http_error:
						text = self.messages[4] + webdata.http_error
					else:
						text = self.messages[5]
				self.update_results_area(text)
			else:
				self.update_results_area(self.messages[2])



	def ask_for_agent(self):
		""" pop up window for user agent choice or cancelation
		"""
		return QMessageBox.question(self, 
									"robot/user_agent", 
									"Simulate to visit the site as a user agent?",
									QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)


	def read_insert_url_area(self):
		""" Returns data provided by user
		"""
		return self.insert_url_area.toPlainText()


	def update_results_area(self, message):
		""" Updates a message for user
		"""
		self.results_area.setPlainText(message)


	def close_application(self):
		""" Closes the application
		"""
		sys.exit()


	@staticmethod
	def is_canceled(answer):
		""" Checks if given answer is canceled
		"""
		return answer == QMessageBox.Cancel


class ScrapPreparation:
	"""
		Gathers needed elemenets to start scrapping
		url: str; provided url
		user_answer; QMessageBox.Yes or QMessageBox.No
		validation; UrlValidation object
	"""


	def __init__(self, url, user_answer):
		self.url = url
		self.user_answer = user_answer
		self.use_user_agent = self.interpret_user_answer()
		self.validation = UrlValidation(self.url)


	def interpret_user_answer(self):
		""" Turns provided QMessageBox objects into boolean answers
		"""
		if self.user_answer == QMessageBox.Yes:
			return True
		elif self.user_answer == QMessageBox.No:
			return False


def main():
	app = QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec())


if __name__ == '__main__':
	main()