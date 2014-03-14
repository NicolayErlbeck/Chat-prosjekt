'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import ReceiveMessageWorker
from threading import Thread
import time
import json

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
            print "Message: " + "\n" + message
        #pass

    def connection_closed(self, connection):
        print "Connection with server is closed"
        #todo: try to reconnect??
        self.loginRequest()
        pass

    def send(self, data):
        self.connection.sendall(data)

    def force_disconnect(self):
        self.connection.close()
        #pass
    
    def loginRequest(self):
        while 1:
            username = raw_input("Type username: ")
            try:
                login = {'request': 'login', 'username': username}
                loginJson = json.dumps(login)
            except:
                print "Invalid username"
                return
            try:
                self.send(loginJson)
                responseJson = self.connection.recv(1024).strip()
            except:
                print "No contact with server"
                self.connection_closed(self.connection)
                return
            try:
                response = json.loads(responseJson)
                print response
            except:
                print "Invalid username"
                return
            break
            
        try:
            if 'error' in response:
                print response['username']
                print response['error']
            else:
                print response['username'] + 'logged in, printing all messages: '
                print response['messages']
        except:
            print "Invalid message received"
            
    def logoutRequest(self):
        logout = {'request': 'logout'}
        logoutJson = json.dumps(logout)
        self.send(logoutJson)
        self.force_disconnect()
            
    def sendMessage(self, data):
        try:
            msg = {'request': 'message', 'message': data}
            msgJson = json.dumps(msg)
        except:
            print "Invalid text"
            return
        try:
            self.send(msgJson)
        except:
            print "No contact with server"
            self.connection_closed(self.connection)
                
            
if __name__ == "__main__":
    client = Client()
    client.start('localhost', 9999)

    client.loginRequest()

    msgWorkerThread = ReceiveMessageWorker(client,client.connection) #call as ReceiveMessageWorker(listener,connection)
    msgWorkerThread.start()
    
    
    
    #testing
    #time.sleep(1)
    #client.send('Heartbeat: 1')
    #time.sleep(1)
    #client.send('Heartbeat: 2')
    while 1:
        #get user input etc.
        msg = raw_input("Type a message: ")
        client.sendMessage(msg)
    msgWorkerThread.join()
    client.force_disconnect()
    print "Client disconnected"
    
