import os
import sys
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import pydantic
import pydantic_xml

SCRIPT_DIR =  os.path.dirname(os.getcwd()) + "\\Services"
sys.path.append(os.path.dirname(SCRIPT_DIR))
from Services.data_extractor_service import DataExtractor

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