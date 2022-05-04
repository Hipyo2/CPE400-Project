#CPE400 Project
#Group: Brendan Aguiar, Nicholas Ang
#UDP-based reliable data transfer algorithm

#Python Libraries
from copyreg import add_extension
import socket
import os
import time
import hashlib
import pickle

#General socket setup - host, ports, addresses
#Sockets created for TCP and UDP
tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#SOCK_STREAM establishes TCP protocol
udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#SOCK_DGRAM establishes UDP protocol
host = socket.gethostbyname('localhost')
port = 12345
address = (host, port)
packetNum = 0

#UDP client connection - Transmits reliable data
def startDataChannel(contents):
	established = True
	size = 0
	sequenceNumber = 0
	previousSequence = 0
	contentIndex = 0
	while established and contentIndex <= packetNum:
		#Create packet with checksum, content checksum, sequence number, and file segment contents
		checksum = hashlib.sha256(str(sequenceNumber).encode('ascii')).hexdigest()
		contentChecksum = hashlib.sha256((contents[contentIndex]).encode('ascii')).hexdigest()
		packet = pickle.dumps([sequenceNumber, checksum, contentChecksum, contents[contentIndex]])
		try:
			#send packet
			udpClient.sendto(bytearray(packet), address)
			previousSequence = sequenceNumber
			#Set timeout for ack message
			udpClient.settimeout(0.9)
			
			packetRecv, addr = udpClient.recvfrom(1024)
			message = pickle.loads(packetRecv)
			

			#check if ack number is the same as the current sequence
			if sequenceNumber != message[0]:
				sequenceNumber = message[0]
			else:
				print("[SERVER RESPONSE]: Retransmitting")
			#print current ack number
			print("[SERVER RESPONSE]: Ack Number:{}".format(sequenceNumber))
			#packet number is set to the packet number in message

			contentIndex = message[1]
			#Check if file has been completely sent and no packets remain
			if fileSize == sequenceNumber:
				established = False
				break
		#If socket times out, resend packet
		except socket.timeout:
			sequenceNumber = previousSequence
	#After file is completely sent, send close connection delimiter and checksum for final sequence number to server
	closeConnection = '@'
	checksum = hashlib.sha256(str(sequenceNumber).encode('ascii')).hexdigest()
	contentChecksum = hashlib.sha256(('@').encode('ascii')).hexdigest()
	packet = pickle.dumps([sequenceNumber, checksum, contentChecksum,closeConnection])
	udpClient.sendto(bytearray(packet), address)

#TCP client connection
def startControlChannel(fileName, fileSize):
	tcpClient.connect(address)
	
	#Send file name and receive ack for file name
	tcpClient.send(fileName.encode('ascii'))
	recmsg1 = tcpClient.recv(1024).decode('ascii')
	print("[SERVER RESPONSE]: {}".format(recmsg1))
	
	#Send file size and receive ack for file size
	tcpClient.send(fileSize.encode('ascii'))
	recmsg2 = tcpClient.recv(1024).decode('ascii')
	print("[SERVER RESPONSE]: {}".format(recmsg2))
	
	#Send close connection delimiter
	closeConnection = '@'
	tcpClient.send(closeConnection.encode('ascii'))


#Main Function
if __name__ == "__main__":
	#Get user-inputted text file
	print("Please input file name")
	fileName = input()
	file = open(fileName, 'r')#open for reading
	
	#Break file up into 200 Byte segments
	contents = []
	while True:
		data = file.read(200)
		contents.append(data)
		if data == '':
			break
		
	#Start sending packet metadata
	packetNum = len(contents)
	global fileSize 
	fileSize = os.stat(fileName).st_size
	startControlChannel(fileName, str(fileSize))
	
	#wait 1 second before starting UDP data channel and transfer
	time.sleep(1)
	startDataChannel(contents)
