import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO


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
    
    numOnes = 0
    
    while True:
        value = mcp.read_adc(0)
        print value

        if value > 1020:
            numOnes = numOnes + 1
        else:
            numOnes = 0
        
        if numOnes > 10:
            print('end')
            break

        time.sleep(0.01)

