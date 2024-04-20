from instamarket.config.configuration import ConfigurationManager
from instamarket.components.data_preparation import DataPreparation

class DataPreparationTrainingPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self):
        config = ConfigurationManager()
        data_preparation_config = config.get_data_preparation_config()
        data_preparation = DataPreparation(config=data_preparation_config)
        data_preparation.split_data()