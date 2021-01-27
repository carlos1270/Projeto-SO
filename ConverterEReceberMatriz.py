def converterStringMatriz(linhas, colunas, matAux):
    if(len(matAux) == linhas*colunas):
        matriz = []
        for k in range(0, linhas*colunas, colunas):
            linha = matAux[k:k+colunas]
            matriz.append(linha)
        return matriz
    else:
        print("Matriz inválida")
        
def dividirEntrada(entrada):
    entradaAux = list(map(int, entrada.split(" ")))
    linhas_A = entradaAux[0]
    colunas_A = entradaAux[1]
    matrizA = entradaAux[2:(linhas_A*colunas_A)+2]

    linhas_B = entradaAux[(linhas_A*colunas_A)+2]
    colunas_B = entradaAux[(linhas_A*colunas_A)+3]
    matrizB = entradaAux[(linhas_A*colunas_A)+4:]

    MA = converterStringMatriz(linhas_A, colunas_A, matrizA)
    MB = converterStringMatriz(linhas_B, colunas_B, matrizB)
    return [MA, MB]
