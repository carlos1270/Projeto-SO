# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 18:24:37 2020

@author: carlo
"""
from decodificadorDeStringParaMatrizes import *
import socket
from Models.Matriz import Matriz
import threading

serverName = '10.0.0.129'
serverPort = 12000

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print(matriz)
clientSocket.send(str(matriz).encode())
modifiedSetence = clientSocket.recv(1024)
print('Resposta: ', modifiedSetence.decode())
clientSocket.close()

"""
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
