import socket
import sys
import thread
import Queue
import threading
import time

class mainServer():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '10.189.130.126'
        self.port = 5555
        self.s.bind((self.host, self.port))
        self.s.listen(10)
        print 'Socket is now listening'
        # self.s.setblocking(0)
        self.q = Queue.LifoQueue(maxsize=1)
        # self.format = struct.Struct('I')

    def main(self):
        while True:
            print 'Looking for connection...'
            self.conn, self.addr = self.s.accept()
            print self.conn
            print 'Connected with ' + self.addr[0] + ':' + str(self.addr[1])
            # thread.start_new_thread(self.sentinelThread, (self.conn,))
            thread = threading.Thread(target=self.sentinelThread, args=(self.conn,))
            thread.daemon = True
            thread.start()
    
        self.s.close()    
    
    # def recvall(self, sock, length):
    #     data = ''
    #     while len(data) < length:
    #         data_recv = sock.recv(length - len(data))
    #         if not data_recv:
    #             raise EOFError('socket closed %d bytes into a %d-byte message')
    #         data += data_recv
    #     return data
    
    # def get(self, sock):
    #     lendata = self.recvall(sock, self.format.size)
    #     (length,) = self.format.unpack(lendata)
    #     return self.recvall(sock, length)

    def sentinelThread(self,conn):
        # self.s.settimeout(0.5)
        print 'Thread created.'
        try:
            length = None
            buffer = ''
            while True:
                data = conn.recv(2)
                print data
                if not data:
                    break
                buffer += data
                while True:
                    if length is None:
                        if ':' not in buffer:
                            break
                        length_str, ignored, buffer = buffer.partition(':')
                        print buffer
                        length = int(length_str)
                        print length
                    
                    if len(buffer) < length:
                        break

                    msg = buffer[:length]
                    print msg
                    buffer = buffer[length:]
                    length = None
                    
                    print msg.isdigit()
                    if msg.isdigit():
                        self.q.put(msg)
                        print 'data in queue'
                    print self.q.qsize()
                    # try:
                    if msg.isalpha():
                        queued_data = self.q.get()
                        print queued_data
                        conn.sendall(queued_data)
                        print 'queued data sent'
                        self.q.task_done()
                # except socket.error:
                #     pass
                    time.sleep(0.1)
            conn.close()
        finally:
            sys.exit()

if __name__=='__main__':
    main = mainServer()
    main.main()


    


