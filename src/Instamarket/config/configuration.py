from instamarket.constants import CONFIG_FILE_PATH
from instamarket.utils.common import read_yaml, create_directories

from instamarket.entity import (DataIngestionConfig, DataPreprocessingConfig)

class ConfigurationManager:
    def __init__(self) -> None:
        config_file_path = CONFIG_FILE_PATH

        self.config = read_yaml(config_file_path)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
        )

        return data_ingestion_config
    
    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        config = self.config.data_preprocessing

        create_directories([config.root_dir])

        data_preprocessing_config = DataPreprocessingConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            clean_data_file=config.clean_data_file
        )

        return data_preprocessing_config