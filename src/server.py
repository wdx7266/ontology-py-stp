#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import socket, AF_INET, SOCK_STREAM
from os import path
import ssl

KEYFILE = path.abspath(
    path.join(path.dirname("__file__"), "pem", "server_key.pem"))  # Private key of the server
CERTFILE = path.abspath(
    path.join(path.dirname("__file__"), "pem", "server_cert.pem"))  # Server certificate (given to client)

print(KEYFILE)
print(CERTFILE)


def echo_client(s):
    while True:
        data = s.recv(8192)
        if data == b'':
            break
        s.send(data)
    s.close()
    print('Connection closed')


def echo_server(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(1)

    # Wrap with an SSL layer requiring client certs
    s_ssl = ssl.wrap_socket(s,
                            keyfile=KEYFILE,
                            certfile=CERTFILE,
                            server_side=True
                            )
    # Wait for connections
    while True:
        try:
            c, a = s_ssl.accept()
            print('Got connection', c, a)
            echo_client(c)
        except Exception as e:
            print('{}: {}'.format(e.__class__.__name__, e))


if __name__ == '__main__':
    echo_server(('', 20000))
