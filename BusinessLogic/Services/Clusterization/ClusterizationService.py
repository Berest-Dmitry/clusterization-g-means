from copy import copy
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans
from scipy.stats import normaltest
from sklearn.preprocessing import StandardScaler

from BusinessLogic.Models.AnalysisResult import AnalysisResult


# класс, содержащий логику выполнения кластеризации
class ClusterizationService:
    # исходные данные и условия анализа
    _clusterization_params = {
        'gender_to_age': ('gender', 'age'),
        'num_of_posts': ('age', 'posts_count'),
        'num_of_comments': ('age', 'comments_count'),
    }
    # результаты анализа
    current_dataframe: DataFrame


    # Функция для проверки нормальности
    @staticmethod
    def _is_normal(data: list):
        statistic, p_value = normaltest(data)
        return p_value > 0.05  # Если p_value > 0.05, то данные нормально распределены

    # базовый метод кластеризации методом g-means
    @staticmethod
    def _gmeans_base(X, initial_k=3, max_k=20):
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        k = initial_k
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(X_scaled)

        while k < max_k:
            new_labels = []
            for i in range(k):
                cluster_data = X[labels == i]
                if len(cluster_data) > 0 and ClusterizationService._is_normal(cluster_data[:, 0]):
                    new_labels.extend([i] * len(cluster_data))
                else:
                    # Разделяем кластер на два
                    kmeans_sub = KMeans(n_clusters=2, random_state=42)
                    sub_labels = kmeans_sub.fit_predict(cluster_data)
                    new_labels.extend([k + j for j in sub_labels])
                    k += 1  # Увеличиваем количество кластеров

            labels = np.array(new_labels)
            if len(set(labels)) == k:  # Если количество кластеров не изменилось
                break
        return labels

    # метод выполнения кластеризации
    def conduct_clusterization(self, analysis_type: str, data: list):
        try:
            base_param, target_param = self._clusterization_params[analysis_type]
            self.current_dataframe = pd.DataFrame(data, columns= [base_param, target_param])
            result_dataframe = copy(self.current_dataframe)
            matrix = result_dataframe.values
            labels = self._gmeans_base(matrix)
            result_dataframe['Cluster'] = labels
            return AnalysisResult(result_dataframe, base_param, target_param)

        except (AttributeError, BaseException) as e:
            print(str(e))
