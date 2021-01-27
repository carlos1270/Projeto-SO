import socket
import threading

global maqA, maqB
maqA = "172.17.0.2"
maqB = "172.17.0.3"
maqC = '172.17.0.4'

global linhas_A, linhas_B, colunas_B, colunas_A, matrizA, matrizB

class ClienteThread(threading.Thread):
    def __init__(self, server, porta):
        threading.Thread.__init__(self)
        self.server = server
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, porta))

def enviarMatriz(thread):
    print("Entre com a matriz: padrao")
    #recebe a quantidade de linhas  e colunas
    # linhas_A, colunas_A = map(str, input().split(" "))
    # #recebe a matriz em uma linha unica
    # matrizA = input()
    # linhas_B, colunas_B = map(str, input().split(" "))
    # matrizB = input()
    #coloca tudo das duas matrizes em uma unica string pra enviar
    linhas_A = str(2)
    colunas_A = str(2)
    matrizA = "1 2 3 4"
    linhas_B = str(2)
    colunas_B = str(2)
    matrizB = "1 2 3 4"
    entrada = linhas_A+' '+colunas_A+' '+matrizA+' '+linhas_B+' '+colunas_B+' '+matrizB
    thread.socket.send(entrada.encode())

entrada = "Requisitar"

while entrada != "sair":
    print("Digite uma máquina: ", end = "")
    entrada = input()
    if(entrada == "A"):
        thread = ClienteThread(maqA, 12100)
        enviarMatriz(thread)
        resposta = thread.socket.recv(1024)
        print(resposta.decode())
    elif(entrada == "B"):
        thread = ClienteThread(maqB, 12100)
        enviarMatriz(thread)
        resposta = thread.socket.recv(1024)
        print(resposta.decode())
