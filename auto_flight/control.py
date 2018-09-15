# -*- coding: utf-8 -*-
"""
control.py

Controller logic for flying the quadcopter autonomously

Rev 0.1: Bang-bang controller

Created on Fri Sep 14 2018 23:55:11 2018

@author: botmayank
"""

import time

from auto_flight.syma_controller import SymaController
from vision.aruco.aruco_finder import ArucoFinder

PORT = "/dev/ttyUSB0"
Syma = None
arucoFinder = None

epsilon = 5
target = 80.0
thrust_gain = 5

# prev_height = 0.0
count = 0
land_thresh = 20  # no. of lost frames after which it should land


def get_height():
    global count
    count = 0
    current_height = arucoFinder.run_camera_and_detect()
    if current_height == -1:
        count += 1
        if count == land_thresh:
            Syma.reset_inputs()
            count = 0
            time.sleep(2)
            Syma.init_throttle()
            current_height = 0.0
        else:
            Syma.delta_thrust("mid")
            current_height = target
    else:
        count = 0

    return current_height


def control_listener():
    while True:
        height = get_height()
        print("<===============================>")
        print("Current height: " + str(height))
        control_logic(height)
        print("Target height: " + str(target))

        cmd = Syma.send_command()
        print("\nCommand sent: ")
        print("Thr, Roll, Pitch, Yaw:")
        print(cmd)


def control_logic(val):
    # Logic for controlling height with thrust
    global epsilon, target, thrust_gain
    # if abs(val - target) < epsilon:
    #     # Hover
    #     Syma.thrust("mid")
    if val > target + epsilon:
        Syma.delta_thrust("down", thrust_gain)
    elif val <= target - epsilon:
        Syma.delta_thrust("up", thrust_gain)


if __name__ == "__main__":
    try:
        # Init Syma Controller
        Syma = SymaController(PORT)
        time.sleep(2)

        print("Init Throttle: ")
        # Init Throttle
        Syma.init_throttle()
        time.sleep(1)

        # Get Target height
        # target = 50.0

        # Setup the camera
        arucoFinder = ArucoFinder(640, 480, 30)

        # Start control listener
        control_listener()

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanly exit
        del Syma
        del arucoFinder
