import math as m
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

read = pd.read_csv('autos.csv')
X = np.column_stack((read['city-mpg'], read['highway-mpg'])).astype(int)
K = 6

def distp(X,C,e):
    '''Obliczanie odległości Euklidesowej'''
    return [[np.sqrt((X[i,0] - C[C_len,0])**2+(X[i,1] - C[C_len,1])**2) for i in range(len(X))] for C_len in range(len(C))]

def distm(X,C,V):
    '''Obliczanie odległości Mahalanobis'a'''
    return [np.sqrt(((X[i] - C[i])*V**-1)*np.transpose((X[i] - C[i]))) for i in range(len(X))]

def ksrodki(X, k, C = []):
    '''Zwraca dane punktów C i indeksy punktów należących do nich'''
    if len(C) == 0:
        C = np.array([[np.random.randint(np.min(X, axis = 0)[0],np.max(X, axis = 0)[0]), np.random.randint(np.min(X, axis = 0)[1],np.max(X, axis = 0)[1])] for i in range(k)])
    dist = distp(X,C,1)
    dist = {i:[[idx, dist[i][idx]] for idx in range(len(X))] for i in range(len(C))}  #pogrupowane odległości względem k
    min_1 = [[idx, np.amin([dist[k][idx][1] for k in range(k)])] for idx in range(len(dist[0]))]  #mniejsze wartosci
    final_dist = {i:[] for i in range(k)}
    for i in range(k):
        for j in range(len(min_1)):
            if min_1[j] in dist[i]:
                final_dist[i].append(min_1[j][0]) ###[0], grupowanie wzgledem k w nowej tabeli (tylko minimalne odległości)
    rows_to_del = []
    for i in range(k):
        if len(final_dist[i]) == 0:
            del final_dist[i]
            rows_to_del.append(i)
    C = np.delete(C, rows_to_del, axis = 0)
    return C, final_dist

C, Ck = ksrodki(X, K)
K = len(C)

def get_color(c):
    '''Zwraca kolor z pyplotowej listy podstawowych kolorów (do ustalenia jednolitych kolorów w scatterze'''
    if c >= len(plt.rcParams['axes.prop_cycle']):
        c -= len(plt.rcParams['axes.prop_cycle'])
    return [plt.rcParams['axes.prop_cycle'].by_key()['color'][i] for i in range(len(plt.rcParams['axes.prop_cycle']))][c]

def avg(X, Ck, k):
    '''Przypisuje nowe wspołrzędne dla C w środku punktów Ck'''
    C_axis_x = X[Ck[k]][:,0].mean()
    C_axis_y = X[Ck[k]][:,1].mean()
    return [C_axis_x, C_axis_y]

cnt = 0
previous_C = 0

while True in np.unique(previous_C !=C):
    previous_C = C.copy()
    for idx, k in enumerate(Ck.keys()):
        x_axis = X[Ck[k]][:,0]
        y_axis = X[Ck[k]][:,1]
        plt.scatter(x_axis,y_axis, c = get_color(idx))
        plt.scatter(C[idx,0],C[idx,1], c = get_color(idx), marker = '^', linewidths = 6)
        new_C = avg(X, Ck, k)
        C[idx] = new_C
    C, Ck = ksrodki(X, K, C)
    K = len(C)
    cnt += 1
    plt.title(str(cnt)+'. iteration for k = 5')
    plt.savefig(fname = 'Plot'+ str(cnt)+'.jpg', format = 'jpg')
    plt.show()
