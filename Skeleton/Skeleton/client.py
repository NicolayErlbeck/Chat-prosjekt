'''
KTN-project 2013 / 2014
'''
import socket


class Client(object):

    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        self.connection.connect((host, port))
        self.send('Hello')
        received_data = self.connection.recv(1024).strip()
        print 'Received from server: ' + received_data
        self.connection.close()

    def message_received(self, message, connection):
        pass

    def connection_closed(self, connection):
        pass

    def send(self, data):
        self.connection.sendall(data)

    def force_disconnect(self):
        pass


if __name__ == "__main__":
    client = Client()
<<<<<<< HEAD
    client.start('78.91.38.244', 9999)
=======
    client.start('78.91.7.178', 1212)
#'78.91.7.178'
>>>>>>> f14af58c2b59c5291b7c27c6c75357c8fad05c2a
