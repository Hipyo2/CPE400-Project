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
	server = None
	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	def	serverConnectUDP(self):
		self.server.bind(address)
		print(f"[NEW CONNECTION] UDP connected.")
		established = True
		while established: 
			packet, addr = self.server.recvfrom(1024)#receives up to 1024 Bytes
			packet = packet.decode('ascii')
			if packet != '@':
				print("{}".format(packet))
				msg = "received up to " + str(len(packet)) + " bytes"
				self.server.sendto(msg.encode('ascii'), addr)
			else:
				established = False
		self.server.close()
	
class tcp_server_connection():
	server = None
	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def serverConnectTCP(self):
		self.server.bind(address)
		self.server.listen(5)
		conn, addr = self.server.accept()
		print(f"[NEW CONNECTION] {addr} connected.")
		established = True
		while established: 
			packet = conn.recv(1024).decode('ascii')#receives up to 1024 Bytes
			if packet != '@':
				print("Packet: {}".format(packet))
				conn.send("Packet received.".encode('ascii'))
			else:
				established = False

		conn.close()
		



if __name__ == "__main__":
	tcpServer = tcp_server_connection()
	tcpServer.serverConnectTCP()
	udpServer = udp_server_connection()
	udpServer.serverConnectUDP()
	
