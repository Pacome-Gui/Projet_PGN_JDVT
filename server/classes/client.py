import mlflow
import os

TRACKING_URI = "https://mlflow-ynov-jade-aba876011611.herokuapp.com/"
AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"

class QuickDrawClient(mlflow.MlflowClient):
    
    def __init__(self):
        os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
        os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
        super().__init__(TRACKING_URI, None)
        
    def get_registered_model(self, name: str, version: str = None):
        if name is None:
            return None
        model = super().get_registered_model(name)
        if model is None:
            return None
        
        if version is None:
            return model.latest_versions[0]
        return next((x for x in model.latest_versions if x.version == version), model.latest_versions[0])