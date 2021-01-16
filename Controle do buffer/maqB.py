import socket

def set_nucleo(semaforo, maquina, nucleo):
    atulizarInformacaoNucleo = True

    serverName = '10.0.0.129'
    serverPort = 12101

    clientSocketBuffer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocketBuffer.connect((serverName, serverPort))

    # enquanto não atualizar repete
    while atulizarInformacaoNucleo:
        clientSocketBuffer.send(str([semaforo, maquina, nucleo]).encode())
        resposta = clientSocketBuffer.recv(1024)

        # checa a resposta de atulizacao
        if (resposta.decode() == 'Atualizado'):
            atulizarInformacaoNucleo = False
            clientSocketBuffer.close()
        else:
            print('Ocupado')
    return 0


# chama a função que atualiza o buffer

for i in range(10000):
    set_nucleo(True, 2, 1)

    
print("Terminou")
