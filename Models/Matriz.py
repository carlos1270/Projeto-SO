# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 15:44:56 2020

@author: carlo
"""

class Matriz:
    def __init__(self, matriz):
        self.matriz      = matriz
        self.quantLinhas = len(matriz)
        self.quantCol    = len(matriz[0])
    
    def getLinha(self, n):
        return [i for i in self.matriz[n]]

    def getCol(self, n):
        return [i[n] for i in self.matriz]
        
    def mult_mat(self, mat_b):
        matrizFinal = []
        for i in range(self.quantLinhas):
            linha = []
            for j in range(mat_b.quantCol):
                resultado = 0
                # multiplica cada linha de mat1 por cada coluna de mat2;
                listMult = [x*y for x, y in zip(self.getLinha(i), mat_b.getCol(j))]
        
                # e em seguida adiciona a matFinal a soma das multiplicações
                resultado = sum(listMult)
                linha.append(resultado)
                
            matrizFinal.append(linha)
                
        return matrizFinal  