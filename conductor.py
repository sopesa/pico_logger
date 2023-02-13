from machine import Pin, ADC
from picozero import RGBLED
from utime import sleep

import sys
import utime

rgb = RGBLED(red = 11, green = 13, blue = 12)
rgb.color = (50, 0, 0)

sensor_temp = ADC(4)
temp_offset = 8.7
conversion_factor = 3.3 / (65535)
interface = Pin(10, Pin.IN, Pin.PULL_UP)

delta_t = 0.1
x = 50

def wait_for_interface():
    while True:
        sleep(0.1)
        if not interface.value():
            break
    while True:
        sleep(0.1)
        if interface.value():
            break



# STAGE 1: wait for button push...
wait_for_interface()

#STAGE 2: create log file...
rgb.color = (255, 0, 0)

file_name = 'temp_log.csv'
f = open(file_name, 'w')

rgb.color = (0, 0, 50)

wait_for_interface()

#STAGE 3: start logging to file...
rgb.color = (0, 50, 0)

running_sum = 0
running_count = 0

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    running_sum += reading
    running_count += 1

    if running_count == x:
        temperature = ((27 - ((running_sum/x) - 0.706)/0.001721) - temp_offset)
        f.write('{0}: {1}\n'.format(utime.mktime(utime.localtime()), temperature))
        print('{0}: {1}\n'.format(utime.mktime(utime.localtime()), temperature))
        running_sum = 0
        running_count = 0

    if not interface.value():
        break
    sleep(0.1)

#STAGE 4: save and close the log file and stop the pico
rgb.color = (100, 100, 100)
f.close()
sleep(0.2)
rgb.color = (0, 0, 0)
sys.exit()