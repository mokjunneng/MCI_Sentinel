import RPi.GPIO as GPIO
import time
import socket
import spidev
import threading
import pygame
import sys

from luma.core.interface.serial import spi,noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, SINCLAIR_FONT, LCD_FONT

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup([26,16], GPIO.OUT)
# RED_LED = GPIO.PWM(26, 500)
GREEN_LED = GPIO.PWM(16, 500)
# RED_LED.start(100)
GREEN_LED.start(100)
#create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = '10.189.130.126'

#reserve a port for service
port = 5555

max_health = 20
health = 20

s.connect((host,port))
print 'connected'

spi2 = spidev.SpiDev()
spi2.open(0,0)

def read_adc(channel):
    if ((channel > 1) or (channel < 0)):
        return -1
    r = spi2.xfer2([1,(2+channel)<<6,0])
    ret = ((r[1]&31) << 6) + (r[2] >> 2)
    return ret  
    
def game_over():
    global health
    global max_health
    global GREEN_LED

    # pygame.mixer.pre_init(22050, -16, 2, 512)
    # pygame.mixer.init()
    # gameOver_sound = pygame.mixer.Sound("/home/sentinel/Desktop/MCI_Sentinel/gameover.wav")
    # gameOver_sound.play()1

    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial)
    msg = 'Game Over'
    show_message(device, msg, fill='white', font=proportional(LCD_FONT), scroll_delay=0.1)

    time.sleep(3)

    health = max_health
    GREEN_LED.ChangeDutyCycle(100)

def LED():
    global health
    # global max_health
    global RED_LED
    global GREEN_LED
    GREEN_LED.ChangeDutyCycle(health / 20.0 * 100)

def receiver():
    global health
    global mcp
    while True:
        # time.sleep(0.1)
        IR_value = read_adc(0)
        
        if IR_value < 1000:
            print 'IR detected'
            msg = '12:incomingData'
            s.sendall(msg)

            code = s.recv(1024)
            print code 

            if not code:
                break

            player_no = int(code[:3], 2)
            shot = int(code[3:], 2)
            damage = 0
            
            if shot == 1:
                damage = 1
                health -= damage
                print health
                LED()

            elif shot == 2:
                damage = 3
                health -= damage
                print health
                LED()

            if health==0:
                game_over()
            
            time.sleep(0.1)

    s.close()

if __name__=='__main__':
    try:
        receiver()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit()
        
        