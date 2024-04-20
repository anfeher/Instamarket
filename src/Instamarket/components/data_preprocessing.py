import pandas as pd
import numpy as np

from instamarket.entity import DataPreprocessingConfig
from instamarket.logging import logger

class DataPreprocessing:
    def __init__(self, config:DataPreprocessingConfig) -> None:
        self.config = config

    def start(self) -> pd.DataFrame:
        logger.info("Read the dataset as dataframe")
        df = pd.read_csv(self.config.data_path)

        logger.info("Converting picking times to datetime DType")
        datetime_cols = ["actual_start_time_picking",
                        "actual_end_time_picking",
                        "optimal_start_time_picking",
                        "optimal_end_time_picking"]
        df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime, format="mixed")
        
        df.drop(columns="job_id", axis=1, inplace=True)

        logger.info("Removing missing values")
        df.dropna(subset=['actual_start_time_picking', 'actual_end_time_picking'], inplace=True)

        logger.info("Adding columns for analysis") 
        df["actual_total_time"] = (df["actual_end_time_picking"] - df["actual_start_time_picking"]).dt.total_seconds() / 60.0
        df["optimal_total_time"] = (df["optimal_end_time_picking"] - df["optimal_start_time_picking"]).dt.total_seconds() / 60.0
        df["diff_actual_optimal_time"] = df["actual_total_time"] - df["optimal_total_time"]

        df["start_delay"] = (df["actual_start_time_picking"] - df["optimal_start_time_picking"]).dt.total_seconds() / 60.0
        df["end_delay"] = (df["actual_end_time_picking"] - df["optimal_end_time_picking"]).dt.total_seconds() / 60.0

        df["PTP"] = df["actual_total_time"]/df["optimal_total_time"]

        logger.info("Removing outliers") 
        cols_to_normalize = ["actual_total_time",
                              "optimal_total_time",
                              "diff_actual_optimal_time",
                              "start_delay",
                              "end_delay",
                              "PTP"]

        for col in cols_to_normalize:
            col_zscore = col + '_zscore'
            df[col_zscore] = (df[col] - df[col].mean())/df[col].std(ddof=0)
        
        zcore_cols  =  [col+ '_zscore' for col in cols_to_normalize]
        filters = [(df[col]>-3) & (df[col]<3) for col in zcore_cols]

        df_clean = df[np.logical_and.reduce(filters)]
        df_clean.to_csv(self.config.clean_data_file, index=False, header=True)
        logger.info("Preprocessing data saved") 