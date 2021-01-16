def str_matriz(str_matriz):
    matriz = []
    matrizes = []
    linha = []
    numero = ''
    for i in range(len(str_matriz) - 1):
        if (i != 0):
            if (str_matriz[i] != '[' and str_matriz[i] != ' ' and str_matriz[i] != ',' and str_matriz[i] != ']' and str_matriz[i+1] == ','):
                numero += str(str_matriz[i])
            elif (str_matriz[i] != '[' and str_matriz[i] != ' ' and str_matriz[i] != ',' and str_matriz[i] != ']' and str_matriz[i+1] != ','):
                numero += str(str_matriz[i])
                    
            if ((str_matriz[i] == ',' or str_matriz[i] == ']') and numero != ''):
                linha.append(int(numero))
                numero = ''

            if (str_matriz[i] == ']' and len(linha) != 0):
                matriz.append(linha)
                linha = []
                    
            elif (str_matriz[i-1] == ']' and str_matriz[i] == ']' and len(matriz) != 0):
                matrizes.append(matriz)
                matriz = []

            
    return matrizes

matriz = [[[1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10]], [[1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10], [1, 2, 3, 5, 6, 7, 4, 8, 9, 10]]]


