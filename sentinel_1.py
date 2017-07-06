import RPi.GPIO as GPIO
import time

#Pin Assignments
IR_emitter = 14
laser = 16

#GPIO Pins Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_emitter, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(laser, GPIO.out, initial = GPIO.LOW)
GPIO.setwarnings(False)


def onUnlock():
    	myo.unlock("hold")

def onPoseEdge(pose, edge):
    global ammo
    if (pose == 'fist') and (edge == 'on'):
        global roll
        roll = myo.getRoll()
        print('reloading.....')

    if (pose == 'waveOut') and (edge == "on"):
        if ammo <= 0:
            print('out of bullets!')
        else:
            GPIO.output(IR_emitter, GPIO.HIGH)
            GPIO.output(laser, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(IR_emitter, GPIO.LOW)
            GPIO.output(laser, GPIO.LOW)
            ammo -= 1
            print('shoot')
            print("ammo: " + str(ammo)) 
        

def onPeriodic():
    global ammo
    global roll
    roll_2 = myo.getRoll()
    #print(abs(roll_2))
    if ((abs(roll) - abs(roll_2)) >= 1.20):
        print("reload success!")
        ammo = 5
        roll = roll_2

		