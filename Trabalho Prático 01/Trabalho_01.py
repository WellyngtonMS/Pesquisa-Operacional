# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 19:47:15 2020

@author: Wellyngton
"""
from __future__ import print_function
from ortools.linear_solver import pywraplp

def main():
    #-----informando o nome do arquivo
    print("Digite o nome do arquivo a ser lido:")
    nome = input()
    
    #-----abertura e leituraa iniciaia do arquivo
    arquivo = open(nome, 'r')
    n_vertices = int(arquivo.readline())
    n_arcos = int(arquivo.readline())
    origem = int(arquivo.readline())
    escoadouro = int(arquivo.readline())
    
    #-----inicializando variáveis e preenchendo com os valores restantes do arquivo
    
    #capacidade de cada arco, representado por matriz, cada linha e coluna representa um vértice e a capacidade entre eles
    capacidade = [[0 for i in range(n_vertices)] for i in range(n_vertices)]
    list = [] #lista vazia que armazena arco por arco, linha a linha
    for i in range(0, n_arcos):
      linha = arquivo.readline()#le a linha inteira
      for j in linha.split():#quebra a linha pelos espaços
        list.append(j)
      capacidade[int(list[0])-1][int(list[1])-1] = int(list[2])
      list = []
    
    #declarando o solver conforme https://developers.google.com/optimization/lp/glop#python
    solver = pywraplp.Solver('FluxoMáximo', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    capacidade[escoadouro-1][origem-1] = solver.infinity()
    
    #variáveis que se unem por um arco, Xij
    variaveis = [[0 for i in range(n_vertices)] for i in range(n_vertices)]
    #criando e definindo as variáveis no solver
    for i in range(0, n_vertices):
      for j in range(0, n_vertices):
        if(capacidade[i][j] > 0):#se a capacidade do vértice for maior que zero, cria a variável no solver
          variaveis[i][j] = solver.NumVar(0, solver.infinity(), '')
          
    #-----tratamento das restrições e preenchimento dos demais valores
    
    #restrição da capacidade em cada arco
    restricoes_arcos = [[0 for i in range(n_vertices)] for i in range(n_vertices)]
    #percorre os vertices verificando a capacidade de cada um
    for i in range (0, n_vertices):
      for j in range(0, n_vertices):
        if(capacidade[i][j] > 0):#se for maior que zero adiciona restrição ao solver na respectiva posição
          restricoes_arcos[i][j] = solver.Constraint(0, capacidade[i][j])
          restricoes_arcos[i][j].SetCoefficient(variaveis[i][j], 1)
          
    #-----tratamento dos fluxos dos vértices e preenchimento dos valores no solver
    
    fluxo = [0 for i in range(n_vertices)]
    #demandas do nó
    for i in range (0, n_vertices):
      fluxo[i] = solver.Constraint(0, 0)
      #fluxo que sai do vértice
      for x in range (0, n_vertices):
        if(capacidade[i][x] > 0): 
          fluxo[i].SetCoefficient(variaveis[i][x], -1)
      #fluxo que entra no vértice
      for y in range (0, n_vertices):
        if(capacidade[y][i] > 0):
          fluxo[i].SetCoefficient(variaveis[y][i], 1)
         
    #-----função objetivo 
    
    custo = [[0 for i in range(n_vertices)] for i in range(n_vertices)]
    custo[escoadouro-1][origem-1] = -1
    objective = solver.Objective()
    for i in range(0, n_vertices):
      for j in range(0, n_vertices):
        if(capacidade[i][j] > 0):
          objective.SetCoefficient(variaveis[i][j], custo[i][j])
    objective.SetMinimization()
    
    #variável de resolução
    opt_solution = 0

    #solving
    status = solver.Solve()
    if status == solver.OPTIMAL:
      for i in range(0, n_vertices):
        for j in range(0, n_vertices):
          if(i != escoadouro-1 | j != origem-1):
            if(capacidade[i][j] > 0):
                print('Arco',i+1,'->',j+1,' Valor:',variaveis[i][j].solution_value(), 'Capacidade:', capacidade[i][j])     
          opt_solution = variaveis[escoadouro-1][origem-1].solution_value()
      #o valor de cada variável na solução
      print('\nSolution')
      #o valor objetivo da solução
      print('Optimal objective value =', opt_solution)  
    else: 
      print("Without solution")   
    

if __name__ == '__main__':
    main()
    