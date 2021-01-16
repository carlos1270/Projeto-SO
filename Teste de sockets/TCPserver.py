# -*- coding: utf-8 -*-

from decodificadorDeStringParaMatrizes import *
import socket
from Models.Matriz import Matriz

serverPort = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('O servidor está rodando')
while True:
    connectionSocket, addr = serverSocket.accept()
    print('conexão aceita')
    matrizes = connectionSocket.recv(1024)
    mat1 = Matriz(str_matriz(matrizes.decode())[0])
    mat2 = Matriz(str_matriz(matrizes.decode())[1])
    print(mat2.mult_mat(mat1))
     
    connectionSocket.send(str(mat2.mult_mat(mat1)).encode())
    connectionSocket.close()
    
"""
mat1 = Matriz(str_matriz(str(matriz).encode()))
mat2 = Matriz(str_matriz(str(matriz).encode()))
print(mat2.mult_mat(mat1))


    
SSID:	TITA MADEREIRA_5G
Protocolo:	Wi-Fi 5 (802.11ac)
Tipo de segurança:	WPA2-Personal
Banda de rede:	5 GHz
Canal de rede:	36
Endereço IPv6:	2804:4498:8070:300:5981:449b:fd95:7f5b
Endereço IPv6 de link local:	fe80::5981:449b:fd95:7f5b%16
Servidores DNS IPv6:	2804:4498:8ff0::1
2804:4498:8ff0::2
Endereço IPv4:	10.0.0.129
Servidores DNS IPv4:	10.0.0.1
Fabricante:	Intel Corporation
Descrição:	Intel(R) Wireless-AC 9462
Versão do driver:	22.10.0.7
Endereço físico (MAC):	94-E6-F7-57-66-97
"""
