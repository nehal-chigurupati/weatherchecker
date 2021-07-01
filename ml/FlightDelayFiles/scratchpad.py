import pickle
import numpy
import os

training = pickle.load(open('trainingSet1Features.pkl', 'rb'))
testing = pickle.load(open('trainingSet1Labels.pkl', 'rb'))
print(len(training))
print(len(testing))

print(training)
print(testing)
