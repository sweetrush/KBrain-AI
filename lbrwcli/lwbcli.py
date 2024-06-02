import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Initialize QtWebEngine 
    QWebEngineProfile.defaultProfile() 

    view = QWebEngineView()
    view.setUrl(QUrl("https://www.google.com"))
    view.show()

    sys.exit(app.exec_())