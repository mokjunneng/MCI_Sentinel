import RPi.GPIO as GPIO

#Pin Assignments
emitter = 14
receiver = 21

#GPIO Pins Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(emitter, GPIO.OUT)

def onPoseEdge(pose, edge):
    if (pose == 'waveOut') and (edge == "on"): 
		GPIO.output(emitter, GPIO.LOW)
        print("Shoot!")
	