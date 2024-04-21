import pandas as pd

from instamarket.utils.common import load_object
from instamarket.config.configuration import ConfigurationManager
from instamarket.logging import logger

import warnings
warnings.filterwarnings('ignore')

class PredictionPipeline:
    def __init__(self) -> None:
        self.config = ConfigurationManager().config

    @staticmethod
    def features_preparation(store, optimal_start_time, optimal_end_time):
        columns = ["store_id", "optimal_start_time_picking", "optimal_end_time_picking"]
        data = [[store, optimal_start_time, optimal_end_time]]
        
        df = pd.DataFrame(data, columns=columns)
        datetime_cols = ["optimal_start_time_picking",
                         "optimal_end_time_picking"]
        df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime, format="mixed")

        df_prepared = df[["store_id"]]
        df_prepared["optimal_total_time"] = (df["optimal_end_time_picking"] - df["optimal_start_time_picking"]).dt.total_seconds() / 60.0

        df_prepared['optimal_start_day'] = df['optimal_start_time_picking'].dt.day
        df_prepared['optimal_start_hour'] = df['optimal_start_time_picking'].dt.hour
        df_prepared['optimal_start_minute'] = df['optimal_start_time_picking'].dt.minute
        df_prepared['optimal_start_weekday'] = df['optimal_start_time_picking'].dt.weekday
        df_prepared['optimal_start_is_weekend'] = df_prepared['optimal_start_weekday'].isin([5, 6])

        df_prepared['optimal_end_day'] = df['optimal_end_time_picking'].dt.day
        df_prepared['optimal_end_hour'] = df['optimal_end_time_picking'].dt.hour
        df_prepared['optimal_end_minute'] = df['optimal_end_time_picking'].dt.minute
        df_prepared['optimal_end_weekday'] = df['optimal_end_time_picking'].dt.weekday
        df_prepared['optimal_end_is_weekend'] = df_prepared['optimal_end_weekday'].isin([5, 6])

        return df_prepared

    def predict(self,store, optimal_start_time, optimal_end_time):
        try:
            logger.info("Loading model & features preprocessor")
            model = load_object(self.config.model_evaluation.model_path)
            preprocessor = load_object(self.config.data_transformation.preprocessor_file)

            features = self.features_preparation(store, optimal_start_time, optimal_end_time)

            data_scaled = preprocessor.fit_transform(features)
            preds = model.predict(data_scaled)

            return preds
        
        except Exception as e:
            raise e