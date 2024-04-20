import os
import sys
import logging

from datetime import datetime

logs_dir = "logs"
logs_file_name = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
logging_str = "[%(asctime)s] %(lineno)d %(module)s - %(levelname)s - %(message)s"
logs_file_path = os.path.join(logs_dir,logs_file_name)

os.makedirs(logs_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(logs_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("instamarketLogger")