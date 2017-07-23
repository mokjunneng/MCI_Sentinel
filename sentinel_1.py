import RPi.GPIO as GPIO
import time
import socket
from threading import Thread
import threading

# import LED display modules
from luma.core.interface.serial import spi,noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, SINCLAIR_FONT, LCD_FONT

#import IR receiver modules
# import Adafruit_GPIO.SPI as SPI
# import Adafruit_MCP3008

#Pin Assignments
IR_emitter = 4
laser = 23

#setup IR receiver
# SPI_PORT = 0
# SPI_DEVICE = 1
# mcp = Adafruit_MCP3008(spi = SPI.SpiDev(SPI_PORT,SPI_DEVICE))

#GPIO Pins Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_emitter, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(laser, GPIO.OUT, initial = GPIO.LOW)

#setup global variables
ammo = 8
health = 8

        
#laser and emitter output class
class emitter():
    def __init__(self, player):
        self._player = player
        self._team_code = "{0:03b}".format(int(player))
        self.emitter = 4
        self.laser = 23
        self.shotNo = 1
        # self.ir = pyslinger.IR(self._gpio_pin, self._protocol, self._protocol_config)

    def normalShot(self):
        self.IRcode = self._team_code + "{0:04b}".format(self.shotNo) 
        self.IRoutput()
        # self.laserOutput()

    def chargedShot(self):
        self.IRcode = self._team_code + "{0:04b}".format(2)
        self.IRoutput()
        # self.laserOutput2()

    def IRoutput(self):
        global ammo
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._host = socket.gethostname()
        self._host = socket.gethostname()
        self._port = 5555
        GPIO.output(self.emitter, GPIO.HIGH)
        GPIO.output(self.laser, GPIO.HIGH)
        if (self.shotNo == 2) and (ammo < 2):
            print 'insufficient power for chargedShot!'
        else:
            print('shoot')
            ammo -= self.shotNo
            print("ammo: " + str(ammo))
            self._s.connect((self._host,self._port))
        # self.ir.send_code(self.IRcode)      
            self._s.send(self.IRcode)
            self._s.close()
        time.sleep(0.1)
        GPIO.output(self.emitter, GPIO.LOW)
        GPIO.output(self.laser, GPIO.LOW)
        
        self.shotNo = 1       

#LED display function
class myoLED(Thread):
    def __init__(self):
        super(myoLED, self).__init__()
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial)
        self.daemon = True
        self.event = threading.Event()
    
    def run(self):
        while not self.event.is_set():
            self.ammo_display()
            # self.health_display()
            print 'displaying ammo'
            self.event.wait(3)
            # time.sleep(0.1)
        
    def ammo_display(self):
        global ammo
        if ammo == 0:
                
            with canvas(self.device) as draw:
                text(draw, (0, 0), "R", fill="white")
            # time.sleep(1)
            for _ in range(3):
                for intensity in range(16):
                    self.device.contrast(intensity * 16)
                    time.sleep(0.1)
                    for intensity in range(16,-1):
                        self.device.contrast(intensity * 16)
                        time.sleep(0.1)
        else:
            with canvas(self.device) as draw:
                ammo_bar1 = draw.rectangle([6, 0, 7, ammo-1], fill='white')
    

    def health_display(self):
        
        global health

        if health == 0:
            msg = "Game Over"
            show_message(self.device, msg, fill='white', font=CP437_FONT, scroll_delay=0.08)
        else:
            with canvas(self.device) as draw:
                draw.rectangle([0,0, 1, health-1], fill='white')
        
        
#create LED object
# class testThread(Thread):
#     def __init__(self):
#         super(testThread, self).__init__()
#         self.daemon = True

#     def run(self):
#         while True:
#             print 'HELLo'
#             time.sleep(1)

#receiver thread
# class receiver(Thread):
#     def __init__(self):
#         super(receiver, self).__init__()
#         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.host = socket.gethostname()
#         self.port = 5556
#         self.s.bind((self.host,self.port))
#         self.LED = myoLED()
        
#     def run(self):
        
#         global mcp
#         global health

#         self.s.listen(1)

#         while True:
#         # time.sleep(0.1)
#             IR_value = mcp.read_adc(0)
#             if IR_value < 1020:
#                 client, address = self.s.accept()
#                 print 'getting connection from', address
#                 code = client.recv(7)
#                 print code
#                 if not code:
#                     break
#                 client.close()

#                 player_no = int(code[:3], 2)
#                 shot = int(code[3:], 2)
#                 damage = 0
                
#                 if shot == 1:
#                     damage = 1
#                     health -= damage
#                     print health
#                 elif shot == 2:
#                     damage = 3
#                     health -= damage
#                     print health

#                 self.LED.health_display()
#                 time.sleep(0.1)

        

def onUnlock():
    myo.unlock("hold")

roll = 0
#initialize class
player = emitter(1)
# receiver = receiver()
# receiver.start()
LED = myoLED()
LED.start()

# test = testThread()
# test.start()



def onPoseEdge(pose, edge):
    global ammo
    global roll
    global player
    
    if (pose == 'fist') and (edge == 'on'):
        
        roll = myo.getRoll()
        print('reloading.....')

    if (pose == 'waveOut') and (edge == "on"):
        if ammo <= 0:
            print('out of bullets! Please reload.')
            # LED.ammo_display()
            # LED.event.set()
            # LED.event.clear()
        else:
            player.normalShot()
            LED.event.set()
            LED.event.clear()
            # LED.ammo_display()
                
    if (pose == 'fingersSpread') and (edge == 'on'):
        print("initializing chargedShot")
        player.shotNo = 2

def onPeriodic():
    global ammo
    global roll
    roll_2 = myo.getRoll()
    if ((abs(roll) - abs(roll_2)) >= 1.20):
        print("reload success!")
        ammo = 8
        LED.event.set()
        LED.event.clear()
        roll = roll_2

    

		
