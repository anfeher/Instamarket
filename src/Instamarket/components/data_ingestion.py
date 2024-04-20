import os
import urllib.request as request

from instamarket.logging import logger
from instamarket.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config:DataIngestionConfig) -> None:
        self.config = config

    def download_file(self) -> None:
        """Download files from a given URL
        """
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded with the following info:\n{headers}")
        else:
            logger.info("File already exists.")
    