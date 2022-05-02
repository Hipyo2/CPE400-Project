#CPE400 Project
#Group: Brendan Aguiar, Nicholas Ang
#UDP-based reliable data transfer algorithm

import socket
import os
import pickle 
import hashlib
import time
import random

host = socket.gethostbyname('localhost')
port = 12345
address = (host, port)
fileName = None
fileSize = None
packetNum = 0

class udp_server_connection():
	server = None
	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	def serverConnectUDP(self):
		self.server.bind(address)
		print(f"[NEW CONNECTION] UDP connected.")
		packetNum = 0
		sequenceNumber = 0
		established = True
		while established: 
			try:
				packet, addr = self.server.recvfrom(1024)#receives up to 1024 Bytes
				if random.randint(0,3) != 0:
					message = pickle.loads(packet)
					
					clientChecksum = message[1]
					clientChecksum2 = message[2]
					#print(clientChecksum)
					serverChecksum = hashlib.sha256(str(message[0]).encode('ascii')).hexdigest()
					serverChecksum2 = hashlib.sha256(str(message[3]).encode('ascii')).hexdigest()

					#serverChecksum = packet[0]
					#print(serverChecksum)
					if clientChecksum == serverChecksum and clientChecksum2 == serverChecksum2:
						packet = message[3]
						if packet != '@':
							print("{}".format(packet), end="")
							#msg = str(len(packet))
							packetNum = packetNum + 1
							sequenceNumber = sequenceNumber + len(packet)
							msg = pickle.dumps([sequenceNumber, packetNum])
							
							self.server.sendto(bytearray(msg), addr)
							
						else:
							#print(message[0])
							#print(fileSize)
							if str(message[0]) == fileSize:
								print("Closing server")
								established = False
							else:
								print("Error in downloading file")
								established = False
					else:
						#msg = str(packetNum)
						msg = pickle.dumps([sequenceNumber, packetNum])
						self.server.sendto(bytearray(msg), addr)
						#print("Retransmitting")
				else:
					#print("Lost Packet")
					msg = pickle.dumps([sequenceNumber, packetNum])
					self.server.sendto(bytearray(msg), addr)
					#print("Retransmitting")
			except socket.timeout:
				msg = pickle.dumps([sequenceNumber, packetNum])
				self.server.sendto(bytearray(msg), addr)
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
		
		packet = conn.recv(1024).decode('ascii')#receives up to 1024 Bytes
		fileName = str(packet)
		print("Packet: {}".format(fileName))
		conn.send("Packet received.".encode('ascii'))
		
		packet = conn.recv(1024).decode('ascii')#receives up to 1024 Bytes
		global fileSize
		fileSize = str(packet)
		print("Packet: {}".format(fileSize))
		conn.send("Packet received.".encode('ascii'))
		
		packet = conn.recv(1024).decode('ascii')#receives up to 1024 Bytes
		if packet == '@':
			print("Closing server")
			established = False
		conn.close()
		



if __name__ == "__main__":
	tcpServer = tcp_server_connection()
	tcpServer.serverConnectTCP()
	udpServer = udp_server_connection()
	udpServer.serverConnectUDP()
