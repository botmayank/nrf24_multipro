#!/usr/bin/python
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

epsilon = 0.5
target = 0.0
thrust_gain = 0.1


def get_height(camera, camera_matrix, dist_matrix):
    return arucoFinder.run_camera_and_detect(camera, camera_matrix, dist_matrix)


def control_listener(camera, camera_matrix, dist_matrix):
    while True:
        # char = screen.getch()
        # screen.erase()
        # parse_key_input(char)
        height = get_height(camera, camera_matrix, dist_matrix)
        print("\nCurrent height: " + str(height))
        control_logic(height)
        print("\nTarget height: " + str(target))

        cmd = Syma.send_command()
        print("\nCommand sent: ")
        print("Thr, Roll, Pitch, Yaw:")
        print(cmd)


def control_logic(val):
    # Logic for controlling height with thrust
    global epsilon, target, thrust_gain
    if abs(val - target) < epsilon:
        # Hover
        Syma.thrust("mid")
    elif val > target + epsilon:
        Syma.thrust("down", thrust_gain)
    elif val < target - epsilon:
        Syma.thrust("up", thrust_gain)


if __name__ == "__main__":
    try:
        # Init Syma Controller
        Syma = SymaController(PORT)

        # Init Throttle
        Syma.init_throttle()
        time.sleep(1)

        # Get Target height
        target = 15.0

        # Setup the camera
        arucoFinder = ArucoFinder()
        camera, camera_matrix, dist_matrix = arucoFinder.setup_camera(640, 480, 30)

        # Start control listener
        control_listener(camera, camera_matrix, dist_matrix)

        arucoFinder.finalize_camera(camera)

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanly exit
        del Syma
