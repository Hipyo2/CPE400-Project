#CPE400 Project
#Group: Brendan Aguiar, Nicholas Ang
#UDP-based reliable data transfer algorithm

from copyreg import add_extension
import socket
import os
import time
import hashlib
import pickle


tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#SOCK_STREAM establishes TCP protocol
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#SOCK_DGRAM establishes UDP protocol
host = socket.gethostbyname('localhost')
port = 12345
address = (host, port)

def startDataChannel(contents):
	established = True
	size = 0
	sequenceNumber = 0
	while established:
		checksum = hashlib.sha256(str(sequenceNumber).encode('ascii')).hexdigest()
		packet = pickle.dumps([sequenceNumber, checksum, contents])
		udpClient.sendto(bytearray(packet), address)
		size = int(udpClient.recvfrom(1024)[0].decode('ascii'))
		sequenceNumber = sequenceNumber + size
		b_arr = bytearray(contents.encode('ascii'))
		print("[SERVER RESPONSE]: {}".format(size))
		i = 0
		while i < size:
			b_arr.pop(0)
			i = i + 1
		contents = b_arr.decode('ascii')
		if size == 0:
			established = False
	closeConnection = '@'
	packet = pickle.dumps([sequenceNumber, checksum, closeConnection])
	#udpClient.sendto(closeConnection.encode('ascii'), address)
	udpClient.sendto(bytearray(packet), address)


def startControlChannel(fileName, fileSize):
	tcpClient.connect(address)
	tcpClient.send(fileName.encode('ascii'))
	recmsg1 = tcpClient.recv(1024).decode('ascii')
	print("[SERVER RESPONSE]: {}".format(recmsg1))
	tcpClient.send(fileSize.encode('ascii'))
	recmsg2 = tcpClient.recv(1024).decode('ascii')
	print("[SERVER RESPONSE]: {}".format(recmsg2))
	closeConnection = '@'
	tcpClient.send(closeConnection.encode('ascii'))



if __name__ == "__main__":
	print("Please input file name")
	fileName = input()
	file = open(fileName, 'r')#open for reading
	contents = file.read()
	fileSize = len(contents)
	startControlChannel(fileName, str(fileSize))
	time.sleep(1)
	startDataChannel(contents)
