import os
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from instamarket.entity import ModelEvaluationConfig
from instamarket.utils.common import load_object
from instamarket.logging import logger

class ModelEvaluation:
    def __init__(self, config:ModelEvaluationConfig) -> None:
        self.config = config

    @staticmethod
    def eval_metrics(actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def evaluate(self):
        logger.info("Loading test data")
        test_arr = load_object(os.path.join(self.config.data_path,"test.pkl"))

        logger.info("Split data in Independent & dependent variable")
        X_test,y_test = (test_arr.tocsc()[:,:-2], test_arr.tocsc()[:,-2:])

        logger.info("Loading model")
        model = load_object(self.config.model_path)

        logger.info("Start model evaluation")
        preds = model.predict(X_test)
        
        start_metrics = self.eval_metrics(y_test.toarray()[:, 0], preds[:, 0])
        logger.info("start_delay")
        logger.info(f"rmse: {start_metrics[0]}, mae: {start_metrics[0]}, r2: {start_metrics[1]}")

        end_metrics = self.eval_metrics(y_test.toarray()[:, 1], preds[:, 1])
        logger.info("end_delay")
        logger.info(f"rmse: {end_metrics[0]}, mae: {end_metrics[0]}, r2: {end_metrics[1]}")
        
