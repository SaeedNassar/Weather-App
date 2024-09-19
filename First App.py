import sys
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QApplication, QMainWindow,QLineEdit, QDesktopWidget, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout,QPushButton
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt
import requests
from lxml import html
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #38b6ff;") 
        self.setWindowTitle("Weather App")
        self.setGeometry(0,680,400,400)
        self.setWindowIcon(QIcon(resource_path("appicon1.png")))
        self.center_window()
        self.secondinitUI()
    def center_window(self):
        # Get the geometry of the screen and the window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def firstinitUI(self):
        pixmap=QPixmap(resource_path("appicon2.png"))
        
        label1 = QLabel(self)
        label1.setPixmap(pixmap)
        label1.setGeometry(120,0,150,120)
        label1.setScaledContents(True)
        label = QLabel("Weather App",self)
        label.setFont(QFont("Ariel",30))
        label.setGeometry(0,100,400,100)
        label.setStyleSheet("color: black;"
                            "font-weight: bold;")
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
    def secondinitUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.firstinitUI()
        self.degreel = QLabel(self)
        self.degreel.setFont(QFont("Ariel",15))
        self.degreel.setGeometry(60,200,400,100)
        self.degreel.setStyleSheet("color: black;"
                            "font-weight: bold;")
        self.country = QLineEdit(self)
        self.state = QLineEdit(self)
        self.city = QLineEdit(self)
        self.country.setFont(QFont("Ariel",15))
        self.country.setPlaceholderText("Country")
        self.country.setGeometry(5,175,135,50)
        self.country.setStyleSheet("color: black;"
                            "background-color: white;"
                            "font-weight: bold;")
        self.state.setFont(QFont("Ariel",15))
        self.state.setPlaceholderText("State")
        self.state.setGeometry(149,175,120,50)
        self.state.setStyleSheet("color: black;"
                            "background-color: white;"
                            "font-weight: bold;")
        self.city.setFont(QFont("Ariel",15))
        self.city.setPlaceholderText("City")
        self.city.setGeometry(277,175,120,50)
        self.city.setStyleSheet("color: black;"
                            "background-color: white;"
                            "font-weight: bold;")
        
        self.button = QPushButton("What Is The Weather?",self)#"Calculate")
        self.button.setGeometry(125,289,150,100)
        self.button.setFont(QFont("Ariel"))
        self.button.setStyleSheet("color: black;"
                            "background-color: yellow;"
                            "font-weight: bold;")
        self.button.clicked.connect(self.on_click)
        
    def on_click(self):
        response=requests.get("https://www.yr.no/en/search?q="+self.city.text()).content
        tree = html.fromstring(response)
        first_result = tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/main/div[3]/div/ol/li[1]')
        first_result = first_result[0].text_content()
        if self.country.text() in first_result and self.state.text() in first_result and self.city.text() in first_result:
            first_result_href = tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/main/div[3]/div/ol/li[1]//a[@class="search-results-list__item-anchor"]/@href')[0]
            response=requests.get("https://www.yr.no"+first_result_href).content
            tree = html.fromstring(response)
            self.degree = tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/main/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/span')[0].text_content()
            self.feels_like=tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/main/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/span')[0].text_content()
        else:
            first_result_href = tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/main/div[3]/div/ol/li[2]//a[@class="search-results-list__item-anchor"]/@href')[0]
            response=requests.get("https://www.yr.no"+first_result_href).content
            tree = html.fromstring(response)
            self.degree = tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/main/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/div/span')[0].text_content()
            
            self.feels_like=tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/main/div[3]/div[1]/div/div/div/div/div[2]/div[1]/div/span')[0].text_content()
        text="Degree is:"+self.degree+"C "+self.feels_like+"C"
        self.degreel.setText(text)

def main():
    app = QApplication(sys.argv)
    window = MainWin()
    window.show()
    sys.exit(app.exec_())
if __name__=="__main__":
    main()