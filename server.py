#CPE400 Project
#Group: Brendan Aguiar, Nicholas Ang
#UDP-based reliable data transfer algorithm

#Python Libraries
import socket
import os
import pickle 
import hashlib
import time
import random

#General setup of sockets - host, ports, address
host = socket.gethostbyname('localhost')
port = 12345
address = (host, port)
fileName = None
fileSize = None
packetNum = 0

#UDP Class 
class udp_server_connection():
	server = None
	
	#start UDP server socket
	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
	#Connect server and client
	def serverConnectUDP(self):
		self.server.bind(address)
		print(f"[NEW CONNECTION] UDP connected.")
		packetNum = 0
		ackNumber = 0
		previousAck = 0
		established = True
		while established: 
			#receives up to 1024 Bytes
			packet = None
			packet, addr = self.server.recvfrom(1024)
			
			#simulate packet loss with random values 
			if random.randint(0,3) != 0:
				#packet is loaded into variables
				message = pickle.loads(packet)
				
				clientChecksum = message[1]
				clientChecksum2 = message[2]
				
				#server checksums computed for values to be compared with client checksums
				serverChecksum = hashlib.sha256(str(message[0]).encode('ascii')).hexdigest()
				serverChecksum2 = hashlib.sha256(str(message[3]).encode('ascii')).hexdigest()

				#if checksum succeeds, output contents of message
				if clientChecksum == serverChecksum and clientChecksum2 == serverChecksum2:
					packet = message[3]
					#output packet contents
					if packet != '@':
						print("{}".format(packet), end="")
						#Send to client, ack number and packet number
						previousAck = ackNumber
						packetNum = packetNum + 1
						ackNumber = ackNumber + len(packet)
						msg = pickle.dumps([ackNumber, packetNum])
						self.server.sendto(bytearray(msg), addr)
						

					#check end condition and if file is completely downloaded, output closed server
					else:
						if str(message[0]) == fileSize:
							print("Closing server")
							established = False
							
						else:
							print("Error in downloading file")
							established = False
				#if checksums fails		
				else:
					#Send current ack Number and packet number to request a retransmit for
					msg = pickle.dumps([ackNumber, packetNum])
					self.server.sendto(bytearray(msg), addr)
					
			#Send current ack Number and packet number to request a retransmit for when packet is lost - simulated
			else:
				msg = pickle.dumps([ackNumber, packetNum])
				self.server.sendto(bytearray(msg), addr)

		#Connection Closed
		self.server.close()

#TCP Class
class tcp_server_connection():
	server = None
	#start TCP server socket
	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#Connect TCP server and client
	def serverConnectTCP(self):
		self.server.bind(address)
		self.server.listen(5)
		conn, addr = self.server.accept()
		#Output address of connection
		print(f"[NEW CONNECTION] {addr} connected.")		
		
		#First packet received is file name
		packet = conn.recv(1024).decode('ascii')#receives up to 1024 Bytes
		fileName = str(packet)
		print("Packet: {}".format(fileName))
		conn.send("Packet received.".encode('ascii'))
		
		#Second packet received is file size
		packet = conn.recv(1024).decode('ascii')#receives up to 1024 Bytes
		global fileSize
		fileSize = str(packet)
		print("Packet: {}".format(fileSize))
		conn.send("Packet received.".encode('ascii'))
		
		#Third packet received is the closing delimiter to close server
		packet = conn.recv(1024).decode('ascii')#receives up to 1024 Bytes
		if packet == '@':
			print("Closing server")
			conn.close()
		
#Main Function
if __name__ == "__main__":
	#TCP connection is opened and closed before data from UDP connection is transmitted
	tcpServer = tcp_server_connection()
	tcpServer.serverConnectTCP()
	udpServer = udp_server_connection()
	udpServer.serverConnectUDP()
