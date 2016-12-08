# Program for printing the temperaure readings from the DS18B20 to the pi terminal.
# We also convert the readings to Celsius & Fahrenheit
# Devices used - 'raspberry pi 3 model b', 'DS18B20 Temp Sensor', Jumper Wires', 'Bread Board'

# introduced the time variable ist
## set the data for loading into influxDB using json_body


import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

from influxdb import InfluxDBClient

host = "192.168.1.124" ## Change the IP address here with your machines IP address
port = 8086
dbname = "IoTDashboard"
user = "root"
password = "root"

host_pi = "drawingroom"   # change this on each Pi
sample_duration = 5 # seconds

client = InfluxDBClient(host, port, user, password, dbname)
client.create_database(dbname)

#ist = time.ctime()

# The raw readings from the sensor are stored in the '/sys/bus/w1/devices/28***' folder on the Pi
# Within this folder the temerature data is stored in the file 'w1_slave'

def get_cpu_temp():
    path="/sys/class/thermal/thermal_zone0/temp"
    f = open(path, "r")
    temp_raw = int(f.read().strip())
    temp_cpu = float(temp_raw / 1000.0)
    return temp_cpu


base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#print ('\n *** Temperature Sensor Module *** ')
#print (' *** Display Temperature in Celsius & Fahrenheit *** ')
#print ('   C      F   ')

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c



try:
    while True:
        ist = time.ctime()
        temp_cpu = get_cpu_temp()
        temperature = read_temp()
        json_body = [
            {
               "measurement": "ambient_celcius",
               "tags": {"host": host_pi},
               "time": ist,
               "fields": {
                    "value": temperature,
                    "val": float(temperature)
                    }
            },
            {
                "measurement": "cpu_celcius",
                "tags": {"host": host_pi},
                "time": ist,
                "fields": {
                    "value": temp_cpu,
                    }
                }
            ]
        print(read_temp())
        print(get_cpu_temp())
        print(ist)
        client.write_points(json_body)
        time.sleep(sample_duration)
except KeyboardInterrupt:
    pass
