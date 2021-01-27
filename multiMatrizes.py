# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 14:40:31 2020

@author: carlo
"""
def numCol(matriz):
    return len(matriz[0]);

def numLin(matriz):
    return len(matriz);

def mult_valida(mat_a, mat_b):
    #Número de colunas de mat_a tem que ser igual ao número de linhas de mat_2
    num_col_a = numCol(mat_a)
    num_linhas_b = numLin(mat_b)
    if(num_col_a == num_linhas_b):
        return True 
    return False 

def getLinha(matriz, n):
    return matriz[n]

def getCol(matriz, n):
    col = []
    for i in matriz:
        col.append(i[n])
    return col
    
def mult_mat(mat_a, mat_b):
    matrizFinal = []
    for i in range(numLin(mat_a)):
        linha = []
        for j in range(numCol(mat_b)):
            resultado = 0
            # multiplica cada linha de mat1 por cada coluna de mat2;
            listMult = [x*y for x, y in zip(getLinha(mat_a, i), getCol(mat_b, j))]
    
            # e em seguida adiciona a matFinal a soma das multiplicações
            resultado = sum(listMult)
            linha.append(resultado)
            
        matrizFinal.append(linha)
            
    return matrizFinal  
