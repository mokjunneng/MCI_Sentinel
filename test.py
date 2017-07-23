import RPi.GPIO as GPIO
import time
import socket
# import pyslinger


#Pin Assignments
IR_emitter = 4
laser = 23

#GPIO Pins Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_emitter, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(laser, GPIO.OUT, initial = GPIO.LOW)

ammo = 8

class emitter():
    def __init__(self, player):
        self._player = player
        self._team_code = "{0:03b}".format(int(player))
        self.emitter = 4
        self.laser = 23
        self._protocol = "RAW"
        self._gpio_pin = 4
        self._protocol_config = dict(one_duration = 520,
                            zero_duration = 520)
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
        self._host = 'LaserTag'
        self._port = 5556
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

def onUnlock():
    myo.unlock("hold")

roll = 0
player = emitter(1)

def onPoseEdge(pose, edge):

    global ammo
    global roll
    global player
    
    if (pose == 'fist') and (edge == 'on'):
        # global roll
        roll = myo.getRoll()
        print('reloading.....')

    if (pose == 'waveOut') and (edge == "on"):
        if ammo <= 0:
            print('out of bullets!')
        else:
            player.normalShot()
                
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
        roll = roll_2
    

		