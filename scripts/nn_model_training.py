
import sklearn
import numpy as np
print "sklearn:",sklearn.__version__ # 0.19.0
print "numpy:  ",np.__version__ # 1.13.1

def dataset_load(dataset_number):
    dataset_path = '../datasets/'
    dataset_name = ['breast-cancer.npz', 'diabetes.npz', 'digit.npz', 'iris.npz', 'wine.npz']
    
    number = dataset_number % 5
    print "dataset:   "+dataset_name[number]
    
    with np.load(dataset_path + dataset_name[number]) as data:
        [train_X, train_Y, test_X, test_Y] = [data['train_X'], data['train_Y'], data['test_X'], data['test_Y']]
    
    print "datashape: trainset:", train_X.shape, ", testset:", test_X.shape
    return [train_X, train_Y, test_X, test_Y]

# 2. Neural Network
def exploring_NN(dataset_number):
    best_space = 2*5*10
    best_settings=[['constant', 0.1, 1, 5, 0, 0.0, 0.0] for _ in range(best_space)] 
    index = 0
    # learning_rate, eta0, randome_state, H, iterations, mean_train_scores, test_scores
    
    from sklearn.model_selection import cross_val_score
    from sklearn.neural_network import MLPClassifier
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    

    for lr in ['constant', 'adaptive']:
        # print "lr =", lr
        for eta in [1e-3, 3e-3, 1e-2, 3e-2, 1e-1]:
            # print "eta =", eta
            for H in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                # print "H =", H
                for rs in range(1, 11): # test 100 times
                    clf = MLPClassifier(solver='sgd', # default: 'lbfgs'
                                        learning_rate=lr, # default: 'constant'
                                        learning_rate_init=1e-3, # default: 1e-3
                                        hidden_layer_sizes=(H),
                                        activation='relu', # default: 'relu'
                                        max_iter=500, # default: 200
                                        tol=1e-4, # default: 1e-4                        
                                        random_state=rs,
                                        alpha=1e-5,
                                        verbose=0)
                    
                    train_scores = cross_val_score(clf, train_X, train_Y, cv=5)
                    train_scores_mean = train_scores.mean()
                    
                    if train_scores_mean > best_settings[index][-2]: # the best in single setting
                        clf.fit(train_X, train_Y)
                        test_score = clf.score(test_X, test_Y)
                        best_settings[index]=[lr, eta, rs, H, clf.n_iter_, train_scores_mean, test_score]
                index = index + 1

    for i in range(best_space):
        print best_settings[i]
    
def best_NN(dataset_number):
#     from sklearn.model_selection import cross_val_score
    import time
    from sklearn.neural_network import MLPClassifier
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    
    best_settings=[['constant', 0.01, 1, 7, 400, 0.96353417637821315, 0.96323529411764708],
                   ['adaptive', 0.001, 1, 8, 415, 0.76422162317868536, 0.77124183006535951],
                   ['constant', 0.003, 1, 8, 339, 0.94377153404429848, 0.97499999999999998],
                   ['constant', 0.001, 1, 7, 500, 1.0, 1.0],
                   ['constant', 0.1, 1, 2, 5, 0.59876847290640389, 0.61111111111111116]]
    [lr, eta, rs, H] = best_settings[dataset_number % 5][:4]
    clf = MLPClassifier(solver='sgd', # default: 'lbfgs'
                        learning_rate=lr, # default: 'constant'
                        learning_rate_init=eta, # default: 1e-3
                        hidden_layer_sizes=(H),
                        activation='relu', # default: 'relu'
                        max_iter=1000, # default: 200
                        tol=1e-4, # default: 1e-4                        
                        random_state=rs,
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
    print "CPU time (ms):", 1000*period

    
    # Store the model for later usage
    from sklearn.externals import joblib
    model_path = "../models/sklearn/" 
    model_name = "nn_model.sav"
    joblib.dump(clf, model_path + model_name)

    # clf = joblib.load(model_path + model_name)
    # print clf.score(test_X, test_Y)


    
# exploring_NN(0)
# exploring_NN(1)
# exploring_NN(2)
# exploring_NN(3)
# exploring_NN(4)
best_NN(0)
# best_NN(1)
# best_NN(2)
# best_NN(3)
# best_NN(4)
    



