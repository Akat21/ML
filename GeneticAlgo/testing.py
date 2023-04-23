import numpy as np
import matplotlib.pyplot as plt

pop = 10
n = 5

def GenerateP_0(pop, n):
    '''Generuje P_0'''
    P_0 = []
    for i in range(pop):
        P_0.append(np.random.choice(n, size=n, replace=False) + 1)
    return np.array(P_0)

def evaluate(P):
    '''Zwraca liczbę bić'''
    res = []
    if len(np.shape(P)) == 2:
        for el in P:
            res.append(beats_counter(el))
        return res
    elif len(np.shape(P)) == 1:
        return beats_counter(P)

def beats_counter(pos):
    '''Liczy bicia'''
    cnt = 0
    #Iterujemy po każdym elemencie
    for iter in range(len(pos) - 1):
        #Kolumny to indeksy, a wiersze to zawartość listy pos
        for col, row in enumerate(pos[iter:]):
            #Sprawdzamy czy kolumna nie jest ustawiona na ostatnią, i przechodzimy po liście w celu poszukiwania bić
            if(col == (len(pos[iter:]) - 1)):
                break
            else:
                if Attack(row, col + 1, pos[col + iter + 1], col + 2) == True:
                    cnt += 1
    return cnt

def Attack(q_row, q_col, o_row, o_col):
    '''Sprawdza czy jest bicie między 2 hetmanami q - actual_queen, o - opponent'''
    if q_row == o_row:
        return True
    elif q_col == o_col:
        return True
    elif (np.abs(q_row - o_row) == np.abs(q_col - o_col)):
        return True
    else:
        return False

def selection(P):
    '''Dokonuje selekcji turniejowej, zwraca P_n z powtórkami'''
    i = 0
    P_n = []
    while i < pop:
        i_1 = np.random.randint(pop)
        i_2 = np.random.randint(pop)
        if i_1 != i_2:
            if i_1 != i_2:
                if evaluate(P[i_1]) <= evaluate(P[i_2]):
                    P_n.append(P[i_1])
                else:
                    P_n.append(P[i_2])
                i += 1
    return np.array(P_n)

def crossover(P):
    '''Swapuje miejscami kilka losowych wartości'''
    i = 0
    p_c = 0.7
    while i < pop - 2:
        if np.random.rand() <= p_c:
            P[[i + 1, i]] = P[[i, i + 1]]
            i += 2
    return P

def mutation(P):
    '''Usuwa i dodaje nową wartość do populacji'''
    i = 0
    p_m = 0.5
    while i < pop:
        if np.random.rand() <= p_m:
            P[i] = np.random.choice(n, size=n, replace=False) + 1
        i += 1
    return P

def main():
    ff = []
    P_0 = GenerateP_0(pop, n)
    P = P_0
    gen = 0
    gens = []
    gen_max = 1000
    ff_max = 0
    best = np.where(evaluate(P_0) == np.amin(evaluate(P_0)))[0][0]
    print(best)
    while ((gen < gen_max) and (evaluate(P[best]) > ff_max)):
        P_n = selection(P)

        P_n = crossover(P_n)

        P_n = mutation(P_n)

        #Y w wykresie - funkcja przystosowania
        ff.append(np.mean(evaluate(P_n)))

        best = np.where(evaluate(P_n) == np.amin(evaluate(P_n)))[0][0]
        P = P_n
        gen += 1
        #X w wykresie(numer generacji)
        gens.append(gen)
    
    print(P[best], evaluate(P[best]))
    return ff, gens


ff_mean, gen = main()

plt.plot(gen, ff_mean)
plt.savefig("plot.png", format = "png")
plt.show()
