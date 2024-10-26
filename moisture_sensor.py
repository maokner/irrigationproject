import random
import RPi.GPIO as GPIO
import time

def get_moisture_level():

    return random.randint(1,100)


def read_moisture():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)  

    moisture_level = GPIO.input(18)
    
    GPIO.cleanup()
    
    return moisture_level

moisture_value = read_moisture()
print(f"Current moisture level: {moisture_value}")
