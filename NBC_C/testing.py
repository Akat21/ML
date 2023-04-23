import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from NBC import NBC 
import pandas as pd

X = np.array(pd.read_csv("wine.data"))
y = X[:,0]
X = X[:,1:]

accs = []
sklearn_accs = []

for i in range(100):

    X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=0.33)

    nbc_1 = GaussianNB()
    nbc_1.fit(X_train, y_train)
    y_predict = nbc_1.predict(X_test)
    sklearn_accs.append(accuracy_score(y_predict, y_test)*100)

    nbc = NBC()
    nbc.fit(X_train, y_train)
    y_predict = nbc.predict(X_test)
    acc = nbc.accuracy_score(y_predict, y_test)
    accs.append(nbc.accuracy_score(y_predict, y_test))
    
print("My Accuracy:", np.mean(accs))
print("Sklearn Accuracy:", np.mean(sklearn_accs))