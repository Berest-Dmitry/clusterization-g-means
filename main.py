import os
import sys
from PyQt5.QtCore import QObject, QThread
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
import matplotlib.pyplot as plt
from BusinessLogic.Services.MainService import MainService
from BusinessLogic.ThreadConfig.DataDownloaderThread import DataDownloaderThread
from BusinessLogic.ThreadConfig.MainServiceThread import MainServiceThread

SCRIPT_DIR =  os.path.dirname(os.getcwd()) + "\\Services"
sys.path.append(os.path.dirname(SCRIPT_DIR))
from BusinessLogic.Services.DataDownload.DataDownloader import DataDownloader

# главный класс приложения
class MainApp(QObject):
    def __init__(self):
        super().__init__()
        self.thread: QThread = None
        self.data_downloader_service = DataDownloader()
        self.main_service = MainService()

    def start_data_download(self):
        try:
            self.thread = DataDownloaderThread(self.data_downloader_service)
            self.thread.finished.connect(self.on_data_download_finished)
            self.thread.start()
        except BaseException as e:
            print(str(e))

    def start_clusterization(self):
        try:
            self.thread = MainServiceThread(self.main_service)
            self.thread.finished.connect(self.on_clusterization_finished)
            self.thread.start()
        except BaseException as e:
            print(str(e))


    def on_data_download_finished(self, message):
        print(message)
        self.start_clusterization()

    def on_clusterization_finished(self, message, result):
        print(message)
        plt.figure(figsize=(10, 6))
        columns_list = result.df.columns.tolist()
        feature1 = columns_list[0]
        feature2 = columns_list[1]
        labels = columns_list[2]
        plt.scatter(result.df[feature1], result.df[feature2], c=result.df[labels], cmap='viridis', alpha=0.6)
        plt.title(result.plot_title)
        plt.xlabel(feature1)
        plt.ylabel(feature2)
        plt.colorbar(label='Cluster Label')
        plt.show()


app = QApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./UI/main.qml')

#запуск приложения
main_app = MainApp()
main_app.start_data_download()

sys.exit(app.exec())