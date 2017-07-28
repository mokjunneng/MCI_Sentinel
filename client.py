import socket, struct, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '10.189.9.224'
PORT = 5555
format = struct.Struct('!s')  # for messages up to 2**32 - 1 in length

def put(sock, message):
    sock.send(format.pack(message))


s.connect((HOST, PORT))
# s.shutdown(socket.SHUT_RD)
put(s, 'Beautiful is better than ugly.')
put(s, 'Explicit is better than implicit.')
put(s, 'Simple is better than complex.')
put(s, '')
s.close()

