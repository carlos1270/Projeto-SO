import time
import socket
import threading

class ThreadLevantarSemaforo(threading.Thread):
    def __init__(self, connection, addr):
        threading.Thread.__init__(self)
        self.connection = connection
        self.addr = addr

    def run(self):
        print("atualizando semaforo")
        atualizar = self.connection.recv(1024)
        print(atualizar)
        
        if (int(atualizar.decode())):
            print("1")
            semaforo.acquire()
            
        self.connection.send("1".encode())
        self.connection.close()

class ThreadAbaixarSemaforo(threading.Thread):
    def __init__(self, connection, addr):
        threading.Thread.__init__(self)
        self.connection = connection
        self.addr = addr

    def run(self):
        print("atualizando semaforo")
        atualizar = self.connection.recv(1024)
        print(atualizar)
        if (not(int(atualizar.decode()))):
            print("0")
            semaforo.release()
            
        self.connection.send("1".encode())
        self.connection.close()       

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
        
global semaforo, socktLevantar, secktAbaixar

semaforo = threading.Semaphore()
socktLevantar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socktLevantar.bind(('', 12200))
socktLevantar.listen(2)

secktAbaixar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secktAbaixar.bind(('', 12201))
secktAbaixar.listen(2)

t1 = threading.Thread(target=levantarSemaforoLocal)
t2 = threading.Thread(target=abaixarSemaforoLocal)
t1.start()
t2.start()
print("Maquina rodando")
t1.join()
t2.join()


