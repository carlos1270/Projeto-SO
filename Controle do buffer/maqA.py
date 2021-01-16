import socket
import threading
"""

global nucleos

class thread_maqA(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.socktBuffer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socktBuffer.bind(('', self.port))
        self.socktBuffer.listen(1)
        
    def get_info(informacao):
        mensagem = []
        info = ''
        numeros = [1, 2, 3]
        semaforos = [True, False]
        for i in range(len(informacao)):
            if (informacao[i] != '[' and informacao[i] != ']'):
                info += informacao[i]

        if (info.split(',')[0] == 'True'):
            mensagem.append(True)
        else:
            mensagem.append(False)

        mensagem.append(int(info.split(',')[1]))
        mensagem.append(int(info.split(',')[2]))

        return mensagem

    def run():
        while True:
            connectionSocket, addr = self.socktBuffer.accept()
            informacao = connectionSocket.recv(1024)
            print(informacao)
            # checa se pode entrar na região critica
            if (not(bufferOcupado)):
                # Se poder atualiza que entrou na região critica
                bufferOcupado = True

                #atualiza a informacao
                info = self.get_info(informacao.decode())
                semaforo.acquire()
                nucleos[info[1]-1][info[2]-1] = info[0]
                semaforo.release()
                connectionSocket.send('Atualizado'.encode())

                # Sai da região critica
                bufferOcupado = False
            else:
                # Se tiver ocupado manda a resposta ocupado
                connectionSocket.send('Ocupado'.encode())
            
"""
def get_info(informacao):
        mensagem = []
        info = ''
        for i in range(len(informacao)):
            if (informacao[i] != '[' and informacao[i] != ']'):
                info += informacao[i]

        if (info.split(',')[0] == 'True'):
            mensagem.append(True)
        else:
            mensagem.append(False)

        mensagem.append(int(info.split(',')[1]))
        mensagem.append(int(info.split(',')[2]))

        return mensagem

bufferOcupado = False
serverPortsBuffer = [13000, 14000]
bufferOcupado = False
nucleos = [[False], [False, False], [False, False, False]]

semaforo = threading.Semaphore()

"""
while True:
    threadB = thread_maqA(12100)
"""

socktBuffer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktBuffer.bind(('', 12100))
socktBuffer.listen(1)
print('Maquina A rodando')
while True:
        connectionSocket, addr = socktBuffer.accept()
        informacao = connectionSocket.recv(1024)
        # checa se pode entrar na região critica
        if (not(bufferOcupado)):
                # Se poder atualiza que entrou na região critica
                bufferOcupado = True

                #atualiza a informacao
                info = get_info(informacao.decode())
                nucleos[info[1]-1][info[2]-1] = info[0]
                connectionSocket.send('Atualizado'.encode())
                connectionSocket.close()

                # Sai da região critica
                bufferOcupado = False
        else:
                # Se tiver ocupado manda a resposta ocupado
                connectionSocket.send('Ocupado'.encode())
    
