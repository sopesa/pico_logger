from machine import Pin
import machine
import utime
# import _thread
import sys
import os

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
led = Pin('LED', Pin.OUT)

running_sum = 0
running_index = 0

avg_factor = 150
sampling_time = 1
temp_offset = 9.4
led_blink_time = 0.1
sample_size = 240

running_sample_size = 0

contains_log = False
file_name = 'temp_log.csv'

def led_blink():
    led.on()
    utime.sleep(led_blink_time)
    led.off()

for element in os.listdir():
    if (element == file_name):
        contains_log = True

if (contains_log):
    print('contains log')
    sys.exit()
    
f = open(file_name, 'w')

#for i in range(int(sample_size * ((avg_factor * sampling_time) / 60) / 60)):
#    led_blink()
#    utime.sleep(0.5)

while True:
    reading = sensor_temp.read_u16() * conversion_factor
    running_sum += reading
    
    if (running_index % 5 == 0):
        led_blink()
    
    if ((running_index + 1) == avg_factor):
        temperature = ((27 - ((running_sum/avg_factor) - 0.706)/0.001721) - temp_offset)
        running_index = 0
        running_sum = 0
        running_sample_size += 1
        f.write('{0}: {1}\n'.format(utime.mktime(utime.localtime()), temperature))
    else:
        running_index += 1

    if (running_sample_size == sample_size):
        f.close()
        sys.exit()
    utime.sleep(sampling_time - led_blink_time)