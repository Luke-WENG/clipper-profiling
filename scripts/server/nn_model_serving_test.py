
import sklearn
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

def dataset_load(dataset_number):
    dataset_path = '../../datasets/'
    dataset_name = ['breast-cancer.npz', 'diabetes.npz', 'digit.npz', 'iris.npz', 'wine.npz']
    
    number = dataset_number % 5
    print "dataset:   "+dataset_name[number]
    
    with np.load(dataset_path + dataset_name[number]) as data:
        [train_X, train_Y, test_X, test_Y] = [data['train_X'], data['train_Y'], data['test_X'], data['test_Y']]
    
    print "datashape: trainset:", train_X.shape, ", testset:", test_X.shape
    return [train_X, train_Y, test_X, test_Y]
    
def load_NN():
    model_path = "../../models/sklearn/" 
    model_name = "nn_model.sav"
    clf = joblib.load(model_path + model_name)
    return clf
    
def serving_test(dataset_number):
    clf = load_NN()
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    train_scores = clf.score(train_X, train_Y)
    test_scores = clf.score(test_X, test_Y)
    print "accuracy of train set =",train_scores
    print "accuracy of test  set =",test_scores
    print "type of input:", type(train_X)
    results = clf.predict(train_X)
    print "predict results of train_X:\n", results

serving_test(0)



