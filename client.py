import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 5555                # Reserve a port for your service.

s.connect((host, port))
code = '10010010'
s.sendall(code)
reply = s.recv(4096)
print reply
s.close    