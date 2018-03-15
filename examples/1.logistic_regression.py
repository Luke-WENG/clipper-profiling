
# coding: utf-8

# In[13]:


import sklearn
import numpy as np
print "sklearn:",sklearn.__version__ # 0.19.0
print "numpy:  ",np.__version__ # 1.13.1


# In[14]:


def dataset_load(dataset_number):
    dataset_path = './datasets/'
    dataset_name = ['breast-cancer.npz', 'diabetes.npz', 'digit.npz', 'iris.npz', 'wine.npz']
    
    number = dataset_number % 5
    print "dataset: "+dataset_name[number]
    
    with np.load(dataset_path + dataset_name[number]) as data:
        [train_X, train_Y, test_X, test_Y] = [data['train_X'], data['train_Y'], data['test_X'], data['test_Y']]
    return [train_X, train_Y, test_X, test_Y]

# print train_X.shape, train_Y.shape
# print test_X.shape, test_Y.shape


# In[17]:


import matplotlib.pyplot as plt
import itertools
def plot_confusion_matrix(cm, classes=["class0", "class1"],
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# In[19]:


# 1. logistic regression
def exploring_LR(dataset_number): # dataset_number: 0,1,2,3,4
    from sklearn.linear_model import SGDClassifier
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    
    best_space = 3*10
    best_settings=[['constant', 0.1, 0.1, 1, 0, 0.0, 0.0] for _ in range(best_space)] 
    # learning_rate, eta0, power_t, randome_state, iterations, train_accuracy, test_accuracy
    index = 0
    for lr in ['constant','invscaling','optimal']:
        # print "lr =", lr
        for eta in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            # print "\teta =", eta
            for rs in range(1, 101): # random_state
                if lr == 'invascaling':
                    pt = rs % 0.9 + 0.1 # 0.1, 0.1, 0.2, ..., 0.9, 1.0
                else:
                    pt = 0.5 # default value
                clf = SGDClassifier(loss="log", # default: hinge (linear SVM)
                                    eta0=eta, # default: 0.0
                                    learning_rate=lr, # default: 'optimal'
                                    power_t=pt, # default: 0.5
                                    penalty="l2", # default: l2
                                    max_iter=100, # default: 5
                                    random_state=rs, # default: None
                                    tol=1e-3, # default: None
                                    verbose=1) # default: 0

                clf.fit(train_X, train_Y)
                train_score = clf.score(train_X, train_Y)

                if train_score > best_settings[index][-2]: # the best in single setting
                    test_score = clf.score(test_X, test_Y)
                    best_settings[index]=[lr, eta, pt, rs, clf.n_iter_, train_score, test_score]
            index = index + 1

    for i in range(best_space):
        print best_settings[i]

def best_LR(dataset_number): # dataset_number: 0,1,2,3,4
    from sklearn.linear_model import SGDClassifier
    import time
    [train_X, train_Y, test_X, test_Y] = dataset_load(dataset_number)
    
    best_settings=[['constant', 0.8, 0.5, 96, 3, 0.9780621572212066, 0.97058823529411764],
                   ['constant', 0.6, 0.5, 65, 4, 0.79024390243902443, 0.78431372549019607],
                   ['invscaling', 0.9, 0.5, 72, 10, 0.92500000000000004, 0.91500000000000004],
                   ['constant', 0.4, 0.5, 1, 3, 1.0, 1.0],
                   ['optimal', 0.1, 0.5, 100, 11, 0.79577464788732399, 0.63888888888888884]]
    
    [lr, eta, pt, rs] = best_settings[dataset_number % 5][0:4]
    clf = SGDClassifier(loss="log", # default: hinge (linear SVM)
                        eta0=eta, # default: 0.0
                        learning_rate=lr, # default: 'optimal'
                        power_t=pt, # default: 0.5
                        penalty="l2", # default: l2
                        max_iter=100, # default: 5
                        random_state=rs, # default: None
                        tol=1e-3, # default: None
                        verbose=1) # default: 0
    print clf
    print "\n-------- Start Training --------\n"
    start = time.time()
    clf.fit(train_X, train_Y)
    period = time.time() - start
    print "\n-------- End of Training --------\n"
    print "coefficents =\n",clf.coef_
    print "# of iterations =",clf.n_iter_
    print "accuracy of train set =",clf.score(train_X, train_Y)
    print "accuracy of test  set =",clf.score(test_X, test_Y)
    print "CPU time (ms):", 1000*period
    
    y_pred_train = clf.predict(train_X)
    y_pred_test  = clf.predict(test_X)
    train_loss = sklearn.metrics.log_loss(train_Y, y_pred_train)
    test_loss = sklearn.metrics.log_loss(test_Y, y_pred_test)
    print "loss of train set=", train_loss
    print "loss of test  set=", test_loss
    train_conf_matrix = sklearn.metrics.confusion_matrix(train_Y, y_pred_train)
    test_conf_matrix  = sklearn.metrics.confusion_matrix(test_Y, y_pred_test)
    plt.figure()
    plot_confusion_matrix(train_conf_matrix, title='Confusion matrix of training data' )
    plt.figure()
    plot_confusion_matrix(test_conf_matrix, title='Confusion matrix of testing data')
    print "\n===================================================================="
    print "====================================================================\n"

# exploring_LR(0) # 0,1,2,3,4
# exploring_LR(1)
# exploring_LR(2)
# exploring_LR(3)
# exploring_LR(4)
best_LR(0) # 0,1,2,3,4
best_LR(1)
best_LR(2)
best_LR(3)
best_LR(4)

