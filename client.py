#CPE400 Project
#Group: Brendan Aguiar, Nicholas Ang
#UDP-based reliable data transfer algorithm

import socket
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 12345
address = (host, port)

if __name__ == "__main__":
	print("Please input file name")
	fileName = input()
	client.connect(address)
	client.send(fileName.encode('ascii'))
	msg = client.recv(1024).decode('ascii')
	print("[SERVER RESPONSE]: {}".format(msg))
