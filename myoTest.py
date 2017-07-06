import time
#global roll_2
roll = 0
ammo = 5

def onUnlock():
    myo.unlock('hold')

def onPoseEdge(pose, edge):
    global ammo
    if (pose == 'fist') and (edge == 'on'):
        global roll
        roll = myo.getRoll()
        print('reloading.....')
    if (pose == 'waveOut') and (edge == 'on'):
        if ammo <= 0:
            print('out of bullets!')
        else:
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
