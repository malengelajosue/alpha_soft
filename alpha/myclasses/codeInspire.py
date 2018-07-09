#!/usr/bin/env python

import sys
import serial


def init():
    ser = serial.Serial()
    ser.baudrate = 4800
    ser.port = '/dev/ttyUSB0'

    ser.open()

    if not ser.isOpen():
        print("Unable to open serial port!")
        raise SystemExit

    while True:
        gps = ser.read(1)
        print
        gps


try:
    init()
except KeyboardInterrupt:
    print
    ("Done.")