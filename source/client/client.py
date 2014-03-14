'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import ReceiveMessageWorker
from threading import Thread
import json

class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(2)

    def start(self, host, port):
        try:
            self.connection.connect((host, port))
        except:
            print "No contact with server, retry"
            #self.start(host, port)

    def message_received(self, message, connection):
        if len(message) != 0:
            print "\nMessage: " + "\n" + message            #to be removed
            try:
                msg = json.loads(message)
                if 'error' in msg:
                    print "\n"+msg['error']
                    self.loginRequest()
                else:
                    print "\nMessage: " + msg['message']
            except:
                print "\nInvalid message received"
                return
            
    def connection_closed(self, connection):
        print "\nConnection with server is closed"
        #todo: try to reconnect??
        self.loginRequest()
        pass

    def send(self, data):
        self.connection.sendall(data)

    def force_disconnect(self):
        self.connection.close()
        self.connection_closed(self.connection)
    
    def loginRequest(self):
        while 1:
            username = raw_input("\nType username: ")
            try:
                login = {'request': 'login', 'username': username}
                loginJson = json.dumps(login)
            except:
                print "\nInvalid username"
                return
            try:
                self.send(loginJson)
                responseJson = self.connection.recv(1024).strip()
            except:
                print "\nNo contact with server"
                self.connection_closed(self.connection)
                return
            try:
                response = json.loads(responseJson)
                print response
            except:
                print "\nInvalid username"
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
        print "Logging out.."
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
    #client.start('localhost', 9999)
    #client.start('78.91.29.196', 9999)
    #client.start('78.91.7.178', 9999)
    client.start('78.91.7.32', 9999)
    client.loginRequest()

    msgWorkerThread = ReceiveMessageWorker(client,client.connection) #call as ReceiveMessageWorker(listener,connection)
    msgWorkerThread.start()

    while 1:
        msg = raw_input("Type a message: ")
        if msg == 'logout':
            client.logoutRequest()
        client.sendMessage(msg)
    msgWorkerThread.join()
    client.force_disconnect()
    print "Client disconnected"
    
