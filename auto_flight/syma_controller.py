#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
syma_controller.py

Created on Fri Sep 14 2018 23:55:11 2018

@author: botmayank
"""
import serial
import time

INPUT_MIN = 1000
INPUT_MID = 1500
INPUT_MAX = 2000

THROTTLE_GO = 1530

# deltas to increase/decrease RC inputs
tg = 5
ag = 20
eg = 20
rg = 20


class SymaController:
    """ Syma Controller class """

    throttle = INPUT_MIN  # thrust
    aileron = INPUT_MID  # roll
    elevator = INPUT_MID  # pitch
    rudder = INPUT_MID  # yaw
    arduino = None
    port = "/dev/ttyUSB0"

    def __init__(self, port):
        self.port = port
        self.arduino = serial.Serial(port, 115200, timeout=0.01)
        time.sleep(1)  # give the connection a second to settle
        self.arduino.write("1000, 1500, 1500, 1500\n")

    def __del__(self):
        # close the connection
        self.arduino.close()
        # re-open the serial port which will also reset the Arduino Uno and
        # this forces the quadcopter to power off when the radio loses conection. 
        self.arduino = serial.Serial(self.port, 115200, timeout=.01)
        # close it again so it can be reopened the next time it is run.    
        self.arduino.close()

    def init_throttle(self):
        self.max_throttle()
        time.sleep(0.5)
        self.go_throttle()

    def _clamp_input(self, n):
        return max(INPUT_MIN, min(n, INPUT_MAX))

    def _update_input(self, input_type, val, delta):
        # global throttle, aileron, elevator, rudder
        temp = val + delta

        if input_type == "thrust":
            self.throttle = self._clamp_input(temp)
        elif input_type == "roll":
            self.aileron = self._clamp_input(temp)
        elif input_type == "pitch":
            self.elevator = self._clamp_input(temp)
        elif input_type == "yaw":
            self.rudder = self._clamp_input(temp)

    def roll(self, dir, delta=ag):
        if dir == "right":
            self._update_input("roll", self.aileron, +delta)
        elif dir == "left":
            self._update_input("roll", self.aileron, -delta)

    def pitch(self, dir, delta=eg):
        if dir == "forward":
            self._update_input("pitch", self.elevator, +delta)
        elif dir == "back":
            self._update_input("pitch", self.elevator, -delta)

    def yaw(self, dir, delta=rg):
        if dir == "ccw":
            self._update_input("yaw", self.rudder, -delta)
        elif dir == "cw":
            self._update_input("yaw", self.rudder, +delta)

    def thrust(self, dir, delta=tg):
        if dir == "up":
            self._update_input("thrust", self.throttle, +delta)
        elif dir == "down":
            self._update_input("thrust", self.throttle, -delta)
        elif dir == "mid":
            self.throttle = INPUT_MID

    def reset_inputs(self):
        self.throttle = INPUT_MIN
        self.aileron = INPUT_MID
        self.rudder = INPUT_MID
        self.elevator = INPUT_MID

    def max_throttle(self):
        self.throttle = INPUT_MAX

    def go_throttle(self):
        self.throttle = THROTTLE_GO

    def reset_rotation(self):
        self.aileron = INPUT_MID
        self.rudder = INPUT_MID
        self.elevator = INPUT_MID

    def send_command(self):
        command = "%i, %i, %i, %i" % (self.throttle, self.aileron, self.elevator, self.rudder)
        self.arduino.write(command + "\n")
        return command
