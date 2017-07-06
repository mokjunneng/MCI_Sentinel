import RPi.GPIO as GPIO
import time
import socket
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT,SPI_DEVICE))
GPIO.setmode(BCM)

#create a socket object
s = socket.socket()

#get local machine name
host = socket.gethostname()

#reserve a port for service
port = 555

s.bind((host,port))
print 'Socket binding complete'

s.listen(10)
print 'Socket is now listening'

while True:
    IR_value = mcp.read_adc(0)
    if IR_value < 1020:
        client, address = s.accept()
        print 'getting connection from', address
        code = client.recv(4096)
        print code 
        client.sendall('Binary codes received')