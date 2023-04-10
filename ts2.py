# DNS Server 2

import threading
import time
import random
import os
import socket
import sys


# Read the DNS table from the input file PROJ2-DNSTS2.txt
def ts2_server():
    IPADDRESSDNSTS2 = {}
    DNSRECORDTYPETS2 = {}

    with open("PROJ2-DNSTS2.txt", 'r') as file:

        # PROJ2-DNSTS2.txt contains a list of domain names, IP addresses, and record types
        for line in file:
            line = line.strip('\n').split(' ')
            IPADDRESSDNSTS2[line[0]] = line[1]
            DNSRECORDTYPETS2[line[0]] = line[2]

    # Create a socket for the TS2 server
    try:
        ts2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS2]: Server socket created")
    except socket.error as err:
        print('[TS2] socket open error: {}\n'.format(err))
        exit()

    ts2_socket.bind(('', 50051))
    ts2_socket.listen(1)
    host = socket.gethostname()
    end = 'endFile'
    print("[TS2]: Server host: {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS2]: Server IP address: {}".format(localhost_ip))
    ls_socketid, ls_address = ts2_socket.accept()
    print("[TS2]: Got a connection request from a client at {}".format(ls_address))
    # For each query received from the LS, each TS server does a lookup of the domain name in its DNS table,
    # and if there is a match, sends a DNS response with the following string: DomainName IPaddress A IN
    while True:

        if ls_socketid.fileno() == -1:
            sys.exit(0)
        data = ls_socketid.recv(4096).decode('utf-8')
        if data == end:
            break
        else:
            for domains in IPADDRESSDNSTS2:
                if domains.lower() == data.lower():
                    response = domains + " " + IPADDRESSDNSTS2[domains] + " " + DNSRECORDTYPETS2[domains] + " " + "IN"
                    ls_socketid.send(response.encode('utf-8'))
                    break
                else:
                    continue

            # close socket
    ts2_socket.close()
    exit()


if __name__ == "__main__":
    time.sleep(random.random() * 5)
    t1 = threading.Thread(name='ts2_server', target=ts2_server)
    t1.start()

    time.sleep(5)
    print("Done.")
