from pydantic import BaseModel
from mlflow.entities.model_registry import RegisteredModel, ModelVersion
from classes.utils import LABELS

class QDModelVersion(BaseModel):
    version: str = '0'
    source_link: str = 'no link'
    status: str = 'UNAVAILABLE'
    
    @staticmethod
    def fromModelVersion(modelVersion: ModelVersion):
        this = QDModelVersion()
        this.version = modelVersion.version
        this.source_link = modelVersion.source
        this.status = modelVersion.status
        return this

class QDModel(BaseModel):
    name: str = 'Unknown name'
    description: str = 'No description'
    versions: list[QDModelVersion] = []
    
    @staticmethod
    def fromRegisteredModel(registeredModel: RegisteredModel):
        this = QDModel()
        this.name = registeredModel.name
        this.description = registeredModel.description
        this.versions = list(map(QDModelVersion.fromModelVersion, registeredModel.latest_versions))
        return this
    
    @staticmethod
    def fromModelVersion(modelVersion: ModelVersion):
        this = QDModel()
        this.name = modelVersion.name
        this.description = modelVersion.description
        this.versions = [QDModelVersion.fromModelVersion(modelVersion)]
        return this

class QDPrediction(BaseModel):
    label: str = 'Unknown'
    id: int = -1
    confidence: float = 0.
    
    @staticmethod
    def fromOutput(id, confidence):
        this = QDPrediction()
        this.id = int(id)
        this.label = LABELS.get(this.id)
        this.confidence = round(float(confidence), 4)
        return this