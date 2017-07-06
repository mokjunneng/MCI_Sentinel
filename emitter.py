import time
import RPi.GPIO as GPIO

emitter = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(emitter, GPIO.OUT, initial = GPIO.LOW)




class emitter():
    def __init__(self, player):
        self._player = player
        self._team_code = "{0:03b}".format(int(player))

    def normalShot(self):
        IRcode = '1' + self._team_code + "{0:04b}".format(1) + '0'
        print(IRcode)
        for i in IRcode:
            if i == '1':
                GPIO.output(4, GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(4, GPIO.LOW)
            elif i == '0':
                GPIO.output(4, GPIO.LOW)
                time.sleep(0.01)
        

    def chargedShot(self):
        IRcode = '1' + self._team_code + "{0:04b}".format(2) + '0'
        print(IRcode)
        for i in IRcode:
            if i == '1':
                GPIO.output(4, GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(4, GPIO.LOW)
            elif i == '0':
                GPIO.output(4, GPIO.LOW)
                time.sleep(0.01)

class receiver():
    def __init__(self,code):
        self._code = code
    
    def decodeIR(self):
        pass
        
        
if __name__ == '__main__':
    try:
        player1 = emitter(1)
        player2 = emitter(2)
        player2.chargedShot()
    except KeyboardInterrupt:
        GPIO.cleanup()
    # shot2 = player2.chargedShot()
    # print shot1
    # print shot2
        
        
        
        

