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
packetNum = 0
fileSize = 0

def startDataChannel(contents):
	established = True
	size = 0
	sequenceNumber = 0
	contentIndex = 0
	#for x in contents:
	while established:
		checksum = hashlib.sha256(str(sequenceNumber).encode('ascii')).hexdigest()
		contentChecksum = hashlib.sha256((contents[contentIndex]).encode('ascii')).hexdigest()
		packet = pickle.dumps([sequenceNumber, checksum, contentChecksum, contents[contentIndex]])
		udpClient.sendto(bytearray(packet), address)
		packetRecv, addr = udpClient.recvfrom(1024)
		message = pickle.loads(packetRecv)
		size = message[0]


		sequenceNumber = sequenceNumber + size
		#b_arr = bytearray((contents[contentIndex]).encode('ascii'))
		print("[SERVER RESPONSE]: {}".format(size))
		i = 0
		#while i < size:
		#	b_arr.pop(0)
		#	i = i + 1
		#contents[contentIndex] = b_arr.decode('ascii')
		contentIndex = message[1]
		#contentIndex = contentIndex + 1
		if fileSize == sequenceNumber and contentIndex == packetNum:
			established = False
	closeConnection = '@'
	checksum = hashlib.sha256(str(sequenceNumber).encode('ascii')).hexdigest()
	contentChecksum = hashlib.sha256(('@').encode('ascii')).hexdigest()
	packet = pickle.dumps([sequenceNumber, checksum, contentChecksum,closeConnection])
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
	contents = []
	while True:
		data = file.read(200)
		contents.append(data)
		if data == '':
			break
		
	packetNum = len(contents)
	fileSize = os.stat(fileName).st_size
	startControlChannel(fileName, str(fileSize))
	time.sleep(1)
	startDataChannel(contents)
