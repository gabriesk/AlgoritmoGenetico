# AlgoritmoGenetico
Trabalho para matéria de Inteligência Artificial do Ifes - Serra, 2021/1.
Este tutorial tem o objetivo de ensinar como executar o Algoritmo Genético para buscar o valor mínimo da função ![equation](https://user-images.githubusercontent.com/65257922/130359253-ab5935d0-94b5-47fe-a8d5-392d7e4019b1.png) dentro do limite horizontal de x = [-20, 20].

# Execução
Para executar o algoritmo, na linha de comando execute ```python AG.py```

# Código
O [código](https://github.com/gabriesk/AlgoritmoGenetico/blob/main/AG.py) foi escrito em Python usando as bibliotecas _randon_ e _math_.

# Explicação das funções

      from math import cos
      from random import randint

      X_RANGE = [-20, 20]
      POP_TAM = 10
      MUT_TAX = 2
      CROSS_TAX = 60
      GER_NUM = 10
      NUM_BITS = 16

As primeiras linhas são as variáveis globais usadas como parâmetro para o algorítmo.

* _X_RANGE_ é uma lista que determina os limites horizontais no plano x;
* _POP_TAM_ é o tamanho da população;
* _MUT_TAX_ é a probalidade de mutação do indivíduo;
* _CROSS_TAX_ é a probalidade de crossover do indivíduo;
* _GER_NUM_ são os números de gerações que passarão pela execução;
* _NUM_BITS_ é o número de bits de cada indivíduo.


A próxima função refere à criação da população:

    def createPop():
    pop = [[] for _ in range(POP_TAM)]

    for ind in pop:
        num = randint(X_RANGE[0], X_RANGE[1])
        num_bin = bin(num).replace('0b', '' if num < 0 else '+').zfill(NUM_BITS)

        for bit in num_bin:
            ind.append(bit)

    return pop

A função _function()_ avalia o indíviduo dentro da função proposta.

    def function(num_bin):
    x = int(''.join(num_bin), 2)
    return cos(x) * x + 2

_check_func()_ separa a população em indivíduos para chamar _function()_

    def check_func(pop):
    y = []

    for ind in pop:
        num_bin = function(ind)

        y.append(num_bin)

    return y

_select()_ seleciona dois indivíduos em torneio. Esta função será utilizada na definição de pai e mãe no crossover.
    
    def select(pop):
    tourn = list(zip(pop, check_func(pop)))

    ind1 = tourn[randint(0, POP_TAM - 1)]
    ind2 = tourn[randint(0, POP_TAM - 1)]

    return ind1[0] if ind1[1] >= ind2[1] else ind2[0]

_fix_range()_ verifica se um indivíduo se encontra dentro do limite do plano x. Caso não se encontre, o valor do indivíduo será o limite nos extremos negativo ou positivo. Caso menor que -20, o indivíduo será -20. No outro extremo, caso passe de 20, o indivíduo será 20.

    def fix_range(ind):
    if int(''.join(ind), 2) < X_RANGE[0]:
        fix = bin(X_RANGE[0]).replace('0b', '' if X_RANGE[0] < 0 else '+').zfill(NUM_BITS)

        for i, bit in enumerate(fix):
            ind[i] = bit

    elif int(''.join(ind), 2) > X_RANGE[1]:
        fix = bin(X_RANGE[1]).replace('0b', '' if X_RANGE[1] < 0 else '+').zfill(NUM_BITS)
        for i, bit in enumerate(fix):
            ind[i] = bit

_crossover()_ faz o cruzamento entre dois indivíduos para gerar dois filhos.

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

_mutation()_ executa a mutação de um indivíduo dentro da probalidade determinada.

    def mutation(ind):
    tab = str.maketrans("+-01", "-+10")

    if randint(1, 100) <= MUT_TAX:
        bit = randint(0, NUM_BITS - 1)
        ind[bit] = ind[bit].translate(tab)

    fix_range(ind)
    
_findBest()_ irá encontrar dentro da população o melhor indivíduo para passar para a próxima como modelo.

    def findBest(pop, y):
    cand = list(zip(pop, y))

    chosen = max(cand)
    x_chosen = int(''.join(chosen[0]), 2)

    return x_chosen, chosen
