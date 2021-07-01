import requests
sequence = "BUILD MODEL TREE WITH NAME FIRSTMODEL, TRAIN MODEL FIRSTMODEL WITH DATASET weatherchecker/ml/FlightDelayFiles/trainingSet1Features.pkl&weatherchecker/ml/FlightDelayFiles/trainingSet1Labels.pkl, TEST MODEL FIRSTMODEL WITH DATASET weatherchecker/ml/FlightDelayFiles/testingSet1Features.pkl&weatherchecker/ml/FlightDelayFiles/testingSet1Labels.pkl"
params={'sequence': sequence}

data = requests.get('http://127.0.0.1:8000/nehal/ml/engine', params=params)
print(data.json())
