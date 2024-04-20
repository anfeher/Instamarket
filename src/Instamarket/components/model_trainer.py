import os

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from sklearn.multioutput import MultiOutputRegressor

from instamarket.entity import ModelTrainerConfig
from instamarket.utils.common import load_object, save_object
from instamarket.logging import logger

MODELS = {
    "Linear Regression": LinearRegression(),
    "Lasso": Lasso(),
    "Ridge": Ridge(),
    "K-Neighbors Regressor": KNeighborsRegressor(),
    "Decision Tree": DecisionTreeRegressor(),
    "Random Forest Regressor": RandomForestRegressor(),
    "Gradient Boosting": GradientBoostingRegressor(),
    "XGBRegressor": XGBRegressor(), 
    "CatBoosting Regressor": CatBoostRegressor(verbose=False),
    "AdaBoost Regressor": AdaBoostRegressor()
    }

class ModelTrainer:
    def __init__(self, config:ModelTrainerConfig) -> None:
        self.config = config
    
    def train(self):
        logger.info("Loading training data")
        train_arr = load_object(os.path.join(self.config.data_path,"train.pkl"))

        logger.info("Split data - Independent & dependent variable")
        X_train,y_train = (train_arr.tocsc()[:,:-2], train_arr.tocsc()[:,-2:])
        
        logger.info(f"Model: {self.config.model}")
        model = MODELS[self.config.model]

        logger.info(f"Params: {self.config.hparams}")
        model.set_params(**self.config.hparams)
        multi_out_model = MultiOutputRegressor(model)

        logger.info("Start training model")
        multi_out_model.fit(X_train, y_train.toarray())

        logger.info("Saving model")
        save_object(os.path.join(self.config.root_dir,"model.pkl"), multi_out_model)
