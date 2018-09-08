#!/usr/bin/python

""" 
Basic test script to efficiently read keys including arrow keys
on Linux. This will serve as the basic controlling interface
for communicating over serial to control a quadcopter.

Based on: 
https://www.codehaven.co.uk/using-arrow-keys-with-inputs-python/

Python Curses:
https://docs.python.org/2/howto/curses.html#curses-howto
https://docs.python.org/2/library/curses.html

Created on Sun Sept 9 2018 02:01
@author: botmayank
"""

import curses
from time import sleep
 
# get the curses screen window
screen = curses.initscr()
 
# turn off input echoing
curses.noecho()
 
# respond to keys immediately (don't wait for enter)
curses.cbreak()
 
# map arrow keys to special values
screen.keypad(True)
 
try:
    while True:
        char = screen.getch()
        screen.erase()
        if char == ord('q') or char == 27: #q or ESC to quit
            break
        elif char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
            screen.addstr(0, 0, 'right')
            screen.addstr(1, 0, 'Roll right')
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'left ')       
            screen.addstr(1, 0, 'Roll left')
        elif char == curses.KEY_UP:
            screen.addstr(0, 0, 'up   ')     
            screen.addstr(1, 0, 'Pitch forward')  
        elif char == curses.KEY_DOWN:            
            screen.addstr(0, 0, 'down ')
            screen.addstr(1, 0, 'Pitch back')
        elif char == ord('w'):
            screen.addstr(0,0, 'w ')
            screen.addstr(1, 0, 'Thrust up')
        elif char == ord('a'):
            screen.addstr(0,0, 'a ')
            screen.addstr(1, 0, 'Yaw counter-clockwise')
        elif char == ord('s'):
            screen.addstr(0,0, 's ')
            screen.addstr(1, 0, 'Thrust down')
        elif char == ord('d'):
            screen.addstr(0,0, 'd ')
            screen.addstr(1, 0, 'Yaw clockwise')

except KeyboardInterrupt:
    pass

finally:
    # shut down cleanly
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
 