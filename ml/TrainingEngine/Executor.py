from sklearn import tree
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier
import numpy as np
import pickle
from ml.TrainingEngine.Tokens import *
from ml.TrainingEngine.Tokenizer import *

class Executor:
    def __init__(self, sequence):
        self.OperationalTokenizer = Tokenizer(sequence)
        self.OperationalTokenizer.GenerateOperations()
        self.OperationalTokenizer.GenerateTerms()
        self.env = {}
        self.returnDict = {}

    def BuildHandler(self, BuildOp):
        model_type = BuildOp.actions[BuildOp.actions.index(Build())].AssociatedItem.slotterm
        self.env['model_name'] = 'classifier'
        if model_type == 'TREE':
            classifier = BaggingClassifier(n_estimators=30, random_state=0, n_jobs=-1)
        elif model_type == 'SVC':
            classifier = BaggingClassifier(base_estimator=SVC(), n_estimators=100, random_state=0, n_jobs=-1)
        elif model_type == 'KNN':
            classifier = BaggingClassifier(base_estimator=KNeighborsClassifier(), n_estimators=20, random_state=0, n_jobs=-1).fit(features, labels)
        if With() in BuildOp.actions:
            if BuildOp.actions[BuildOp.actions.index(With())].AssociatedItem.keyphrase == 'NAME':
                self.env['model_name'] = BuildOp.actions[BuildOp.actions.index(With())].AssociatedItem.slotterm
        self.env[self.env['model_name']] = classifier

    def TrainHandler(self, TrainOp):
        print(os.getcwd())
        model_title = TrainOp.actions[TrainOp.actions.index(Train())].AssociatedItem.slotterm
        """
        features filepath comes before ampersand, labels afterwards
        """
        filepaths = TrainOp.actions[TrainOp.actions.index(With())].AssociatedItem.slotterm.split("&")

        features = pickle.load(open(filepaths[0], 'rb'))
        labels = pickle.load(open(filepaths[1], 'rb'))



        score = self.env[model_title].fit(features, labels).score(features, labels)

        self.returnDict['training_score'] = score

    def TestHandler(self, TestOp):
        model_title = TestOp.actions[TestOp.actions.index(Test())].AssociatedItem.slotterm
        filepaths = TestOp.actions[TestOp.actions.index(With())].AssociatedItem.slotterm.split("&")

        X = pickle.load(open(filepaths[0], 'rb'))
        y = pickle.load(open(filepaths[1], 'rb'))

        score = self.env[model_title].score(X, y)



        self.returnDict['testing_score'] = score

    def parse(self):
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        for op in self.OperationalTokenizer.sequence.operations:
            if Build() in op.actions:
                self.BuildHandler(op)
            elif Train() in op.actions:
                self.TrainHandler(op)
            elif Test() in op.actions:
                self.TestHandler(op)
            else:
                raise Exception("oh no something went REALLY wrong")
        return self.returnDict

"""
FINAL EXAMPLE SEQUENCE:
BUILD MODEL TREE WITH NAME FIRSTMODEL,
TRAIN MODEL FIRSTMODEL WITH DATASET FlightDelayFiles/trainingSet1Features.pkl&FlightDelayFiles/trainingSet1Labels.pkl,
TEST MODEL FIRSTMODEL WITH DATASET FlightDelayFiles/testingSet1Features.pkl&FlightDelayFiles/testingSet1Labels.pkl
"""
