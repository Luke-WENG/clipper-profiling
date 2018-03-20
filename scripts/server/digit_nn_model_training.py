
import sklearn
import numpy as np
print "sklearn:",sklearn.__version__ # 0.19.0
print "numpy:  ",np.__version__ # 1.13.1

def dataset_load(dataset_number):
    dataset_path = '../../datasets/'
    dataset_name = ['breast-cancer.npz', 'diabetes.npz', 'digit.npz', 'iris.npz', 'wine.npz']
    
    number = dataset_number % 5
    print "dataset:   "+dataset_name[number]
    
    with np.load(dataset_path + dataset_name[number]) as data:
        [train_X, train_Y, test_X, test_Y] = [data['train_X'], data['train_Y'], data['test_X'], data['test_Y']]
    
    print "datashape: trainset:", train_X.shape, ", testset:", test_X.shape
    return [train_X, train_Y, test_X, test_Y]

def best_NN(dataset_number):
#     from sklearn.model_selection import cross_val_score
    import time
    from sklearn.neural_network import MLPClassifier
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)

    clf = MLPClassifier(solver='sgd', # default: 'lbfgs'
                        learning_rate='adaptive', # default: 'constant'
                        learning_rate_init=0.001, # default: 1e-3
                        hidden_layer_sizes=(1000,1000,1000,1000,1000,1000,1000,1000,1000,1000),
                        activation='relu', # default: 'relu'
                        max_iter=1000, # default: 200
                        tol=1e-4, # default: 1e-4                        
                        random_state=1,
                        alpha=1e-5,
                        verbose=0)
    
    print "\n-------- Start Training --------\n"
    print clf
    start = time.time()
    clf.fit(train_X, train_Y)
    period = time.time() - start
    print "\n-------- End of Training --------\n"
    train_scores = clf.score(train_X, train_Y)
    test_scores = clf.score(test_X, test_Y)
    # print "coefficents: shape:",[coef.shape for coef in clf.coefs_]            ,'\nlayer1:', clf.coefs_[0], '\nlayer2:', clf.coefs_[1]
    print "# of iterations =",clf.n_iter_
    print "accuracy of train set =",train_scores
    print "accuracy of test  set =",test_scores
    print "CPU time (sec):", period/1000000

    
    # Store the model for later usage
    from sklearn.externals import joblib
    model_path = "../../models/sklearn/" 
    model_name = "dig_nn_model.sav"
    joblib.dump(clf, model_path + model_name)

    # clf = joblib.load(model_path + model_name)
    # print clf.score(test_X, test_Y)


    
# exploring_NN(0)
# exploring_NN(1)
# exploring_NN(2)
# exploring_NN(3)
# exploring_NN(4)
# best_NN(0)
# best_NN(1)
best_NN(2)
# best_NN(3)
# best_NN(4)
    



