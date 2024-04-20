import os
import pandas as pd

from sklearn.model_selection import train_test_split

from instamarket.entity import DataPreparationConfig
from instamarket.logging import logger

import warnings
warnings.filterwarnings('ignore')

class DataPreparation:
    def __init__(self, config:DataPreparationConfig) -> None:
        self.config = config

    def prepare_data(self) -> pd.DataFrame:
        logger.info("Read the dataset as dataframe")
        df = pd.read_csv(self.config.data_path)

        logger.info("Converting picking times to datetime DType")
        datetime_cols = ["optimal_start_time_picking",
                         "optimal_end_time_picking"]
        df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime, format="mixed")

        df_prepared = df[["store_id","optimal_total_time","start_delay","end_delay"]]

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

    def split_data(self):
        df = self.prepare_data()

        logger.info("Train Test split initiated")
        train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

        train_set.to_csv(os.path.join(self.config.root_dir,"train.csv"), index=False, header=True)
        test_set.to_csv(os.path.join(self.config.root_dir,"test.csv"), index=False, header=True)
        logger.info("Train Test split saved")