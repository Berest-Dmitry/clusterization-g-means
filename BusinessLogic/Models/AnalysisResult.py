from pandas.core.interchange.dataframe_protocol import DataFrame

# модель результата кластеризации
class AnalysisResult:
    df: DataFrame
    base_col: str
    target_col: str

    def __init__(self, data, base_col, target_col):
        self.df = data
        self.base_col = base_col
        self.target_col = target_col