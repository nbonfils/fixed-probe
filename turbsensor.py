#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Implementation of a turbidity sensor.

This module implement a class that will create a mean of the turbidity
read by the the sensor then output it when required.

"""


import threading
import time

from analog import readadc


class TurbiditySensor(threading.Thread):
    """Turbidity sensor implemented as a thread
    
    Note:
        A thread is better as analog reads are not "stable".
        And a mean over a certain period of time with a shorter delay
        between samples is more reliable

    Attributes:
        pin_num (int): The analog channel on which the sensor is hooked
        sleep (float): The delay between samples
        count (int): The number of samples since last read
        total (int): The sum of reads value since last read
    """

    def __init__(self, pin_num, sleep):
        threading.Thread.__init__(self)

        self.pin_num = pin_num
        self.sleep = sleep
        self.count = 0
        self.total = 0

    def run(self):
        while True:
            # Adds measure and keep track of num of measurements
            self.total += readadc(self.pin_num)
            self.count += 1
            time.sleep(self.sleep)

    def read_turbidity(self):
        """reads the turbidity as a rounded mean"""
        # Compute the mean
        turb = round(self.total / self.count)

        # Reset the counter and measurments
        self.total = 0
        self.count = 0

        return turb
