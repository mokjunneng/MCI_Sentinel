import RPi.GPIO as GPIO
import time
import socket
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import threading
# from IRsignals import decodeIR
from luma.core.interface.serial import spi,noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, SINCLAIR_FONT, LCD_FONT

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT,SPI_DEVICE))
GPIO.setmode(GPIO.BCM)

#create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = socket.gethostname()

#reserve a port for service
port = 5555

s.bind((host,port))
print 'Socket binding complete'

s.listen(1)
print 'Socket is now listening'
health = 8

class life(threading.Thread):
    def __init__(self):
        super(life, self).__init__()
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial)
        self.daemon = True
        self.event = threading.Event()
    
    def run(self):
        while not self.event.is_set():
            self.health_display()
            print 'displaying health'
            self.event.wait(0.01)

    def health_display(self):
        
        global health

        if health == 0:
            msg = "Game Over"
            show_message(self.device, msg, fill='white', font=CP437_FONT, scroll_delay=0.08)
        else:
            with canvas(self.device) as draw:
                health_bar = draw.rectangle([0,0, 1, health-1], fill='white')

life = life()
# life.start()


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
            # life.event.set()
            # life.event.clear()

        elif shot == 2:
            damage = 3
            health -= damage
            print health
            # life.event.set()
            # life.event.clear()
        
        time.sleep(0.1)


        
        
        