
import RPi.GPIO as GPIO
import time
import socket


#Pin Assignments
IR_emitter = 4
laser = 23

#GPIO Pins Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_emitter, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(laser, GPIO.OUT, initial = GPIO.LOW)


def onUnlock():
    myo.unlock("hold")

ammo = 5
roll = 0

def onPoseEdge(pose, edge):

    global ammo
    global roll

    if (pose == 'fist') and (edge == 'on'):
        global roll
        roll = myo.getRoll()
        print('reloading.....')

    if (pose == 'waveOut') and (edge == "on"):
        if ammo <= 0:
            print('out of bullets!')
        else:
            print('shoot')
            GPIO.output(4, GPIO.HIGH)
            GPIO.output(23, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(4, GPIO.LOW)
            GPIO.output(23, GPIO.LOW)
            ammo -= 1
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

		
