'''
KTN-project 2013 / 2014
Very simple server implementation that should serve as a basis
for implementing the chat server
'''
import SocketServer
import json
import re
#from MessageWorker import ReceiveMessageWorker
'''
The RequestHandler class for our server.

It is instantiated once per connection to the server, and must
override the handle() method to implement communication to the
client.
'''

onlineClients = {}

class ClientHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # Get a reference to the socket object
        self.connection = self.request
        # Get the remote ip adress of the socket
        self.ip = self.client_address[0]
        # Get the remote port number of the socket
        self.port = self.client_address[1]
        print 'Client connected @' + self.ip + ':' + str(self.port)
        # Wait for data from the client
        while True:
            data = self.connection.recv(1024).strip()
            # Check if the data exists
            # (recv could have returned due to a disconnect)
            if data:
                print data
                self.requestHandler(self,data)
                            
                                # Return the string in uppercase
                                # self.connection.sendall(data.upper())
            else:
                print 'Client disconnected!'
                break
    def requestHandler(self,data):
        try:
            dict = json.loads(data)
            if 'request' in dict:
                request = dict['request']
                if request in requestTypes:
                    requestTypes[request](self,dict)
        except:
            print 'Invalid request'
                            
        def handleLoginRequest(self,dict):
                if 'username' in dict:
                        username = dict['username']
                        valUser = self.validUsername(username)
                        if valUser == 1:
                                data = json.dumps({'response': 'login', 'username': username, 'messages': messages})
                                onlineClients[username] = self.connection
                elif valUser == 0:
                        data = json.dumps({'response': 'login', 'error': 'Invalid username!', 'username': username})
                else:
                        data = json.dumps({'response': 'login', 'error': 'Name already taken!', 'username': username})
                self.connection.sendall(data)

        def handleMessageRequest(self,dict):
            if self.checkIfLoggedIn(dict) != '$NotInOnlineList$':
                    if 'message' in dict:
                        msg= json.dumps({'response': 'message', 'message': dict['message']})
                        for conn in onlineClients.values():
                            conn.sendall(msg)
            else:
                    msg= json.dumps({'response': 'message', 'error': 'You are not logged in!'})
                    self.connection.sendall(msg)
            
        def checkIfLoggedIn(self):
            for k, v in onlineClients:
                if self.connection == v:
                    return k
            return '$NotInOnlineList$'    

        def handleLogoutRequest(self,dict):
            user = self.checkIfLoggedIn()
            if user != '$NotInOnlineList$':
                    msg = json.dumps({'response': 'logout', 'username': user})
                    del onlineClients[user]
            else:
                    msg = json.dumps({'response': 'logout','error': 'Not logged in!', 'username': user})
            self.connection.sendall(msg)

    
        

        def validUsername(self,username):
            if re.match(r'\w+$', username):
                    # valid username! see: http://docs.python.org/2/library/re.html#search-vs-match [ctrl] + f: When the LOCALE and UNICODE flags are not specified, matches any alphanumeric character and the underscore;
                            if username not in onlineClients:
                                    #username not taken, return true!
                                    return 1
            else:
                                    #username taken
                    return -1
            return 0 #username contains invalid characters


'''
This will make all Request handlers being called in its own thread.
Very important, otherwise only one client will be served at a time
'''


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    #HOST = '78.91.7.255'
    #HOST = 'localhost'
    HOST  = '78.91.38.244'
    PORT = 2224
    print("Hei")
    # Create the server, binding to localhost on port 9999
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

requestTypes = {     #Holds the different requests a client can send
           'login'     : handleLoginRequest,
       'message'     : handleMessageRequest,
       'logout'    : handleLogoutRequest,
 }


