import socket
import select
import time
import sys

delay = 0.0001

if __name__ == "__main__":

	localEndPoint = ('localhost',80)
	mimEndPoint = ('localhost',28000)

	mim_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	lcl_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	mim_sock.connect(mimEndPoint)
	print "mim socket connected"
	lcl_sock.connect(localEndPoint)
	print "loc socket connected"

	while True:
		time.sleep(delay)
		inputready, outputready, exceptready = select.select([mim_sock,lcl_sock], [], [])
		
		for s in inputready:
			if s == lcl_sock:
				data = s.recv(1024)
				#print "\n\nlclData\t:\t\n\n",data
				mim_sock.send(data)
			if s == mim_sock:
				data = s.recv(1024)
				#print "\n\nmimData\t:\t\n\n",data
				lcl_sock.send(data)