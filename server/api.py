from fastapi import FastAPI, UploadFile, File
from classes.activeModel import ActiveModel
from classes.client import QuickDrawClient
from classes.quickDrawObject import QDModel, QDPrediction
from classes.utils import API_TAGS, LABELS, fileToImageToInput

app = FastAPI(
    title = "QuickDraw Classifier API REST",
    description= "QuickDraw Classifier API REST",
    version= "0.0.1",
    openapi_tags= API_TAGS
)

CLIENT = QuickDrawClient()
ACTIVE_MODEL = ActiveModel(CLIENT.get_registered_model('VGG16_FT-96'))

@app.get("/labels/", tags = ['Settings'],
         description="Return <b>label</b> output based on <b>id</b>. \
            <br>If <b>id</b> is None, return all outputs with <b>id</b>.")
def get_class(id: int = None) -> str | dict:
    if id is None:
        return LABELS
    return LABELS.get(id)

@app.get("/models/search/all", tags = ['Models manager'],
         description= "Return all models and their versions")
def get_all_model() -> list[QDModel]:
    return list(map(QDModel.fromRegisteredModel,CLIENT.search_registered_models()))

@app.get('/models/current', tags = ['Models manager'],
         description='Return the current active model.')
def get_current_model() -> QDModel:
    return ACTIVE_MODEL.model_info

@app.post('/models/change/', tags = ['Models manager'],
          description='Change the current model to <b>name</b> and <b>version</b>.\
            <br>If <b>version</b> is None, takes latest. \
            <br>Return changed Model')
def change_model(name: str = 'VGG16_FT-96', version: str = None) -> QDModel:
    model_version = CLIENT.get_registered_model(name, version)
    if model_version is None:
        raise Exception("No model found")
    ACTIVE_MODEL.changeModel(model_version)
    print(f'Model changed to : { get_current_model().name, get_current_model().versions[0].version }')
    return get_current_model()

@app.post('/models/predict', tags = ['Predict'],
          description='Return prediction results')
def predict(data: UploadFile = File(...)) -> list[QDPrediction]:
    image = fileToImageToInput(data.file)
    predictions = ACTIVE_MODEL.predict(image)
    print(f'{ prediction.id } : "{ prediction.label }", confidence : { format(prediction.confidence, '.2f')}\n' for prediction in predictions)
    return predictions

@app.post('/models/predict/best', tags = ['Predict'],
          description='Return prediction best result')
def predict_best(data: UploadFile = File(...)) -> QDPrediction:
    image = fileToImageToInput(data.file)
    prediction = ACTIVE_MODEL.argMaxPredict(image)
    print(f'{ prediction.id } : "{ prediction.label }", confidence : { format(prediction.confidence, '.2f') }')
    return prediction