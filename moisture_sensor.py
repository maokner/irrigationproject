import time
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115(busnum=1)

GAIN = 2/3

# Function to read moisture level
def get_moisture_level():
    low = 0
    high = 0.54375
    
    moisture_value = adc.read_adc(0, gain=GAIN) * 0.1875/1000
    print(f"Moisture level: {moisture_value}")
    moisture_percent = round(((moisture_value + low)*100 / high),2)
    print(f"Moisture Percent: {moisture_percent}%")
    return moisture_percent



