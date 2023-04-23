import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, ClassifierMixin
from NBC import NBC 
import pandas as pd

X = np.array(pd.read_csv("wine.data"))
y = X[:,0]
X = X[:,1:]

est = KBinsDiscretizer(n_bins = 3, encode='ordinal', strategy='uniform').fit(X)
X = est.transform(X)
with_laplace = []
without_laplace = []

for i in range(100):

    X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=0.33)
    nbc = NBC()
    nbc.fit(X_train,y_train, LaPlace=False)
    X_predict = nbc.predict(X_test)
    prediction_prob = nbc.predict_proba(X_test)
    with_laplace.append(nbc.accuracy_score(X_predict, y_test))

    nbc = NBC()
    nbc.fit(X_train,y_train, LaPlace=True)
    y_predict = nbc.predict(X_test)
    prediction_prob = nbc.predict_proba(X_test)
    nbc.accuracy_score(y_predict, y_test)
    without_laplace.append(nbc.accuracy_score(y_predict, y_test))
    
print("Bez poprawki LaPlace'a: ", np.mean(without_laplace))
print("Z poprawką LaPlace'a: ", np.mean(with_laplace))

# X = np.array(pd.read_csv("balance-scale.data"))
# y = X[:,0]
# X = X[:,1:]
# est = KBinsDiscretizer(n_bins = 5, encode='ordinal', strategy='uniform').fit(X)
# X = est.transform(X)
# with_laplace = []
# without_laplace = []

# for i in range(1):

#     X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=0.33)
#     nbc = NBC()
#     nbc.fit(X_train,y_train, LaPlace=False)
#     X_predict = nbc.predict(X_test)
#     prediction_prob = nbc.predict_proba(X_test)
#     with_laplace.append(nbc.accuracy_score(X_predict, y_test))

#     nbc = NBC()
#     nbc.fit(X_train,y_train, LaPlace=True)
#     X_predict = nbc.predict(X_test)
#     prediction_prob = nbc.predict_proba(X_test)
#     nbc.accuracy_score(X_predict, y_test)
#     without_laplace.append(nbc.accuracy_score(X_predict, y_test))
    
# print("Bez poprawki LaPlace'a: ", np.mean(without_laplace))
# print("Z poprawką LaPlace'a: ", np.mean(with_laplace))

