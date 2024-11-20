from PyQt5.QtCore import pyqtSignal, QThread
import asyncio
from BusinessLogic.Models.AnalysisResult import AnalysisResult
from BusinessLogic.Services.MainService import MainService
from qasync import QEventLoop, asyncSlot

class MainServiceThread(QThread):
    finished = pyqtSignal(str, AnalysisResult)
    loop: QEventLoop

    def __init__(self, main_service: MainService):
        super().__init__()
        self.main_service = main_service


    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run_async())

    async def run_async(self):
        try:
            result = await self.main_service.run_clusterization()
            self.finished.emit("Выполнена кластеризация.", result)
        except Exception as ex:
            self.finished.emit(f"Произошла ошибка во время кластеризации: {ex}")