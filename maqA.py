import socket
import threading
import ConverterEReceberMatriz as cnvMatriz
import multiMatrizes
import cliente

global nucleos, maqA, maqB, maqC
nucleos = [[False], [False, False], [False, False, False]]

maqA = '172.17.0.2'
maqB = '172.17.0.3'
maqC = '172.17.0.4'

class ThreadLevantarSemaforo(threading.Thread):
    def __init__(self, connection, addr):
        threading.Thread.__init__(self)
        self.connection = connection
        self.addr = addr

    def run(self):
        print("recebendo semaforo atualizado de outra maquina")
        atualizar = self.connection.recv(1024)

        if (int(atualizar.decode())):
            print("1")
            semaforo.acquire()

        self.connection.send("Atualizado".encode())
        self.connection.close()

class ThreadAbaixarSemaforo(threading.Thread):
    def __init__(self, connection, addr):
        threading.Thread.__init__(self)
        self.connection = connection
        self.addr = addr

    def run(self):
        print("recebendo semaforo atualizado de outra maquina")
        atualizar = self.connection.recv(1024)

        if (not(int(atualizar.decode()))):
            print("0")
            semaforo.release()

        self.connection.send("Atualizado".encode())
        self.connection.close()

class ThreadMaquinas(threading.Thread):
    def __init__(self, connectionMaquina, addrMaquina):
        threading.Thread.__init__(self)
        self.connectionMaquina = connectionMaquina
        self.addrMaquina = addrMaquina

    def run(self):
        print("atualizando nucleos requisicao de outra maquina")
        informacao = self.connectionMaquina.recv(1024)
        info = get_info(informacao.decode())
        if(info[0] == 0):
            nucleos[info[1]-1][info[2]-1] = False
        else:
            nucleos[info[1]-1][info[2]-1] = True

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
        matrizes = self.connectionSocket.recv(1024)
        resposta = verificarDisponibilidade(matrizes.decode())
        self.connectionSocket.send(resposta.encode())
        self.connectionSocket.close()

def get_info(informacao):
    mensagem = list(map(int, informacao.split(" ")))
    return mensagem

def atualizarNucleo(server, porta, liberado, maquina, nucleo):
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
            atualizarInformacaoNucleo = False
            clientSocketBuffer.close()
        else:
            print('Ocupado')

def atualizarNucleoLocal(liberado, maquina, nucleo):
    nucleos[maquina-1][nucleo-1] = liberado

def processarMatriz(matrizes):
    print("Processando uma matriz")
    matrizesConvertidas = cnvMatriz.dividirEntrada(matrizes)
    if(multiMatrizes.mult_valida(matrizesConvertidas[0], matrizesConvertidas[1])):
       return str(multiMatrizes.mult_mat(matrizesConvertidas[0], matrizesConvertidas[1]))
    else:
        return("Multiplicação impossível")

def controlarBufferNucleos(maquina, nucleo, matrizes):
    try:
        semaforo.acquire()
        atualizarSemaforo(maqB, 12200, "1".encode())
        atualizarSemaforo(maqC, 12200, "1".encode())
        atualizarNucleoLocal(True, maquina, nucleo)
        atualizarNucleo(maqB, 12000, True, maquina, nucleo)
        atualizarNucleo(maqC, 12000, True, maquina, nucleo)
        semaforo.release()
        atualizarSemaforo(maqB, 12201, "0".encode())
        atualizarSemaforo(maqC, 12201, "0".encode())
    except:
        print("algum erro")

    matriz = processarMatriz(matrizes)
    print("Matriz processada")

    semaforo.acquire()
    try:
        atualizarSemaforo(maqB, 12200, "1".encode())
        atualizarSemaforo(maqC, 12200, "1".encode())
        atualizarNucleoLocal(False, maquina, nucleo)
        atualizarNucleo(maqB, 12000, False, maquina, nucleo)
        atualizarNucleo(maqC, 12000, False, maquina, nucleo)
        semaforo.release()
        atualizarSemaforo(maqB, 12201, "0".encode())
        atualizarSemaforo(maqC, 12201, "0".encode())
    except:
        print("algum erro")

    return matriz

def redirecionarMatrizes(maquina, matrizes):
    try:
        thread = cliente.ClienteThread(maquina, 12100)
        thread.socket.send(matrizes.encode())
        resposta = thread.socket.recv(1024)
        return resposta.decode()
    except:
        print("algum erro")

def verificarDisponibilidade(matrizes):
    print("Verificando onde pode processar a matriz")
    maquinaEncontrada = False
    while maquinaEncontrada == False:

        if(nucleos[0][0] == False):
            maquinaEncontrada = True
            print("Processando na máquina A")
            return controlarBufferNucleos(1, 1, matrizes)
        elif(nucleos[1][0] == False):
            maquinaEncontrada = True
            print("Processando na máquina B, máquina A está indisponível no momento.")
            return redirecionarMatrizes(maqB, matrizes)
        elif(nucleos[1][1] == False):
            maquinaEncontrada = True
            print("Processando na máquina B, máquina A está indisponível no momento.")
            return redirecionarMatrizes(maqB, matrizes)
        elif(nucleos[2][0] == False):
            maquinaEncontrada = True
            print("Processando na máquina C, máquina A está indisponível no momento.")
            return redirecionarMatrizes(maqC, matrizes)
        elif(nucleos[2][1] == False):
            maquinaEncontrada = True
            print("Processando na máquina C, máquina A está indisponível no momento.")
            return redirecionarMatrizes(maqC, matrizes)
        elif(nucleos[2][2] == False):
            maquinaEncontrada = True
            print("Processando na máquina C, máquina A está indisponível no momento.")
            return redirecionarMatrizes(maqC, matrizes)
        else:
            print("Nenhuma máquina disponível")

def atualizarSemaforo(ip, porta, estadoSemaforo):
        socktAtualizarSemaforo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socktAtualizarSemaforo.connect((ip, porta))

        atualizado = True
        while (atualizado):
            socktAtualizarSemaforo.send(estadoSemaforo)
            resposta = socktAtualizarSemaforo.recv(1024)
            if (resposta.decode() == "Atualizado"):
                atualizado = False

        socktAtualizarSemaforo.close()

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

def levantarSemaforoLocal():
    while True:
        connectionSocket, addr = socktLevantar.accept()
        thread = ThreadLevantarSemaforo(connectionSocket, addr)
        thread.start()

def abaixarSemaforoLocal():
    while True:
        connectionSocket, addr = secktAbaixar.accept()
        thread = ThreadAbaixarSemaforo(connectionSocket, addr)
        thread.start()

global semaforo, socktBuffer, socketMaquinas, socktLevantar, secktAbaixar

semaforo = threading.Semaphore()
socktBuffer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktBuffer.bind(('', 12100))
socktBuffer.listen(4)

socketMaquinas = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketMaquinas.bind(('', 12000))
socketMaquinas.listen(4)

socktLevantar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktLevantar.bind(('', 12200))
socktLevantar.listen(4)

secktAbaixar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secktAbaixar.bind(('', 12201))
secktAbaixar.listen(4)

t1 = threading.Thread(target=levantarSemaforoLocal)
t2 = threading.Thread(target=abaixarSemaforoLocal)
t3 = threading.Thread(target=startCliente)
t4 = threading.Thread(target=startServer)

print('Maquina A rodando')

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
