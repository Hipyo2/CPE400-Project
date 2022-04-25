#CPE400 Project
#Group: Brendan Aguiar, Nicholas Ang
#UDP-based reliable data transfer algorithm

import socket
import os
import pickle 

host = socket.gethostname()
port = 12345
address = (host, port)
fileName = None
fileSize = None

class udp_server_connection():
	def __init__(self):
		self.server.bind(address)
	#def	
	
class tcp_server_connection():
	server = None
	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def serverConnectTCP(self):
		self.server.bind(address)
		self.server.listen(5)
		while True: 
			conn, addr = self.server.accept()
			print(f"[NEW CONNECTION] {addr} connected.")
			fileName = conn.recv(1024).decode('ascii')
			print("File Name: {}".format(fileName))
			conn.send("Filename received.".encode('ascii'))
			print("Disconnected")
			conn.close()



if __name__ == "__main__":
	tcpServer = tcp_server_connection()
	tcpServer.serverConnectTCP()
	
	
