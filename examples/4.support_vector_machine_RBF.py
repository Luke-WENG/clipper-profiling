
# coding: utf-8

# In[32]:


import sklearn
import numpy as np
print "sklearn:",sklearn.__version__ # 0.19.0
print "numpy:  ",np.__version__ # 1.13.1


# In[33]:


def dataset_load(dataset_number):
    dataset_path = './datasets/'
    dataset_name = ['breast-cancer.npz', 'diabetes.npz', 'digit.npz', 'iris.npz', 'wine.npz']
    
    number = dataset_number % 5
    print "dataset:   "+dataset_name[number]
    
    with np.load(dataset_path + dataset_name[number]) as data:
        [train_X, train_Y, test_X, test_Y] = [data['train_X'], data['train_Y'], data['test_X'], data['test_Y']]
    
    print "datashape: trainset:", train_X.shape, ", testset:", test_X.shape
    return [train_X, train_Y, test_X, test_Y]
# print train_X.shape, train_Y.shape
# print test_X.shape, test_Y.shape


# In[34]:


# 4. support vector machine with RBF kernel
def exploring_SVM(dataset_number):
    best_space = 10
    best_settings=[[1, 0.0, 0.0] for _ in range(best_space)]
    # gamma, randome_state, train_scores_mean, test_scores

    from sklearn.model_selection import cross_val_score
    from sklearn.svm import SVC
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    
    for index in range(10):
        gm_list = [1, 0.6, 0.3, 0.1, 0.06, 0.03, 0.01, 0.006, 0.003, 0.001]
        gm = gm_list[index]
        clf = SVC(kernel='rbf',gamma=gm)
        train_scores = cross_val_score(clf, train_X, train_Y, cv=5)
        train_scores_mean = train_scores.mean()
        clf.fit(train_X, train_Y)
        test_scores = clf.score(test_X, test_Y)
        best_settings[index] = [gm, train_scores_mean, test_scores]

    for i in range(best_space):
        print best_settings[i]
        
        
                            
    
def best_SVM(dataset_number):
#     from sklearn.model_selection import cross_val_score
    import time
    # from sklearn.metrics import confusion_matrix
    from sklearn.svm import SVC
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    
    best_settings=[[0.1, 0.96710471939829734, 0.9779411764705882],
                   [0.1, 0.76751385467318445, 0.78431372549019607],
                   [0.01, 0.95002212000468766, 0.98499999999999999],
                   [0.01, 0.95002212000468766, 0.98499999999999999],
                   [0.001, 0.78743842364532024, 0.75]]
    
    gm = best_settings[dataset_number][0]
    clf = SVC(kernel='rbf',
              gamma=gm)
    
    print "\n-------- Start Training --------\n"
    print clf
    start = time.time()
    clf.fit(train_X, train_Y)
    period = time.time() - start
    print "\n-------- End of Training --------\n"
    train_scores = clf.score(train_X, train_Y)
    test_scores = clf.score(test_X, test_Y)
    print "Indices of support vectors:\n", clf.support_
#     print "support vectors:\n", clf.support_vectors_
    print "CPU time (ms):", 1000*period
    print "accuracy of train set =",train_scores
    print "accuracy of test  set =",test_scores

    # print confusion_matrix(test_Y, clf.predict(test_Y))
    
# exploring_SVM(0)
# exploring_SVM(1)
# exploring_SVM(2)
# exploring_SVM(3)
# exploring_SVM(4)
best_SVM(0)
best_SVM(1)
best_SVM(2)
best_SVM(3)
best_SVM(4)
    


