import os
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.sparse import hstack
from pathlib import Path

from instamarket.entity import DataTransformationConfig
from instamarket.utils.common import save_object
from instamarket.logging import logger

class DataTransformation:
    def __init__(self, config:DataTransformationConfig) -> None:
        self.config = config

    def get_data_transformer_obj(self):
        """
        This function is responsible for data transformation 

        """
        numerical_columns = ["optimal_total_time"]
        categorical_columns = [
            "store_id",
            "optimal_start_day", "optimal_start_hour", "optimal_start_minute", "optimal_start_weekday",
            "optimal_end_day", "optimal_end_hour", "optimal_end_minute", "optimal_end_weekday"
            ]

        num_pipeline = Pipeline(
            steps=[
                ("scaler",StandardScaler())
            ]
        )
        logger.info("Numerical columns standard scaling completed")

        cat_pipeline = Pipeline(
            steps=[
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
            ]
        )
        logger.info("Categorical columns encoding completed")

        preprocessor = ColumnTransformer(
            [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns)
            ]
        )

        logger.info("Save preprocessing object")
        save_object(file_path=Path(self.config.preprocessor_file), obj=preprocessor)

        return preprocessor


    def initiate_data_transformation(self, preprocessing_obj, target_column_name):
        logger.info("Read train & test data as dataframe")
        train_df = pd.read_csv(os.path.join(self.config.data_path,"train.csv"))
        test_df = pd.read_csv(os.path.join(self.config.data_path,"test.csv"))

        input_feature_train_df = train_df.drop(columns=target_column_name,axis=1)
        target_feature_train_df = train_df[target_column_name]

        input_feature_test_df = test_df.drop(columns=target_column_name,axis=1)
        target_feature_test_df = test_df[target_column_name]

        logger.info("Applying preprocessing object on training and testing dataframes")
        input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
        input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)

        train_arr = hstack([input_feature_train_arr,np.array(target_feature_train_df)])
        test_arr = hstack([input_feature_test_arr,np.array(target_feature_test_df)])

        save_object(os.path.join(self.config.root_dir,"train.pkl"), train_arr)
        save_object(os.path.join(self.config.root_dir,"test.pkl"), test_arr)

    def convert(self):
        preprocessing_obj = self.get_data_transformer_obj()
        self.initiate_data_transformation(preprocessing_obj, ["start_delay", "end_delay"])
        logger.info("Transformed dataset saved")