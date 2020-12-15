# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 19:49:31 2020

@author: Wellyngton
"""

from __future__ import print_function
from ortools.linear_solver import pywraplp
from math import sqrt
import matplotlib.pyplot as plt

# função que calcula a distância Dij
def distancia(dXi, dXj, dYi, dYj):
    dist = sqrt(((dXi-dXj)**2) + ((dYi-dYj)**2))
    return dist
    
def main():
    #-----informando o nome do arquivo
    print("Digite o nome do arquivo a ser lido:")
    nome = input()
    
    #-----abertura e leitura inicial do arquivo
    arquivo = open(nome, 'r')
    #-----formato do arquivo esperado
    # n = número do distrito
    # X = distância máxima do distrito i até a 1ª UPA
    # Y = distância máxima do distrito i até a 2ª UPA
    # Z = limite para a menor distância entre duas UPAs
    # x, y = coordenadas do distrito n
    # n X Y Z
    # x1 y1
    # .
    # .
    # .
    # xn yn
    
    list = []
    linha = arquivo.readline() # le a primeira linha inteira
    for i in linha.split(): # quebra a linha pelos espaços
      list.append(i)
    n = int(list[0])
    X = int(list[1])
    Y = int(list[2])
    Z = int(list[3])
    
    # lista vazia que armazena uma linha de cada vez, n x y
    list = []
    distritos = [[0 for i in range(2)] for i in range(n)] # lista de distritos, cada distrito com valor x e y respectivo
    for i in range(0, n):
      linha = arquivo.readline() # le a primeira linha inteira
      for j in linha.split(): # quebra a linha pelos espaços
        list.append(j)
      distritos[i][0] = int(list[0])
      distritos[i][1] = int(list[1])
      list = [] # lista vazia
    
    
    # declarando o solver conforme https://developers.google.cn/optimization/mip/integer_opt?hl=zh-cn
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # exemplo de implementação seguido, que usa variável binária https://developers.google.cn/optimization/assignment/assignment_example?hl=zh-cn
    # variáveis booleanas
    b = {}
    for i in range(n):
      b[i] = solver.IntVar(0, 1, 'b[%d]'%i)
    
    for i in range(n):
        # primeira restrição
        solver.Add(solver.Sum(b[j] for j in range(n)
                   if distancia(distritos[i][0], distritos[j][0], distritos[i][1], distritos[j][1]) <= X) >= 1)
        # segunda restrição
        solver.Add(solver.Sum(b[j] for j in range(n)
                    if distancia(distritos[i][0], distritos[j][0], distritos[i][1], distritos[j][1]) <= Y) >= 2)
        
    # terceira restrição
    for i in range(n):
      for j in range(n):
        if i != j:
          if distancia(distritos[i][0], distritos[j][0], distritos[i][1], distritos[j][1]) <= Z: 
            solver.Add(b[i] + b[j] <= 1)
            
    # função Objetivo
    solver.Minimize(solver.Sum(b[i] for i in range(n)))
    
    # para exportar e visualizar o modelo construído, basta retirar o comentário da linha abaixo
    #print(solver.ExportModelAsLpFormat(True).replace('\\', '').replace(',_', ','), sep='\n')
    distritosUPA = []
    cont = 0
    status = solver.Solve()

    #print('Total cost = ', solver.Objective().Value(), '\n')
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
      for i in range(n):
        if b[i].solution_value() >= 0.99:
          cont = cont+1
          distritosUPA.append(i+1)
      print("UPAs instaladas nos distritos", distritosUPA)  
      print('No total, foram instaladas %d UPAs'%cont)
      
      menores = []
      copia = []
      for i in range(n):
        for j in range(0, cont):
          flag = distancia(distritos[i][0], distritos[distritosUPA[j]-1][0], distritos[i][1], distritos[distritosUPA[j]-1][1])
          menores.append(flag)
        x = min(menores)
        copia = sorted(menores)
        if copia[1] > Y:
            print("Maior")
        print('A distância do distrito %d para a 1ª UPA é %.2f km e para a 2ª UPA é %.2f km'%(i+1, x, copia[1]))
        menores = []
        copia = []
      for i in range(len(distritosUPA)):
        flag = 0  
        for j in range(len(distritosUPA)):
          if i != j:
            valor = distancia(distritos[distritosUPA[i]-1][0], distritos[distritosUPA[j]-1][0], distritos[distritosUPA[i]-1][1], distritos[distritosUPA[j]-1][1])
            if valor >= Z:
              flag = 1
              
        if flag == 0:
          print('A distância da UPA instalada no distrito %d para a mais próxima, é menor que %d km'%(distritosUPA[i], Z))
        else:
          print('A distância da UPA instalada no distrito %d para a mais próxima, é maior que %d km'%(distritosUPA[i], Z))  
            
          
    # gráfico
    for i in range(n):
      plt.plot(distritos[i][0], distritos[i][1], 'o', color = 'black') # distritos em preto
      if b[i].solution_value() >= 1.0:
        plt.plot(distritos[i][0], distritos[i][1], 'o', color = 'blue')# UPAs instaladas em azul
        
    plt.ylabel('Eixo Y')
    plt.xlabel('Eixo X')
    plt.show()
    
    
if __name__ == '__main__':
    main()