from BusinessLogic.Services.Clusterization.ClusterizationService import ClusterizationService
from BusinessLogic.Services.Clusterization.DataSelector import DataSelector


# класс главного сервиса проекта
class MainService:
    _selector: DataSelector
    _clusterizationBlogic: ClusterizationService

    def __init__(self):
        self._selector = DataSelector()
        self._clusterizationBlogic = ClusterizationService()

    # метод запуска процесса кластеризации
    async def run_clusterization(self):
        await self._selector.load_data()
