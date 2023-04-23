from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np
import random 
import collections

def fs(x):
    return np.where(x > 0 , 1, -1)

class Perceptron:
    def __init__(self, learning_rate):
        self.lr = learning_rate
        self.weights = None
        self.k = None

    def fit(self, X, y): #########CZASAMI NIE ZNAJDUJE WSPOLCZYNNIKA
        n_samp, n_features = X.shape
        E = np.zeros(n_samp)

        self.weights = np.zeros(n_features)
        self.k = 0

        y_fs = np.array(fs(y))

        while(True):
            r_idx = random.randint(0, len(X)-1)

            E = np.array(fs(np.dot(X, self.weights)))
            
            if (len(list(set(y_fs == E))) == 1) and (list(set(y_fs == E))[0] == True):
                break

            if E[r_idx] == y_fs[r_idx]:
                continue
            else:
                update = self.lr * y_fs[r_idx]
                self.weights = self.weights + (update * X[r_idx])
                self.k += 1

    def predict(self, X):
        return fs(np.dot(X,self.weights)), self.k, self.weights

    def accuracy_score(self, X_predict, y_test):
        res_list = X_predict == y_test
        return np.round((len(res_list[res_list==True])/len(res_list)) * 100)