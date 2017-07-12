import RPi.GPIO as GPIO
import time
import socket
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
# from IRsignals import decodeIR

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT,SPI_DEVICE))
GPIO.setmode(GPIO.BCM)

#create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = socket.gethostname()

#reserve a port for service
port = 5556

s.bind((host,port))
print 'Socket binding complete'

s.listen(1)
print 'Socket is now listening'

health = 10
while True:
    # time.sleep(0.1)
    IR_value = mcp.read_adc(0)
    if IR_value < 1020:

        client, address = s.accept()
        print 'getting connection from', address
        code = client.recv(7)
        print code
        if not code:
            break
        client.close()

        player_no = int(code[:3], 2)
        shot = int(code[3:], 2)
        damage = 0
        
        if shot == 1:
            damage = 1
            health -= damage
            print health
        elif shot == 2:
            damage = 3
            health -= damage
            print health
        
        time.sleep(0.1)

# while True:
    
#     client, address = s.accept()
    
#     value = 1

#     while value:
#         value = mcp.read_adc(0)
#         if value > 1020:
#             value = 1
#         else:
#             value = 0

#     pulse_start = time.time()

#     signals = []

#     numOnes = 0
    
#     prev_value = 0

#     while True:
        
#         if value != prev_value:
#             pulse_end = time.time()
#             pulse_duration = (pulse_end - pulse_start)*1000000
#             pulse_start = pulse_end
#             signals.append((prev_value,pulse_duration))

#         if value:
#             numOnes = numOnes + 1
#         else:
#             numOnes = 0
        
#         if numOnes > 10000:
#             break

#         prev_value = value

#         value = mcp.read_adc(0)
#         if value > 1020:
#             value = int(1)
#         else:
#             value = int(0)

#     for (val, pulse) in signals:
#         print(val,pulse)

#     print("Size of array is" + str(len(signals)))

#     if len(signals) > 1:
        
        
#         print 'getting connection from', address
#         code = client.recv(7)
#         print code
#         if not code:
#             break
#         client.close()

#         player_no = int(code[:3], 2)
#         shot = int(code[3:], 2)
#         damage = 0
        
#         if shot == 1:
#             damage = 1
#             health -= damage
#             print health
#         elif shot == 2:
#             damage = 3
#             health -= damage
#             print health
        


            



