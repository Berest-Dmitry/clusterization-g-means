import asyncio
from PyQt5.QtCore import QThread, pyqtSignal
from BusinessLogic.Services.DataDownload.DataDownloader import DataDownloader
from qasync import QEventLoop, asyncSlot


class DataDownloaderThread(QThread):
    finished = pyqtSignal(str)
    loop: QEventLoop

    def __init__(self, data_downloader: DataDownloader):
        super().__init__()
        self.data_downloader = data_downloader

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.run_async())

    @asyncSlot()
    async def run_async(self):
        try:
            await self.data_downloader.extract_data()
            self.finished.emit("Выполнена выгрузка данных.")
        except Exception as ex:
            self.finished.emit(f"Произошла ошибка во время выгрузки: {ex}")

