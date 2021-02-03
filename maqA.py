import socket
import threading
import ConverterEReceberMatriz as cnvMatriz
import multiMatrizes
import cliente

global nucleos, maqA, maqB, maqC
nucleos = [[False], [False, False], [False, False, False]]

maqA = '192.168.56.1'
maqB = '192.168.56.102'
maqC = '192.168.56.103'

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
    semaforo.acquire()
    nucleos[maquina-1][nucleo-1] = liberado
    semaforo.release()

def processarMatriz(matrizes):
    print("Processando uma matriz")
    matrizesConvertidas = cnvMatriz.dividirEntrada(matrizes)
    if(multiMatrizes.mult_valida(matrizesConvertidas[0], matrizesConvertidas[1])): 
       return str(multiMatrizes.mult_mat(matrizesConvertidas[0], matrizesConvertidas[1]))
    else:
        return("Multiplicação impossível")
    
def controlarBufferNucleos(maquina, nucleo, matrizes):
    atualizarNucleoLocal(True, maquina, nucleo)
    atualizarNucleo(maqB, 12000, True, maquina, nucleo)
    atualizarNucleo(maqC, 12000, True, maquina, nucleo)
    matriz = processarMatriz(matrizes)
    atualizarNucleoLocal(False, maquina, nucleo)
    atualizarNucleo(maqB, 12000, False, maquina, nucleo)
    atualizarNucleo(maqC, 12000, False, maquina, nucleo)
    print("Matriz processada")
    return matriz

def redirecionarMatrizes(maquina, matrizes):
    thread = cliente.ClienteThread(maquina, 12100)
    thread.socket.send(matrizes.encode())
    resposta = thread.socket.recv(1024)
    return resposta.decode()
    
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
