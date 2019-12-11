import socket
def crearServer(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()

    server.bind((host, int(port)))
    print('Conectado a: ' + host + ", PORT : " + str(port))
    return server

def connect(server):
    server.listen(5)
    conn, addr = server.accept()
    print("Conectado, IP: " + str(addr[0]) + ", PORT: " + str(addr[1]) + "\n")
    return conn

def receiveMsg(connection):
    while True:
        bits = connection.recv(1204)
        if not bits:
            break
        return bits.decode()

def envMsg(connection, message):
    connection.sendall(str.encode(message))
    print("Mensaje enviado.\n" )

def cerrar(connection):
    print("Cerrando...  ", connection.getsockname())
    connection.close()
    print("Conección cerrada. ")

def display(message):
    print(message)

def exit():
    exit()

