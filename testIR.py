import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import RPi.GPIO as GPIO
from threading import Thread

emitter = 14
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT,SPI_DEVICE))

#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(emitter, GPIO.OUT, initial = GPIO.LOW)

print("Reading IR Sensor values, Press Ctrl-C to quit...")

try:
    value = mcp.read_adc(0)
    print(value)

def toggleEmitter():
    while True:
        GPIO.output(emitter, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(emitter, GPIO.LOW)
        time.sleep(1)

def receiverReadings():
    while True:
        value = mcp.read_adc(0)
        print(value)
		time.sleep(0.2)

thread1 = Thread(target = toggleEmitter)
thread2 = Thread(target = receiverReadings)

try:
    thread1.run()
    thread2.run()
except KeyboardInterrupt:
    GPIO.cleanup()


