import socket, struct, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '10.189.9.224'
PORT = 5555
format = struct.Struct('!s')  # for messages up to 2**32 - 1 in length

def recvall(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message'
                           % (len(data), length))
        data += more
    return data

def get(sock):
    lendata = recvall(sock, format.size)
    (length,) = format.unpack(lendata)
    return recvall(sock, length)



s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
print 'Listening at', s.getsockname()
sc, sockname = s.accept()
print 'Accepted connection from', sockname
sc.shutdown(socket.SHUT_WR)
while True:
    message = get(sc)
    if not message:
        break
    print 'Message says:', repr(message)
sc.close()
s.close()

