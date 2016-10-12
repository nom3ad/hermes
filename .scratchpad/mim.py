import socket
import select
import time
import sys

inlist = []
channel = {}
delay = 0.0001

clientEndpoint = ('',27000)
tgtEndPoint = ('',28000)
clientoppsock = None
targetoppsock = None
if __name__ == "__main__":

	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	client_sock.bind(clientEndpoint)
	client_sock.listen(1)
	print "listening client at ",clientEndpoint

	target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	target_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	target_sock.bind(tgtEndPoint)
	target_sock.listen(1)

	print "listening TARGET at ",tgtEndPoint

	inlist.append(client_sock)
	inlist.append(target_sock)

	while True:
		time.sleep(delay)
		inputready, outputready, exceptready = select.select(inlist,
														 [], [])
		for s in inputready:

			if s == client_sock:
				clientoppsock, clientoppaddr = client_sock.accept()
				print "CLIENT CONNECTED " ,clientoppaddr
				inlist.append(clientoppsock)

			if s == target_sock:
				targetoppsock, targetoppaddr = target_sock.accept()
				print "TGT CONNECTED  ",targetoppaddr
				inlist.append(targetoppsock)

			if s == clientoppsock:
				data = clientoppsock.recv(1024)
				if len(data) == 0:
					print "clinet diconnected"
					clientoppsock.close
					inlist.remove(clientoppsock)
				else:
					print "----------client data -----\n",data
					if targetoppsock != None:targetoppsock.send(data) 

			if s == targetoppsock:
				data = targetoppsock.recv(1024)
				if len(data) == 0:
					print "taget diconnected"
					targetoppsock.close
					inlist.remove(targetoppsock)
				else:
					if clientoppsock != None: clientoppsock.send(data) 


