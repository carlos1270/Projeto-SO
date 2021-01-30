import time
import socket
import threading

def atualizarSemaforo(ip, porta, estadoSemaforo):
        socktAtualizarSemaforo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socktAtualizarSemaforo.connect((ip, porta))
        resposta = "0".encode()
        while not(int(resposta.decode())):
            socktAtualizarSemaforo.send(estadoSemaforo)
            resposta = socktAtualizarSemaforo.recv(1024)

        socktAtualizarSemaforo.close()


atualizarSemaforo('10.0.0.129', 12200, "1".encode())
atualizarSemaforo('10.0.0.129', 12201, "0".encode())


global semaforo, socktBuffer

###print()
