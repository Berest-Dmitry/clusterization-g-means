import os
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from Persistence.DatabaseConfig.DatabaseContext import AppContext
SCRIPT_DIR =  os.path.dirname(os.getcwd()) + "\\Services"
sys.path.append(os.path.dirname(SCRIPT_DIR))
from BusinessLogic.Services.DataDownloader import DataDownloader

#users_list: list

#инициализация контекста БД
db_context = AppContext()
db_context.init_engine()

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./UI/main.qml')

data_downloader_service = DataDownloader()
try:
    data_downloader_service.extract_data()
except Exception as ex:
    print(ex)

sys.exit(app.exec())