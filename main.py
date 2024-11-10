import os
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from Persistence.DatabaseConfig.DatabaseContext import AppContext

SCRIPT_DIR =  os.path.dirname(os.getcwd()) + "\\Services"
sys.path.append(os.path.dirname(SCRIPT_DIR))
from BusinessLogic.Services.data_extractor_service import DataExtractor

users_list: list

#инициализация контекста БД
db_context = AppContext()
db_context.init_engine()

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./UI/main.qml')

data_extractor = DataExtractor()
try:
    data_extractor.BasicPuplish()
    data_extractor.BasicConsume()
except Exception as ex:
    print(ex)

sys.exit(app.exec())