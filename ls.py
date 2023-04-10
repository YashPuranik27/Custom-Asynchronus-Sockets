import threading
import time
import random
import socket
import sys
import select


def server():
    try:
        # Create a socket for ls
        ls_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Server socket created")
    except socket.error as err:
        print('[LS] socket open error: {}\n'.format(err))
        exit()

    ls_socket.bind(('', 50020))
    ls_socket.listen(1)
    host = socket.gethostname()
    print("[LS]: Server host: {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[LS]: Server IP address: {}".format(localhost_ip))

    # Constants
    TIMEOUT = 5
    BUFSIZE = 4096

    # Create two sockets for the two TS servers
    try:
        ts1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: TS1 server socket created")
    except ConnectionRefusedError:
        print('[LS] TS1 socket open error:\n')
        exit()
    try:
        ts2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: TS2 server socket created")
    except ConnectionRefusedError:
        print('[LS] TS2 socket open error:\n')
        exit()

    port_ts1 = 50054
    port_ts2 = 50051
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # Connect to the two TS servers
    server_binding1 = (localhost_addr, port_ts1)
    server_binding2 = (localhost_addr, port_ts2)
    ts1_socket.connect(server_binding1)
    ts2_socket.connect(server_binding2)

    # Set the sockets to non-blocking mode in ls
    ts1_socket.setblocking(0)
    ts2_socket.setblocking(0)

    client_socketid, client_address = ls_socket.accept()
    print("[LS]: Got a connection request from a client at {}".format(client_address))
    # Receive data from the server
    end = 'endFile'
    while True:
        if client_socketid.fileno() == -1:
            sys.exit(0)

        data = client_socketid.recv(4096).decode('utf-8')

        if data == end:
            ts1_socket.send(end.encode('utf-8'))
            ts2_socket.send(end.encode('utf-8'))
            break

        ts1_socket.send(data.encode('utf-8'))
        ts2_socket.send(data.encode('utf-8'))

        inputs, filler, exceptions = select.select([ts1_socket, ts2_socket], [], [], 5)

        if exceptions:
            sys.exit(1)

        if not inputs:
            response = data + " - TIMED OUT\n"
            client_socketid.send(response.encode('utf-8'))
            continue

        for s in inputs:
            data = s.recv(4096)
            response = data.decode('utf-8')
            client_socketid.send(response.encode('utf-8'))
            break

    ls_socket.close()
    ts1_socket.close()
    ts2_socket.close()
    exit()


if __name__ == "__main__":
    time.sleep(random.random() * 5)
    t1 = threading.Thread(name='server', target=server)
    t1.start()

    time.sleep(10)
    print("Done.")
