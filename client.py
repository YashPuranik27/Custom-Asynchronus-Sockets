import socket
import sys
import time
import random
import threading


def client():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('Socket open error: {} \n'.format(err))
        exit()

    localhost_addr = socket.gethostbyname(socket.gethostname())

    # Connect to the server
    server_socket.connect((localhost_addr, 50020))
    end = 'endFile'
    # Read lines from the text file
    with open('PROJ2-HNS.txt', 'r') as file:
        domainNames = [line.strip() for line in file]
    queries = []
    # Send each line to the server
    for domains in domainNames:
        data = domains.strip()  # remove leading/trailing whitespaces
        server_socket.send(data.encode())
        response = server_socket.recv(4096).decode().strip()
        queries.append(response)

    server_socket.send(end.encode('utf-8'))

    with open('RESOLVED.txt', 'w') as solution:
        for domain in queries:
            solution.write(str(domain) + '\n')


if __name__ == "__main__":
    time.sleep(random.random() * 5)
    t1 = threading.Thread(name='client', target=client)
    t1.start()

    time.sleep(8)
    print("Done.")
