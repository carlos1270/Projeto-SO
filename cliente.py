import socket
import threading

class ClienteThread(threading.Thread):
    def __init__(self, server, porta):
        threading.Thread.__init__(self)
        self.server = server
        self.porta = porta
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, porta))

def enviarMatriz(thread):
    print("Entre com a matriz: ")
    #recebe a quantidade de linhas  e colunas
    linhas_A, colunas_A = map(str, input().split(" "))
    #recebe a matriz em uma linha unica
    matrizA = input()
    linhas_B, colunas_B = map(str, input().split(" "))
    matrizB = input()
    #coloca tudo das duas matrizes em uma unica string pra enviar
    entrada = linhas_A+' '+colunas_A+' '+matrizA+' '+linhas_B+' '+colunas_B+' '+matrizB
    thread.socket.send(entrada.encode())


if __name__ == '__main__':
    entrada = "Requisitar"
    while entrada != "sair":
        print("Digite uma máquina: ", end = "")
        entrada = input()
        if(entrada == "A"):
            try:
                thread = ClienteThread('172.17.0.2', 12100)
                enviarMatriz(thread)
                resposta = thread.socket.recv(1024)
                print(resposta.decode())
            except:
                print("Maquina indisponivel no momento")
                continue

        elif(entrada == "B"):
            try:
                thread = ClienteThread('172.17.0.3', 12100)
                enviarMatriz(thread)
                resposta = thread.socket.recv(1024)
                print(resposta.decode())
            except:
                print("Maquina indisponivel no momento")
                continue

        elif(entrada == "C"):
            try:
                thread = ClienteThread('172.17.0.4', 12100)
                enviarMatriz(thread)
                resposta = thread.socket.recv(1024)
                print(resposta.decode())
            except:
                print("Maquina indisponivel no momento")
