from PIL import Image
import numpy as np

LABELS = { 
    0 : "basket",
    1 : "eye",
    2 : "binoculars",
    3 : "rabbit",
    4 : "hand"
}

API_TAGS = [
    {
        'name': 'Models manager',
        'description': 'Manage your models'
    },
    {
        'name': 'Predict',
        'description': 'Get a prediction from the current model'
    },
    {
        'name': 'Settings',
        'description': 'See settings'
    },
]

def fileToImageToInput(file):
    image = Image.open(file).convert('RGB')
    image = image.resize((32, 32))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)