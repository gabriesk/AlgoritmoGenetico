'''
Trabalho de Inteligência Artificial (2021/1)
Gabriel N. dos Passos - 20182BSI0450
'''

from math import cos
from random import randint

# Parâmetros para Algoritmo

X_RANGE = [-20, 20]
POP_TAM = 10
MUT_TAX = 2
CROSS_TAX = 60
GER_NUM = 10
NUM_BITS = 16


def main():
    ag = createPop()

    chk = check_func(ag)

    for i in range(GER_NUM):
        print("Geração {}: {}".format(i, findBest(ag, check_func(ag))))

        new_pop = []

        while len(new_pop) < POP_TAM:
            p = select(ag)
            m = select(ag)

            f1, f2 = crossover(p, m)

            mutation(f1)
            mutation(f2)
            new_pop.append(f1)
            new_pop.append(f2)

        ag = new_pop
        chk = check_func(ag)

    print("Geração {}: {}".format(i+1, findBest(ag, check_func(ag))))

    return 0



def createPop():
    pop = [[] for _ in range(POP_TAM)]

    for ind in pop:
        num = randint(X_RANGE[0], X_RANGE[1])
        num_bin = bin(num).replace('0b', '' if num < 0 else '+').zfill(NUM_BITS)

        for bit in num_bin:
            ind.append(bit)

    return pop


def function(num_bin):
    x = int(''.join(num_bin), 2)
    return cos(x) * x + 2


def check_func(pop):
    y = []

    for ind in pop:
        num_bin = function(ind)

        y.append(num_bin)

    return y


def select(pop):
    tourn = list(zip(pop, check_func(pop)))

    ind1 = tourn[randint(0, POP_TAM - 1)]
    ind2 = tourn[randint(0, POP_TAM - 1)]

    return ind1[0] if ind1[1] >= ind2[1] else ind2[0]


def fix_range(ind):
    if int(''.join(ind), 2) < X_RANGE[0]:
        fix = bin(X_RANGE[0]).replace('0b', '' if X_RANGE[0] < 0 else '+').zfill(NUM_BITS)

        for i, bit in enumerate(fix):
            ind[i] = bit

    elif int(''.join(ind), 2) > X_RANGE[1]:
        fix = bin(X_RANGE[1]).replace('0b', '' if X_RANGE[1] < 0 else '+').zfill(NUM_BITS)
        for i, bit in enumerate(fix):
            ind[i] = bit


def crossover(p, m):
    if randint(1, 100) <= CROSS_TAX:
        cut = randint(1, NUM_BITS - 1)
        f1 = p[:cut] + m[cut:]
        f2 = m[:cut] + p[cut:]
        fix_range(f1)
        fix_range(f2)

    else:
        f1 = p[:]
        f2 = m[:]

    return (f1, f2)


def mutation(ind):
    tab = str.maketrans("+-01", "-+10")

    if randint(1, 100) <= MUT_TAX:
        bit = randint(0, NUM_BITS - 1)
        ind[bit] = ind[bit].translate(tab)

    fix_range(ind)


def findBest(pop, y):
    cand = list(zip(pop, y))

    chosen = max(cand)
    x_chosen = int(''.join(chosen[0]), 2)

    return x_chosen, chosen

if __name__ == '__main__':
    main()