import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, ClassifierMixin
import collections

class NBC(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass

    def fit(self, X, y):
        self.y = y
        self._mean = self.mean(X, y)
        self._std = self.std(X, y)

    def accuracy_score(self, X_predict, y_test):
        res_list = X_predict == y_test
        return np.round((len(res_list[res_list==True])/len(res_list)) * 100)

    def predict(self, X_test):
        res = []
        _dens = self.density(X_test,self.y)
        for el in _dens:
            vals = []
            for val in el:
                vals.append(val)
            res.append(vals.index(max(vals)) + 1)
        return res

    def density(self, X, y):
        res = []
        for attri_idx in range(len(X[:,0])):
            p = [1,1,1]
            for idx, el in enumerate(X[attri_idx,:]):
                for classi in set(y):
                    p[int(classi) - 1] *= (1/(self._std[idx][int(classi) -1] * np.sqrt(2*np.pi))) * np.exp(-((el-self._mean[idx][int(classi) -1])**2)/(2*(self._std[idx][int(classi) -1]**2)))
            res.append(p)
                
        return res
        
    def std(self, X, y):
        final = []
        for attri_idx in range(len(X[0])):
            res = []
            for classi in set(y):
                sum = 0
                for idx, el in enumerate(X[:,attri_idx]):
                    if y[idx] == classi:
                        sum += (el - self._mean[attri_idx][int(classi) - 1])**2
                sum = np.sqrt(sum/(len(X[:,attri_idx])-1))
                res.append(sum)
            final.append(res)
        return final

    def mean(self, X, y):
        final = []
        for attri_idx in range(len(X[0])):
            res = []
            for classi in set(y):
                sum = 0
                for idx, el in enumerate(X[:,attri_idx]):
                    if y[idx] == classi:
                        sum += el
                sum = sum/len(X[:,attri_idx])
                res.append(sum) ## MOZNA DODAC KLASYFIAKTOR(1,2,3)D
            final.append(res)
        return final