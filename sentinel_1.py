import RPi.GPIO as GPIO
import time
import socket
from threading import Thread
import threading
import pygame
import sys

# import LED display modules
from luma.core.interface.serial import spi,noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, SINCLAIR_FONT, LCD_FONT

#Pin Assignments
IR_emitter = 14
laser = 15

#GPIO Pins Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_emitter, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(laser, GPIO.OUT, initial = GPIO.HIGH)

#setup global variables
ammo = 8

        
#laser and emitter output class
class emitter():
    def __init__(self, player):
        self._player = player
        self._team_code = "{0:03b}".format(int(player))
        self.emitter = 14
        self.laser = 15
        self.shotNo = 1
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = '10.189.130.126'
        self._port = 5555
        self._s.connect((self._host,self._port))

    def normalShot(self):
        self.IRcode = '7:' + self._team_code + "{0:04b}".format(self.shotNo) 
        self.IRoutput()

    def chargedShot(self):
        self.IRcode = self._team_code + "{0:04b}".format(2)
        self.IRoutput()

    def IRoutput(self):
        global ammo
        
        GPIO.output(self.emitter, GPIO.HIGH)
        GPIO.output(self.laser, GPIO.LOW)
        if (self.shotNo == 2) and (ammo < 2):
            print 'insufficient power for chargedShot!'
        else:
            print('shoot')
            ammo -= self.shotNo
            print("ammo: " + str(ammo))     
            self._s.send(self.IRcode)
            # self._s.close()
        time.sleep(0.1)
        GPIO.output(self.emitter, GPIO.LOW)
        GPIO.output(self.laser, GPIO.HIGH)
        
        self.shotNo = 1       

#LED display function
class myoLED(Thread):
    def __init__(self):
        super(myoLED, self).__init__()
        self.serial = spi(port=0, device=1, gpio=noop())
        self.device = max7219(self.serial, rotate = 2)
        self.daemon = True
        self.event = threading.Event()
    
    def run(self):
        try:
            while not self.event.is_set():
                self.ammo_display()
                print 'displaying ammo'
                self.event.wait(3)
        finally:
            sys.exit()
        
    def ammo_display(self):
        global ammo
        if ammo == 0:
                
            with canvas(self.device) as draw:
                text(draw, (0, 0), "R", fill="white")
            for _ in range(2):
                for intensity in range(16):
                    self.device.contrast(intensity * 16)
                    time.sleep(0.1)
                    for intensity in range(16,-1):
                        self.device.contrast(intensity * 16)
                        time.sleep(0.1)
        else:
            with canvas(self.device) as draw:
                ammo_bar1 = draw.rectangle([2, 0, 5, ammo-1], fill='white')

    def start_display(self):
        msg = 'Start'
        show_message(self.device, msg, fill='white', font=proportional(LCD_FONT), scroll_delay=0.1)
    

    def health_display(self):
        
        global health

        if health == 0:
            msg = "Game Over"
            show_message(self.device, msg, fill='white', font=CP437_FONT, scroll_delay=0.08)
        else:
            with canvas(self.device) as draw:
                draw.rectangle([0,0, 1, health-1], fill='white')

roll = 0

#initialize class
player = emitter(1)
LED = myoLED()
LED.start()

#initialize pygame for audio effects
pygame.mixer.pre_init(22050, -16, 2, 1024)
pygame.mixer.init()
pygame.mixer.get_num_channels()
start_sound = pygame.mixer.Channel(1)
empty_sound = pygame.mixer.Channel(2)
blast_sound = pygame.mixer.Channel(3)
normal_shot_sound = pygame.mixer.Channel(4)
charging_sound = pygame.mixer.Channel(5)
reload_effect_sound = pygame.mixer.Channel(6)

game_start = pygame.mixer.Sound("/home/sentinel/Desktop/MCI_Sentinel/gamestart.wav")
empty = pygame.mixer.Sound("/home/sentinel/Desktop/MCI_Sentinel/emptyShot.wav")
blast = pygame.mixer.Sound("/home/sentinel/Desktop/MCI_Sentinel/chargedShot.wav")
normal_shot = pygame.mixer.Sound("/home/sentinel/Desktop/MCI_Sentinel/normalShot.wav")
charging = pygame.mixer.Sound("/home/sentinel/Desktop/MCI_Sentinel/charging.wav")
reload_effect = pygame.mixer.Sound("/home/sentinel/Desktop/MCI_Sentinel/laserRecharge.wav")

def onUnlock():
    myo.unlock("hold")
    # LED.start_display()
    
    start_sound.play(game_start)

def onPoseEdge(pose, edge):
    global ammo
    global roll
    global player
    # pygame.mixer.music()
    
    

    if (pose == 'fist') and (edge == 'on'):
        
        roll = myo.getRoll()
        print('reloading.....')

    if (pose == 'waveOut') and (edge == "on"):
        if ammo <= 0:       
            empty_sound.play(empty)
            print('out of bullets! Please reload.')
        else:
            if player.shotNo == 2：           
                blast_sound.play(blast)
            else:           
                normal_shot_sound.play(normal_shot)
            myo.vibrate(1)
            player.normalShot()
            LED.event.set()
            LED.event.clear()
                
    if (pose == 'fingersSpread') and (edge == 'on'):
        if ammo >= 2:
            print("initializing chargedShot")
            charging_sound.play(charging)
            myo.vibrate(1)
            player.shotNo = 2
        else:
            empty_sound.play(empty)


def onPeriodic():
    global ammo
    global roll
    
    roll_2 = myo.getRoll()
    if ((abs(roll) - abs(roll_2)) >= 1.20):
        reload_effect_sound.play(reload_effect)
        print("reload success!")
        myo.vibrate(2)
        ammo = 8
        LED.event.set()
        LED.event.clear()
        roll = roll_2

    

		
