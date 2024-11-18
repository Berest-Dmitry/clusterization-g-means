import os
import sys
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from BusinessLogic.ThreadConfig.DataDownloaderThread import DataDownloaderThread
from Persistence.DatabaseConfig.DatabaseContext import AppContext
SCRIPT_DIR =  os.path.dirname(os.getcwd()) + "\\Services"
sys.path.append(os.path.dirname(SCRIPT_DIR))
from BusinessLogic.Services.DataDownloader import DataDownloader

# главный класс приложения
class MainApp(QObject):
    def __init__(self):
        self.data_downloader_service = DataDownloader()

    def start_data_download(self):
        try:
            self.thread = DataDownloaderThread(self.data_downloader_service)
            self.thread.finished.connect(self.on_data_download_finished)
            self.thread.start()
        except BaseException as e:
            print(str(e))


    def on_data_download_finished(self, message):
        print(message)



app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./UI/main.qml')

#запуск приложения
main_app = MainApp()
main_app.start_data_download()

sys.exit(app.exec())