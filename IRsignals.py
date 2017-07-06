import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from datetime import datetime
import os

GPIO.setmode(GPIO.BCM)

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT,SPI_DEVICE))


while True:

    value = 1

    while value:
        value = mcp.read_adc(0)
        if value > 1020:
            value = 1
        else:
            value = 0

    pulse_start = time.time()

    signals = []

    numOnes = 0
    
    prev_value = 0

    while True:
        
        if value != prev_value:
            pulse_end = time.time()
            pulse_duration = (pulse_end - pulse_start)*1000000
            pulse_start = pulse_end
            signals.append((prev_value,pulse_duration))

        if value:
            numOnes = numOnes + 1
        else:
            numOnes = 0
        
        if numOnes > 10000:
            break

        prev_value = value

        value = mcp.read_adc(0)
        if value > 1020:
            value = int(1)
        else:
            value = int(0)

    for (val, pulse) in signals:
        print(val,pulse)

    print("Size of array is" + str(len(signals)))

if __name__ == '__main__':
    try:
        decode = decodeIR()
        decode.readSignal()    
    except KeyboardInterrupt:   
        GPIO.cleanup()
        pass
    

                
                
    
