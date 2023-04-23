from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np
import random
from Perceptron import Perceptron
from sklearn.model_selection import train_test_split

n_s = []
k_s = []

for i in range(10):
    n = 0.1 * ((i)+1) - 0.01
    m = 20

    # X, y = datasets.make_blobs(n_samples=m, centers=2, n_features=2, center_box=(80,100))
    separable = False
    while not separable:
        samples = datasets.make_classification(n_samples=m, n_features=2, n_redundant=0, n_informative=1, n_clusters_per_class=1, flip_y=-1)
        red = samples[0][samples[1] == 0]
        blue = samples[0][samples[1] == 1]
        separable = any([red[:, k].max() < blue[:, k].min() or red[:, k].min() > blue[:, k].max() for k in range(2)])

    # plt.plot(red[:, 0], red[:, 1], 'r.')
    # plt.plot(blue[:, 0], blue[:, 1], 'b.')
    # plt.show()

    X = samples[0]
    y = samples[1]

    X = np.column_stack((np.ones(len(X)), X))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    
    # plt.plot(X_train[:, 1][y_train==0], X_train[:,2][y_train==0], 'g^')
    # plt.plot(X_train[:,1][y_train==1], X_train[:,2][y_train==1], 'bs')
    # plt.show()
    
    p1 = Perceptron(n)
    p1.fit(X_train, y_train)

    predicted, k, weights = np.array(p1.predict(X_test))

    predicted[predicted == -1] = 0

    print("Accuracy: ", int(p1.accuracy_score(predicted, y_test)), "%")
    print("Iters: ", k)
    print("Weights: ", weights,"\n")

    n_s.append(n)
    k_s.append(k)
plt.plot(n_s, k_s)
plt.savefig("nk.jpg", format='jpg')
plt.show()



m_s = []
k_s = []

for i in range(10):
    n = 0.01
    m = 20 * (i + 1)

    # X, y = datasets.make_blobs(n_samples=m, centers=2, n_features=2, center_box=(80,100))
    separable = False
    while not separable:
        samples = datasets.make_classification(n_samples=m, n_features=2, n_redundant=0, n_informative=1, n_clusters_per_class=1, flip_y=-1)
        red = samples[0][samples[1] == 0]
        blue = samples[0][samples[1] == 1]
        separable = any([red[:, k].max() < blue[:, k].min() or red[:, k].min() > blue[:, k].max() for k in range(2)])

    # plt.plot(red[:, 0], red[:, 1], 'r.')
    # plt.plot(blue[:, 0], blue[:, 1], 'b.')
    # plt.show()

    X = samples[0]
    y = samples[1]

    X = np.column_stack((np.ones(len(X)), X))

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    
    # plt.plot(X_train[:, 1][y_train==0], X_train[:,2][y_train==0], 'g^')
    # plt.plot(X_train[:,1][y_train==1], X_train[:,2][y_train==1], 'bs')
    # plt.show()
    
    p1 = Perceptron(n)
    p1.fit(X_train, y_train)

    predicted, k, weights = np.array(p1.predict(X_test))

    predicted[predicted == -1] = 0

    print("Accuracy: ", int(p1.accuracy_score(predicted, y_test)), "%")
    print("Iters: ", k)
    print("Weights: ", weights,"\n")

    m_s.append(m)
    k_s.append(k)
plt.plot(m_s, k_s)
plt.savefig("mk.jpg", format='jpg')