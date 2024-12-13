import RPi.GPIO as gpio
import time

def water_plant(ammount):
    loc=12
    num_seconds = ammount / 10
    gpio.setmode(gpio.BCM)
    
    gpio.setup(loc, gpio.OUT)
    gpio.output(loc, gpio.HIGH)
    time.sleep(num_seconds)
    gpio.output(loc, gpio.LOW)
    gpio.cleanup()