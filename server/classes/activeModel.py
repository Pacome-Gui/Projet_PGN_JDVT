import numpy as np
from server.classes.quickDrawObject import QDModel, QDPrediction
from mlflow.pyfunc import load_model

class ActiveModel():
    
    def __init__(self, model_version):
        self.changeModel(model_version)
    
    def changeModel(self, model_version):
        self.model_info = QDModel.fromModelVersion(model_version)
        self.model = load_model(model_version.source)
        
    def argMaxPredict(self, image):
        results = np.array(self.model.predict(image))
        return QDPrediction.fromOutput(results[0].argmax(), results[0][results[0].argmax()])

    def predict(self, image):
        results = np.array(self.model.predict(image))
        return [QDPrediction.fromOutput(i, confidence) for i, confidence in enumerate(results[0])]