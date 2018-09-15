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

from auto_flight.syma_controller import SymaController

PORT = "/dev/ttyUSB0"

screen = None
Syma = None


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
        cmd = Syma.send_command()
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
        Syma.roll("right")

    elif char == curses.KEY_LEFT:
        screen.addstr(0, 0, 'left')
        screen.addstr(1, 0, 'Roll left')
        Syma.roll("left")

    elif char == curses.KEY_UP:
        screen.addstr(0, 0, 'up')
        screen.addstr(1, 0, 'Pitch forward')
        Syma.pitch("forward")

    elif char == curses.KEY_DOWN:
        screen.addstr(0, 0, 'down')
        screen.addstr(1, 0, 'Pitch back')
        Syma.pitch("back")

    # Thrust/Yaw
    elif char == ord('w'):
        screen.addstr(0, 0, 'w')
        screen.addstr(1, 0, 'Thrust up')
        Syma.thrust("up")

    elif char == ord('s'):
        screen.addstr(0, 0, 's')
        screen.addstr(1, 0, 'Thrust down')
        Syma.thrust("down")

    elif char == ord('a'):
        screen.addstr(0, 0, 'a')
        screen.addstr(1, 0, 'Yaw counter-clockwise')
        Syma.yaw("ccw")

    elif char == ord('d'):
        screen.addstr(0, 0, 'd')
        screen.addstr(1, 0, 'Yaw clockwise')
        Syma.yaw("cw")

    # Special Keys
    elif char == ord('r'):  # Default values useful for landing
        screen.addstr(0, 0, 'r')
        screen.addstr(1, 0, 'Reset all inputs')
        Syma.reset_inputs()

    elif char == ord('t'):  # TH Max
        screen.addstr(0, 0, 't')
        screen.addstr(1, 0, 'Throttle Max!')
        Syma.max_throttle()

    elif char == ord('g'):  # TH Go
        screen.addstr(0, 0, 'g')
        screen.addstr(1, 0, 'Throttle Go!')
        Syma.go_throttle()

    elif char == ord('v'):  # Reset Roll, Pitch, Yaw
        screen.addstr(0, 0, 'v')
        screen.addstr(1, 0, 'Reset rotation')
        Syma.reset_rotation()


if __name__ == "__main__":
    try:
        # Initialize curses screen
        screen_init()
        # Init Syma Controller
        Syma = SymaController(PORT)

        # Start key listener
        key_listener()

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanly exit
        del Syma
        screen_deinit()
