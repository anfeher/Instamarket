from instamarket.config.configuration import ConfigurationManager
from instamarket.components.model_evaluation import ModelEvaluation

class ModelEvaluationPipeline:
    def __init__(self) -> None:
        pass
    
    def main(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.evaluate()