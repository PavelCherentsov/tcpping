import socket


def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 10000)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        connection, client_address = sock.accept()
        data = connection.recv(1024)
        if data:
            connection.sendall(data)
