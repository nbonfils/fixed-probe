#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""Server that reads values from differents sensors.

This script is a server that is supposed to run on a RPi with the
adequate sensors hooked to it via GPIO.
It reads the value of the sensors then store them on disk or on
the usb drive if one is plugged, it also always export local data on
the usb drive if there are local data.
The measurements are stored in csv format in the file called :
    "sensors_data.csv"
either locally in "/srv/sensors/" or directly at the root of the usb.

The sensors are:
    BMP180 from adafruit : ambient temperature and barometric pressure
    DS18B : water temperature
    Turbidity Sensor (dishwasher) : turbidity of water

It also records the time and date of the measure.

"""
import os
import sys
from csv import DictWriter, DictReader
from time import sleep
from datetime import datetime

from w1thermsensor import W1ThermSensor
from Adafruit_BMP.BMP085 import BMP085
from turbsensor import TurbiditySensor


# Constants
DATA_FILENAME = 'sensors_data.csv'
PATH_TO_MEDIA = '/media/root'
MEASURE_INTERVAL = 60

# Global variables
need_to_export = None
data_file_exists = None
turbidity_sensor = None


def init():
    """Initialization for the server to run properly."""
    global need_to_export
    global data_file_exists
    global turbidity_sensor

    # Don't know if data file exists yet
    data_file_exists = False

    # Init working directory
    os.chdir('/srv/sensors')

    # Check if a local file is to be exported
    dirents = os.listdir()
    need_to_export = False
    for ent in dirents:
        if ent == DATA_FILENAME:
            need_to_export = True
            break

    # Create and start the Turbidity Sensor thread on analog pin 0
    pin = 0
    mes_per_interval = 20
    sleep = MEASURE_INTERVAL / mes_per_interval
    turbidity_sensor = TurbiditySensor(pin, sleep)
    turbidity_sensor.start()


def find_dev(path):
    """Find usb device absolute path.

    Note:
        Also check if data already exists on device and update
        global variable data_file_exists.

    Args:
        path (str): The path to the dir where the device might be.

    Returns:
        str: Full path to the correct usb device.

    """
    global data_file_exists
    data_file_exists = False
    dev = ''

    # Get full path of all devices connected
    dirents = [os.path.join(path, e) for e in os.listdir(path)]

    # Pick first one by default if data don't exists on others
    if dirents:
        dev = dirents[0]

    # Try to find if data file already exists on one device
    for ent in dirents:
        found = False
        for subent in os.listdir(ent):
            if subent == DATA_FILENAME:
                dev = ent
                data_file_exists = True
                found = True
                break
        if found:
            break

    return dev


def write_data(data):
    """Write data in the file and eventually export the local file.

    Note:
        Change 2 global variables to know where to write next  time.

    Args:
        data (dict): The dict containing the data for each parameter.

    """
    global need_to_export
    global data_file_exists

    path = find_dev(PATH_TO_MEDIA)
    fieldnames = [
            'time', 
            'date', 
            'air_temp', 
            'air_pressure', 
            'water_temp',
            'turb'
            ]

    if path == '':
        # If there is no storage device, write on disk (sd card)
        with open(DATA_FILENAME, 'a', newline='') as f:
            writer = DictWriter(f, fieldnames)

            if not need_to_export:
                # If data file will be created, add headers
                writer.writeheader()
            writer.writerow(data)

        # As written on disk data will need to be exported now
        need_to_export = True
    else:
        # If storage device available, check if need to export

        # Create the full path to the file on the device
        path = os.path.join(path, DATA_FILENAME)

        if need_to_export:
            # Open the 2 files and transfer the data
            with open(DATA_FILENAME, 'r', newline='') as e, \
                    open(path, 'a+', newline='')  as f:
                reader = DictReader(e)
                writer = DictWriter(f, fieldnames)

                if not data_file_exists:
                    # New data file will be created on device
                    writer.writeheader()
                    data_file_exists = True

                # Write data on device
                for row in reader:
                    writer.writerow(row)
                writer.writerow(data)

            # Once exported remove the local data file
            os.remove(DATA_FILENAME)
            # No more local file to be exported
            need_to_export = False
        else:
            # No need to export
            with open(path, 'a', newline='') as f:
                writer = DictWriter(f, fieldnames)

                if data_file_exists:
                    writer.writerow(data)
                else:
                    writer.writeheader()
                    writer.writerow(data)
                    # Data file created on disk
                    data_file_exists = True


def get_data():
    """Get the data from the sensors, also get the date and time.

    Data recorded:
        time (str): the time of the record in HH:MM:SS format.
        date (str): the date of the record in DD-MM-YYYY format.
        air_temp (float): the ambient temperature in Celsius.
        air_pressure (float): the barometric pressure in Pascal.
        water_temp (float): the temperature of the water in Celsius.
        turb (int): the analog value of the turbidity (from 0 to 1024).

    Returns:
        dict: The data in the order of the fieldnames.

    """
    global turbidity_sensor

    # Date (DD-MM-YYY) and time (HH:MM:SS)
    d = datetime.now()
    time = '{:%H:%M:%S}'.format(d)
    date = '{:%d-%m-%Y}'.format(d)

    # (DS18B) Water temperature
    try:
        w = W1ThermSensor()
        water_temp = str(w.get_temperature())
    except:
        water_temp = '0'

    # (BMP180) Air temperature + pressure
    try:
        b = BMP085()
        air_temp = str(b.read_temperature())
        air_pressure = str(b.read_pressure())
    except:
        air_temp = '0'
        air_pressure = '0'

    # Turbidity of the water
    turb = turbidity_sensor.read_turbidity()
    if turb > 1023:
        turb = 0

    return {
            'time' : time,
            'date' : date,
            'air_temp' : air_temp,
            'air_pressure' : air_pressure,
            'water_temp' : water_temp,
            'turb' : turb
            }


def main():
    """The main function of the program."""
    init()
    while True:
        data = get_data()
        write_data(data)
        sleep(MEASURE_INTERVAL)
    return 0

if __name__ == "__main__":
    sys.exit(main())
