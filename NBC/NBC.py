import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, ClassifierMixin
import collections

class NBC(BaseEstimator, ClassifierMixin):
    def __init__(self):
        pass

    def fit(self, X, y, LaPlace = False):
        '''First element = type, Second element = occurances, Third elemnt = probability'''
        self.P_Y = self.Single_Prob(y, LaPlace)
        self.P_X_Y = self.Condi_Prob(X, y, LaPlace)

    def accuracy_score(self, X_predict, y_test):
        res_list = X_predict == y_test
        return np.round((len(res_list[res_list==True])/len(res_list)) * 100)

    def predict(self, P_X):
        res = []
        cnt = 0
        temp = np.array(self.P_Y)[:,0]
        for el in P_X:
            P = []
            for idx, classi_num in enumerate(temp):
                prob = 1
                for col in self.P_X_Y:
                    for classi in col:
                        if classi[0][0] == classi_num:
                            for est in classi:
                                if est[1] == el[cnt]:
                                    prob *= est[2]
                                    cnt += 1 
                                    break
                            break
                cnt = 0       
                prob *= self.P_Y[idx][2]
                P.append(prob)
            res.append(self.P_Y[P.index(max(P))][0])
        return res
    
    def predict_proba(self, P_X):
        res = []
        cnt = 0
        temp = np.array(self.P_Y)[:,0]
        for el in P_X:
            P = []
            for idx, classi_num in enumerate(temp):
                prob = 1
                for col in self.P_X_Y:
                    for classi in col:
                        if classi[0][0] == classi_num:
                            for est in classi:
                                if str(est[1]) == str(el[cnt]):
                                    prob *= est[2].astype(np.float64)
                                    cnt += 1 
                                    break
                            break
                cnt = 0       
                prob *= self.P_Y[idx][2]
                P.append(prob)
            res.append(P)

        final_res = []
        for i in range(len(res)):
            temp_res = []
            for j in range(len(res[i])):
                temp_res.append(res[i][j] / (sum(res[i])))
            final_res.append(temp_res)
        return final_res

    def Single_Prob(self, y, LaPlace):
        P_cnt = collections.Counter(y)
        x = list(dict(P_cnt).keys())
        P = []
        for el in x:
            if LaPlace == True:
                P.append([el, dict(P_cnt)[el], (dict(P_cnt)[el] + 1)/(sum(P_cnt.values()) + len(x))])
            elif LaPlace == False:
                P.append([el, dict(P_cnt)[el], dict(P_cnt)[el]/sum(P_cnt.values())]) 
        return P

    def Condi_Prob(self, X, y, LaPlace):
        '''Returns probability (first dimension is first column etc)'''
        P_semifinal = []
        P_final = []
        P_Y = self.Single_Prob(y, LaPlace)

        for col_num in range(len(X[0])):
            P_semifinal = []
            for y_el_num in range(len(P_Y)):
                P = []
                P_X = []
                
                ##Liczymy prawdopodobienstwo wystąpienia estymowanej wartosci X dla kolumny w kazdym estymatorze y(są 3 - 1,2,3)
                for idx, est in enumerate(y):
                    if est == P_Y[y_el_num][0]:
                        P_X.append(X[idx, col_num])
                P_X = self.Single_Prob(P_X, LaPlace)
                
                ##Jeżeli nie ma wszystkich wartości w kolumnie dodajemy kolumne o prawdopodobienstwie 0.0 dla brakujacego elementu
                ##nwm czy potrzebne

                est_num = set(X[:,0])
                for el in P_X:
                    if el[0] in est_num:
                        est_num.remove(el[0])
                if len(list(est_num)) > 0:
                    for el in list(est_num):
                        P_X.append([int(el), 0, 0.0])

                ##Liczymy prawdopodobieństwo warunkowe dla każdego elementu i dodajemy do listy P
                ## Dzielenie przez P_Y to liczba występowania y czy jego prawdopodobienstwo??? ( jako liczba wystepowania nie dziala)
                for X_el_num in range(len(P_X)):
                    P.append([P_Y[y_el_num][0], P_X[X_el_num][0], (P_Y[y_el_num][2] * P_X[X_el_num][2])/P_Y[y_el_num][1]]) #1 el - y(wartość 1 - 3), 2 el - X(wartość 1 - 3 po dyskretyzacji), 3 - prawdopodobienstwo warunkowe
                
                P_semifinal.append(P)
            P_final.append(P_semifinal)
        return np.array(P_final)