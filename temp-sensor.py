# Program for printing the Temperature readings from the DS18B20 to the pi terminal.
# We also convert the readings to Celsius & Fahrenheit
# Devices used - 'raspberry pi 3 model b', 'DS18B20 Temp Sensor', Jumper Wires', 'Bread Board'

import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# The raw readings from the sensor are stored in the '/sys/bus/w1/devices/28***' folder on the Pi
# Within this folder the Temperature data is stored in the file 'w1_slave'

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

print ('\n\n *** Temperature Sensor Module *** ')
print (' *** Display Temperature in Celsius & Fahrenheit *** \n')
foo=raw_input(' Enter the no of seconds between temp readings ::> ')
test=raw_input(' \n >>>> Hit any Key to begin ')
print('\n\n')
bar = int(foo)

#print ('\nCelsius  **  Fahrenheit \n')



def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

#CELSIUS CALCULATION
def read_temp_c():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = int(temp_string) / 1000.0
        temp_c = str(round(temp_c, 1))
        return temp_c

#FAHRENHEIT CALCULATION
def read_temp_f():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_f = (int(temp_string) / 1000.0) * 9.0 / 5.0 + 32.0
        temp_f = str(round(temp_f, 1))
        return temp_f

while True:
      print("Temp in Celsius   : " + read_temp_c() +  " C")
      print("Temp in Fahrenheit: " + read_temp_f() +  " F \n")
      time.sleep(bar)
