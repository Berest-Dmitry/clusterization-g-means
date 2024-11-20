from BusinessLogic.Models.AnalysisResult import AnalysisResult
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
        result: AnalysisResult = None
        a_type = input("Введите тип проводимой кластеризации: ")
        initial_num_clusters = input("Введите начальное кол-во кластеров: ")
        if a_type == 'gender_to_age':
            users_distribution = self._selector.users_age_to_gender()
            result = self._clusterizationBlogic.conduct_clusterization(a_type, users_distribution, int(initial_num_clusters))
        elif a_type == 'num_of_comments':
            age_to_comments = self._selector.users_age_to_number_of_comments()
            result = self._clusterizationBlogic.conduct_clusterization(a_type, age_to_comments, int(initial_num_clusters))
        elif a_type == 'num_of_posts':
            age_to_posts = self._selector.users_age_to_number_of_posts()
            result = self._clusterizationBlogic.conduct_clusterization(a_type, age_to_posts, int(initial_num_clusters))
        return  result

