#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
manual_input.py

Based on rc_scripts/serial_syma.py
Used to fly drone with keyboard


Created on Fri Sep 14 2018 23:55:11 2018

@author: botmayank
"""

import curses
import sys

from flight_controller.syma_controller import SymaController

PORT = "/dev/ttyUSB0"

screen = None
syma = None


def screen_init():
    global screen
    # get the curses screen window
    screen = curses.initscr()
    # turn off input echoing
    curses.noecho()
    # respond to keys immediately (don't wait for enter)
    curses.cbreak()
    # map arrow keys to special values
    screen.keypad(True)


def screen_deinit():
    # shut down curses window cleanly    
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()


def key_listener():
    global screen
    while True:
        char = screen.getch()
        screen.erase()
        parse_key_input(char)
        cmd = syma.send_command()
        screen.addstr(3, 0, "Syma Controller Command: ")
        screen.addstr(4, 0, "Thr, Roll, Pitch, Yaw:")
        screen.addstr(5, 0, cmd)


def parse_key_input(char):
    # q or ESC to quit
    if char == ord('q') or char == 27:
        sys.exit()

    # Roll/Pitch
    elif char == curses.KEY_RIGHT:
        screen.addstr(0, 0, 'right')
        screen.addstr(1, 0, 'Roll right')
        syma.delta_roll("right")

    elif char == curses.KEY_LEFT:
        screen.addstr(0, 0, 'left')
        screen.addstr(1, 0, 'Roll left')
        syma.delta_roll("left")

    elif char == curses.KEY_UP:
        screen.addstr(0, 0, 'up')
        screen.addstr(1, 0, 'Pitch forward')
        syma.delta_pitch("forward")

    elif char == curses.KEY_DOWN:
        screen.addstr(0, 0, 'down')
        screen.addstr(1, 0, 'Pitch back')
        syma.delta_pitch("back")

    # Thrust/Yaw
    elif char == ord('w'):
        screen.addstr(0, 0, 'w')
        screen.addstr(1, 0, 'Thrust up')
        syma.delta_thrust("up")

    elif char == ord('s'):
        screen.addstr(0, 0, 's')
        screen.addstr(1, 0, 'Thrust down')
        syma.delta_thrust("down")

    elif char == ord('a'):
        screen.addstr(0, 0, 'a')
        screen.addstr(1, 0, 'Yaw counter-clockwise')
        syma.delta_yaw("ccw")

    elif char == ord('d'):
        screen.addstr(0, 0, 'd')
        screen.addstr(1, 0, 'Yaw clockwise')
        syma.delta_yaw("cw")

    # Special Keys
    elif char == ord('r'):  # Default values useful for landing
        screen.addstr(0, 0, 'r')
        screen.addstr(1, 0, 'Reset all inputs')
        syma.reset_inputs()

    elif char == ord('t'):  # TH Max
        screen.addstr(0, 0, 't')
        screen.addstr(1, 0, 'Throttle Max!')
        syma.max_throttle()

    elif char == ord('g'):  # TH Go
        screen.addstr(0, 0, 'g')
        screen.addstr(1, 0, 'Throttle Go!')
        syma.go_throttle()

    elif char == ord('v'):  # Reset Roll, Pitch, Yaw
        screen.addstr(0, 0, 'v')
        screen.addstr(1, 0, 'Reset rotation')
        syma.reset_rotation()


if __name__ == "__main__":
    try:
        # Initialize curses screen
        screen_init()
        # Init Syma Controller
        syma = SymaController(PORT)

        # Start key listener
        key_listener()

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanly exit
        del syma
        screen_deinit()
