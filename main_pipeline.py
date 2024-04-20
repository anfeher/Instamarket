from instamarket.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from instamarket.pipeline.stage_02_data_preprocessing import DataPreprocessingTrainingPipeline
from instamarket.pipeline.stage_03_data_preparation import DataPreparationTrainingPipeline
from instamarket.logging import logger

STAGE_NAME = "Data Ingestion stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = DataIngestionTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME = "Data Preprocessing stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_preprocessing = DataPreprocessingTrainingPipeline()
   data_preprocessing.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e

STAGE_NAME = "Data Preparation stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_preparation = DataPreparationTrainingPipeline()
   data_preparation.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        logger.exception(e)
        raise e