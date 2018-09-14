#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
syma_controller.py

Created on Fri Sep 14 2018 23:55:11 2018

@author: botmayank
"""
import serial, time, sys

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

    throttle = INPUT_MIN # thrust
    aileron = INPUT_MID  # roll
    elevator = INPUT_MID # pitch
    rudder = INPUT_MID   # yaw
    arduino = None
    port = "/dev/ttyUSB0"

    def __init__(self, port):
        self.port = port
        self.arduino = serial.Serial(port, 115200, timeout=0.01)
        time.sleep(1) #give the connection a second to settle
        self.arduino.write("1000, 1500, 1500, 1500\n")

    def __del__(self):
        # close the connection
        self.arduino.close()
        # re-open the serial port which will also reset the Arduino Uno and
        # this forces the quadcopter to power off when the radio loses conection. 
        self.arduino=serial.Serial(self.port, 115200, timeout=.01)
        # close it again so it can be reopened the next time it is run.    
        self.arduino.close()


    def _clamp_input(self, n):
        return max(INPUT_MIN, min(n, INPUT_MAX))

    def _update_input(self, input_type, val, delta):
        # global throttle, aileron, elevator, rudder
        temp = val + delta

        if input_type == "thrust":
            self.throttle =self. _clamp_input(temp)
        elif input_type == "roll":
            self.aileron = self._clamp_input(temp)
        elif input_type == "pitch":
            self.elevator = self._clamp_input(temp)
        elif input_type == "yaw":
            self.rudder = self._clamp_input(temp)

    def roll(self, dir):
        if dir == "right":
            self._update_input("roll", self.aileron, +ag)
        elif dir == "left":
            self._update_input("roll", self.aileron, -ag)

    def pitch(self, dir):
        if dir == "forward":
            self._update_input("pitch", self.elevator, +eg)
        elif dir == "back":
            self._update_input("pitch", self.elevator, -eg)

    def yaw(self, dir):
        if dir == "ccw":
            self._update_input("yaw", self.rudder, -rg)
        elif dir == "cw":
            self._update_input("yaw", self.rudder, +rg)

    def thrust(self, dir):
        if dir == "up":
            self._update_input("thrust", self.throttle, +tg)
        elif dir == "down":
            self._update_input("thrust", self.throttle, -tg)

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
        command = "%i, %i, %i, %i" %(self.throttle, self.aileron, self.elevator, self.rudder)
        # string commands to the Arduino are prefaced with  [PC]
        # screen.addstr(4, 0, "[PC]: Thr, Roll, Pitch, Yaw:" )
        # screen.addstr(5, 0, "[PC]: " + command )
        self.arduino.write(command + "\n")
        return command
