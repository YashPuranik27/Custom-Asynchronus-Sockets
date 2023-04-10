# DNS Server 1

import threading
import time
import random
import os
import socket
import sys


# Read the DNS table from the input file PROJ2-DNSTS2.txt
def ts1_server():
    IPADDRESSDNSTS1 = {}
    DNSRECORDTYPETS1 = {}

    with open("PROJ2-DNSTS1.txt", 'r') as file:

        # PROJ2-DNSTS1.txt contains a list of domain names, IP addresses, and record types
        for line in file:
            line = line.strip('\n').split(' ')
            IPADDRESSDNSTS1[line[0]] = line[1]
            DNSRECORDTYPETS1[line[0]] = line[2]

    # Create a socket for the TS1 server
    try:
        ts1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS1]: Server socket created")
    except socket.error as err:
        print('[TS1] socket open error: {}\n'.format(err))
        exit()

    ts1_socket.bind(('', 50054))
    ts1_socket.listen(1)
    host = socket.gethostname()
    end = 'endFile'
    print("[TS1]: Server host: {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS1]: Server IP address: {}".format(localhost_ip))
    ls_socketid, ls_address = ts1_socket.accept()
    print("[TS1]: Got a connection request from a client at {}".format(ls_address))
    # For each query received from the LS, each TS server does a lookup of the domain name in its DNS table,
    # and if there is a match, sends a DNS response with the following string: DomainName IPaddress A IN
    while True:
        if ls_socketid.fileno() == -1:
            sys.exit(0)
        data = ls_socketid.recv(4096).decode('utf-8')
        if data == end:
            break
        else:
            for domains in IPADDRESSDNSTS1:
                if domains.lower() == data.lower():
                    response = domains + " " + IPADDRESSDNSTS1[domains] + " " + DNSRECORDTYPETS1[domains] + " " + "IN"
                    ls_socketid.send(response.encode('utf-8'))
                    break
                else:
                    continue
    # close socket
    ts1_socket.close()
    exit()


if __name__ == "__main__":
    time.sleep(random.random() * 5)
    t1 = threading.Thread(name='ts1_server', target=ts1_server)
    t1.start()

    time.sleep(5)
    print("Done.")
