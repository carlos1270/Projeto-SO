# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 15:55:52 2020

@author: carlo
"""

from Models.Matriz import Matriz

mat1 = Matriz([[1, 2, 3], [2, 3, 2]]);
mat2 = Matriz([[2, 3], [1, 2]]);
print(mat2.mult_mat(mat1))