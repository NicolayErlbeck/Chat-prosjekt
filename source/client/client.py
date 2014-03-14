'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import ReceiveMessageWorker
from threading import Thread
import time

class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.connection.connect((host, port))
        
		#self.send('Hello')
        #received_data = self.connection.recv(1024).strip()
        #print 'Received from server: ' + received_data
        #self.connection.close()

    def message_received(self, message, connection):
		if len(message) != 0:
			print message
        #pass

    def connection_closed(self, connection):
        pass

    def send(self, data):
        self.connection.sendall(data)

    def force_disconnect(self):
		self.connection.close()
        #pass

		
if __name__ == "__main__":
    client = Client()
    client.start('localhost', 9999)
    msgWorkerThread = ReceiveMessageWorker(client,client.connection) #call as ReceiveMessageWorker(listener,connection)
    msgWorkerThread.start()
    
    #testing
    time.sleep(1)
    client.send('Heartbeat: 1')
    time.sleep(1)
    client.send('Heartbeat: 2')
    while 1:
        #get user input etc.
    msgWorkerThread.join()
    client.force_disconnect()
    print "Client disconnected"
    
