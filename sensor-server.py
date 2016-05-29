#! /usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from csv import DictWriter, DictReader
from time import sleep


# Constants
DATA_FILENAME = 'sensors_data.csv'
PATH_TO_MEDIA = '/media/root'

# Global variables
need_to_export
data_file_exists


def init():
    """Initialize directory and check if export is needed."""
    global need_to_export
    os.chdir('/srv/sensors')

    # Check if a local file is to be exported
    dirents = os.listdir()
    need_to_export = False
    for ent in dirents:
        if ent == DATA_FILENAME:
            need_to_export = True
            break


def find_dev(path):
    """Find usb device absolute path

    Note:
        Also check if data already exists on device and update
        global variable data_file_exists

    Args:
        path (str): The path to the dir where the device might be

    Returns:
        str: Full path to the correct usb device

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
            if subent == data_filename:
                dev = ent
                data_file_exists = True
                found = True
                break
        if found:
            break

    return dev


def write_data(data):
    """Write data in the file and eventually export the local file

    Note:
        Change 2 global variables to know where to write next  time

    Args:
        data (list): The list containing the data for each parameter

    """
    global need_to_export
    global data_file_exists
    fieldnames = ['time', 'date', 'air_temp', 'air_pressure', 'water_temp']
    path = find_dev(PATH_TO_MEDIA)

    if path == '':
        # If there is no storage device, write on disk (sd card)
        with open(DATA_FILENAME, 'a', newline='') as f:
            writer = DictWriter(f, fieldnames)

            if need_to_export:
                # If data file already exists on disk
                writer.writerow(data)
            else:
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
                    open(path, 'w', newline='')  as f:
                reader = DictReader(e)
                writer = DictWriter(f, fieldnames)

                if data_file_exists:
                    # Append the transfered data
                    f.seek(0, 2)
                else:
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


def main():
    """The main function of the program"""
    init()
    while True:
        sleep(5)
    return 0

if __name__ == "__main__":
    sys.exit(main())
