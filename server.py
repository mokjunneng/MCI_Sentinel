import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created.')

host = socket.gethostbyname('DESKTOP-SC09P85')
print (host)
port = 5556

s.bind((host, port))
print('Socket binding complete')

s.listen(10)
print ('Socket is now listening...')

while True:
    client, address = s.accept()
    print ('getting connection from', address)
    code = client.recv(4096)
    print (code)
    client.sendall('Binary codes received')
