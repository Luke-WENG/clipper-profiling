
# coding: utf-8

# In[28]:


import sklearn
import numpy as np
print "sklearn:",sklearn.__version__ # 0.19.0
print "numpy:  ",np.__version__ # 1.13.1


# In[29]:


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


# In[30]:


# 3. support vector machine by default
def exploring_SVM(dataset_number):
    best_space = 10
    best_settings=[[0, 0.0, 0.0] for _ in range(best_space)]
    # randome_state, train_scores, test_scores

    from sklearn.svm import LinearSVC
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    
    for rs in range(0, 101):
        clf = LinearSVC(random_state=rs)
        clf.fit(train_X, train_Y)
        train_scores = clf.score(train_X, train_Y)
        
        if train_scores > best_settings[0][1]:
            test_scores = clf.score(test_X, test_Y)
            best_settings.pop(0)
            best_settings.append([rs, train_scores, test_scores])
    
    for i in range(best_space):
        print best_settings[i]
        
        
                            
    
def best_SVM(dataset_number):
#     from sklearn.model_selection import cross_val_score
    import time
    from sklearn.svm import LinearSVC
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    
    best_settings=[[0, 0.9744058500914077, 0.9705882352941176],
                   [0, 0.7642276422764228, 0.7843137254901961],
                   [25, 0.91625, 0.905],
                   [0, 1.0, 1.0],
                   [18, 0.9647887323943662, 0.8888888888888888]]
    
    rs = best_settings[dataset_number][0]
    clf = LinearSVC(random_state=rs)
    
    print "\n-------- Start Training --------\n"
    print clf
    start = time.time()
    clf.fit(train_X, train_Y)
    period = time.time() - start
    print "\n-------- End of Training --------\n"
    train_scores = clf.score(train_X, train_Y)
    test_scores = clf.score(test_X, test_Y)
    print "coefficents:\n", clf.coef_
    print "# of iterations =",clf.n_iter_
    print "accuracy of train set =",train_scores
    print "accuracy of test  set =",test_scores
    print "CPU time (ms):", 1000*period

    
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