'''
KTN-project 2013 / 2014
'''
import socket
from MessageWorker import ReceiveMessageWorker
from threading import Thread
import json
import time
import sys

loginTimeOut = 60
SERVER = 'localhost'
PORT = 9999

class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(2)

    def start(self, host, port):
        try:
            self.connection.connect((host, port))
        except:
            print "Can not connect to server.. Please try again later"
            terminate()
            #self.start(host, port)

    def message_received(self, message, connection):
        if len(message) != 0:
            #print "\nMessage: " + "\n" + message            #to be removed
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
            
    def connection_closed(self):
        print "\nConnection with server is closed"
        #how to restart thread?
        msg = raw_input("Try to reconnect (if not program will close)? (yes/no): ")
        if msg == 'yes':
            print "Trying to reconnect, please be patient..."
            self.force_disconnect()
            time.sleep(5)
            self.start(SERVER, PORT)
            self.loginRequest()
            msgWorkerThread.start()
        else:
            terminate()
        pass
    
    def send(self, data):
        self.connection.sendall(data)

    def force_disconnect(self):
        self.connection.close()
        #self.connection_closed(self.connection)
    
    def loginRequest(self):
        while 1:
            username = raw_input("\nType username: ")
            try:
                login = {'request': 'login', 'username': username}
                loginJson = json.dumps(login)
                test = json.loads(loginJson)
                
                #print test['username']
                #print test['request']
                #print loginJson
            except:
                print "\nInvalid username"
                return
            try:
                self.send(loginJson)
                responseJson = self.connection.recv(1024).strip()
                time_start = time.time()
                while len(responseJson) == 0:
                    responseJson = self.connection.recv(1024).strip()
                    diff = int(time.time() - time_start)
                    if diff%60 >= loginTimeOut:
                        print "Timeout"
                        raise Exception()
                print responseJson
            except:
                print "\nNo contact with server"
                self.connection_closed()
                return
            try:
                response = json.loads(responseJson)
                
            except:
                print "\nInvalid response from server"
            break
        try:
            if 'error' in response:
                if 'username' in response:
                    print response['username']
                print response['error']
            else:
                print response['username'] + ' logged in, printing all messages: '
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
            print "Msg sent"
        except:
            print "No contact when sending msg to server"
            self.connection_closed()

def terminate():
    print "Closing program.."
    sys.exit()                
            
if __name__ == "__main__":
    print "Welcome to The KTN-chat!"
    client = Client()
    #client.start('localhost', 9999)
    client.start(SERVER, PORT)
    #client.start('78.91.7.178', 9999)
    #client.start('78.91.7.32', 9999)
    client.loginRequest()

    print "Type in a message followed by enter to send,"
    print "please type \'logout\' to log out"
    
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


