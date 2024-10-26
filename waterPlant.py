import RPi.GPIO as gpio
import time

def water_plant(ammount):
    num_seconds = ammount / 10
    gpio.setmode(gpio.BCM)
    gpio.setup(18, gpio.OUT)
    gpio.output(18, gpio.HIGH)
    time.sleep(num_seconds)
    gpio.output(18, gpio.LOW)
    gpio.cleanup()
