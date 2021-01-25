import socket
import threading
import time

global nucleos
nucleos = [[False], [False, False], [False, False, False]]

class ThreadMaquinas(threading.Thread):
    def __init__(self, connectionMaquina, addrMaquina):
        threading.Thread.__init__(self)
        self.connectionMaquina = connectionMaquina
        self.addrMaquina = addrMaquina

    def run(self):
        print("atualizando nucleos requisicao de outra maquina")
        informacao = self.connectionMaquina.recv(1024)
        info = get_info(informacao.decode())
        semaforo.acquire()
        if(info[0] == 0):
            nucleos[info[1]-1][info[2]-1] = False
        else:
            nucleos[info[1]-1][info[2]-1] = True
        semaforo.release()
        self.connectionMaquina.send('Atualizado'.encode())
        self.connectionMaquina.close()
        print(nucleos)


class MyThread(threading.Thread):
    def __init__(self, connectionSocket, addr):
        threading.Thread.__init__(self)
        self.connectionSocket = connectionSocket
        self.addr = addr

    def run(self):
        print("Requisicao do cliente recebida")
        informacao = self.connectionSocket.recv(1024)
        mensagem = verificarDisponibilidade()
        self.connectionSocket.send(mensagem.encode())
        self.connectionSocket.close()

def get_info(informacao):
    mensagem = list(map(int, informacao.split(" ")))
    return mensagem

def atualizarNucleo(server, porta, liberado, maquina, nucleo):
    print("Atualizando núcleos")
    atualizarInformacaoNucleo = True
    clientSocketBuffer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocketBuffer.connect((server, porta))

    while atualizarInformacaoNucleo:
        if(liberado):
            clientSocketBuffer.send(str(str(1)+" "+str(maquina)+" "+str(nucleo)).encode())
        else:
            clientSocketBuffer.send(str(str(0)+" "+str(maquina)+" "+str(nucleo)).encode())

        resposta = clientSocketBuffer.recv(1024)
        if (resposta.decode() == 'Atualizado'):
            print(nucleos)
            atualizarInformacaoNucleo = False
            clientSocketBuffer.close()
        else:
            print('Ocupado')

def atualizarNucleoLocal(liberado, maquina, nucleo):
    semaforo.acquire()
    nucleos[maquina-1][nucleo-1] = liberado
    semaforo.release()

def processarMatriz():
    time.sleep(30)
    return "60 segundos de processo"

def controlarBufferNucleos(ip1, maquina, nucleo):
    atualizarNucleoLocal(True, maquina, nucleo)
    atualizarNucleo(ip1, 12000, True, maquina, nucleo)
    matriz = processarMatriz()
    atualizarNucleoLocal(False, maquina, nucleo)
    atualizarNucleo(ip1, 12000, False, maquina, nucleo)
    return matriz

def verificarDisponibilidade():
    print("Verificando onde pode processar a matriz")
    maquinaEncontrada = False
    while maquinaEncontrada == False:
        if(nucleos[0][0] == False):
            maquinaEncontrada = True
            print("Processando na máquina A")
            return controlarBufferNucleos('172.17.0.2', 1, 1)
        elif(nucleos[1][0] == False):
            maquinaEncontrada = True
            return "Processando na máquina B, máquina A está indisponível no momento."
        elif(nucleos[1][1] == False):
            maquinaEncontrada = True
            return "Processando na máquina B, máquina A está indisponível no momento."
        elif(nucleos[2][0] == False):
            maquinaEncontrada = True
            return "Processando na máquina C, máquina A está indisponível no momento."
        elif(nucleos[2][1] == False):
            maquinaEncontrada = True
            return "Processando na máquina C, máquina A está indisponível no momento."
        elif(nucleos[2][2] == False):
            maquinaEncontrada = True
            return "Processando na máquina C, máquina A está indisponível no momento."
        else:
            print("Nenhuma máquina disponível")

def startCliente():
    while True:
        connectionSocket, addr = socktBuffer.accept()
        thread = MyThread(connectionSocket, addr)
        thread.start()

def startServer():
    while True:
        connectionMaquina, addrMaquina = socketMaquinas.accept()
        threadMaquina = ThreadMaquinas(connectionMaquina, addrMaquina)
        threadMaquina.start()

global semaforo, socktBuffer, socketMaquinas

semaforo = threading.Semaphore()
socktBuffer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktBuffer.bind(('', 12100))
socktBuffer.listen(2)

socketMaquinas = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketMaquinas.bind(('', 12000))
socketMaquinas.listen(2)
print('Maquina A rodando')



t1 = threading.Thread(target=startCliente)
t2 = threading.Thread(target=startServer)
t1.start()
t2.start()

t1.join()
t2.join()
