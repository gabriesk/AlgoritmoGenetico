AlgoritmoGenetico
=================

| Trabalho para matéria de Inteligência Artificial do Ifes - Serra, 2021-1

| Este tutorial tem o objetivo de ensinar como executar o Algoritmo Genético para buscar o valor mínimo da função |equation| dentro do limite horizontal de x = [-20, 20].


Execução
========


Para executar o algoritmo, na linha de comando execute ``python AG.py``


Código
======


O
`código <https://github.com/gabriesk/AlgoritmoGenetico/blob/main/AG.py>`__
foi escrito em Python usando as bibliotecas *randon* e *math*.

Explicação das funções
======================

.. code:: python

      from math import cos
      from random import randint

      X_RANGE = [-20, 20]
      POP_TAM = 10
      MUT_TAX = 2
      CROSS_TAX = 60
      GER_NUM = 10
      NUM_BITS = 16

As primeiras linhas são as variáveis globais usadas como parâmetro para
o algorítmo.

-  *X*\ RANGE\_ é uma lista que determina os limites horizontais no
   plano x;
-  *POP*\ TAM\_ é o tamanho da população;
-  *MUT*\ TAX\_ é a probalidade de mutação do indivíduo;
-  *CROSS*\ TAX\_ é a probalidade de crossover do indivíduo;
-  *GER*\ NUM\_ são os números de gerações que passarão pela execução;
-  *NUM*\ BITS\_ é o número de bits de cada indivíduo.

A próxima função refere à criação da população:

.. code:: python

    def createPop():
    pop = [[] for _ in range(POP_TAM)]

    for ind in pop:
        num = randint(X_RANGE[0], X_RANGE[1])
        num_bin = bin(num).replace('0b', '' if num < 0 else '+').zfill(NUM_BITS)

        for bit in num_bin:
            ind.append(bit)

    return pop

A função *function()* avalia o indíviduo dentro da função proposta.

.. code:: python

    def function(num_bin):
    x = int(''.join(num_bin), 2)
    return cos(x) * x + 2

*check*\ func()\_ separa a população em indivíduos para chamar
*function()*

.. code:: python

    def check_func(pop):
    y = []

    for ind in pop:
        num_bin = function(ind)

        y.append(num_bin)

    return y

*select()* seleciona dois indivíduos em torneio. Esta função será
utilizada na definição de pai e mãe no crossover.

.. code:: python

    def select(pop):
    tourn = list(zip(pop, check_func(pop)))

    ind1 = tourn[randint(0, POP_TAM - 1)]
    ind2 = tourn[randint(0, POP_TAM - 1)]

    return ind1[0] if ind1[1] >= ind2[1] else ind2[0]

*fix*\ range()\_ verifica se um indivíduo se encontra dentro do limite
do plano x. Caso não se encontre, o valor do indivíduo será o limite nos
extremos negativo ou positivo. Caso menor que -20, o indivíduo será -20.
No outro extremo, caso passe de 20, o indivíduo será 20.

.. code:: python

    def fix_range(ind):
    if int(''.join(ind), 2) < X_RANGE[0]:
        fix = bin(X_RANGE[0]).replace('0b', '' if X_RANGE[0] < 0 else '+').zfill(NUM_BITS)

        for i, bit in enumerate(fix):
            ind[i] = bit

    elif int(''.join(ind), 2) > X_RANGE[1]:
        fix = bin(X_RANGE[1]).replace('0b', '' if X_RANGE[1] < 0 else '+').zfill(NUM_BITS)
        for i, bit in enumerate(fix):
            ind[i] = bit

*crossover()* faz o cruzamento entre dois indivíduos para gerar dois
filhos.

.. code:: python

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

*mutation()* executa a mutação de um indivíduo dentro da probabilidade
determinada.

.. code:: python

    def mutation(ind):
    tab = str.maketrans("+-01", "-+10")

    if randint(1, 100) <= MUT_TAX:
        bit = randint(0, NUM_BITS - 1)
        ind[bit] = ind[bit].translate(tab)

    fix_range(ind)

*findBest()* irá encontrar dentro da população o melhor indivíduo para
passar para a próxima como modelo.

.. code:: python

    def findBest(pop, y):
    cand = list(zip(pop, y))

    chosen = max(cand)
    x_chosen = int(''.join(chosen[0]), 2)

    return x_chosen, chosen

.. |equation| image:: https://user-images.githubusercontent.com/65257922/130359253-ab5935d0-94b5-47fe-a8d5-392d7e4019b1.png
