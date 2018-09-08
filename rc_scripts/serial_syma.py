#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
serial_syma.py

Based on @perrytsao's serial_test:
https://github.com/perrytsao/nrf24_cx10_pc/blob/master/serial_test.py

Uses curses library to efficiently grab key presses including
arrow keys on Linux and relay them to a quadcopter via an Arduino
and an nRF24L01+ module over serial. 

Up/down: Pitch forward/back
Left/Right: Roll left/right
W/S: Thrust up/down
A/D: Yaw CCW/CW

Target platform: Syma X20

TODO: Figure out thresholds to fly quad properly

Created on Sun Sep 9 2018 02:24:18 2017

@author: botmayank
"""
import serial, time, sys, curses
from select import select

throttle = 2000 # thrust
aileron = 1500  # roll 
elevator = 1500 # pitch
rudder = 1500   # yaw

# quadcopter RC inputs
def reset_inputs():
    global throttle, aileron, elevator, rudder
    throttle = 2000 # thrust
    aileron = 1500  # roll 
    elevator = 1500 # pitch
    rudder = 1500   # yaw


# deltas to increase/decrease RC inputs
tg = 10
ag = 50
eg = 50
rg = 50

# serial init
port = '/dev/ttyUSB0'
arduino = serial.Serial(port, 115200, timeout=0.01)

# get the curses screen window
screen = curses.initscr()
 
# turn off input echoing
curses.noecho()
 
# respond to keys immediately (don't wait for enter)
curses.cbreak()
 
# map arrow keys to special values
screen.keypad(True)
 
try:
    arduino=serial.Serial(port, 115200, timeout=.01)
    time.sleep(1) #give the connection a second to settle
    arduino.write("1500, 1500, 1500, 1500\n")

    while True: # Main loop
        char = screen.getch()
        screen.erase()

        data = arduino.readline()
        if data:
            # String responses from Arduino are prefaced with [AU]
            # print doesn't work with curses, use addstr instead
            screen.addstr(4, 0, "[AU]: " + data)
        else:
            screen.addstr(4, 0, "[AU]: EMPTY!")

        if char == ord('q') or char == 27: #q or ESC to quit
            break

        elif char == curses.KEY_RIGHT:
            screen.addstr(0, 0, 'right')
            screen.addstr(1, 0, 'Roll right')
            aileron += ag

        elif char == curses.KEY_LEFT:
            screen.addstr(0, 0, 'left ')
            screen.addstr(1, 0, 'Roll left')
            aileron -= ag

        elif char == curses.KEY_UP:
            screen.addstr(0, 0, 'up   ')
            screen.addstr(1, 0, 'Pitch forward')
            elevator += eg

        elif char == curses.KEY_DOWN:           
            screen.addstr(0, 0, 'down ')
            screen.addstr(1, 0, 'Pitch back')
            elevator-=eg

        elif char == ord('w'):
            screen.addstr(0,0, 'w ')
            screen.addstr(1, 0, 'Thrust up')
            throttle += tg

        elif char == ord('a'):
            screen.addstr(0,0, 'a ')
            screen.addstr(1, 0, 'Yaw counter-clockwise')
            rudder -= rg

        elif char == ord('s'):
            screen.addstr(0,0, 's ')
            screen.addstr(1, 0, 'Thrust down')
            throttle -= tg

        elif char == ord('d'):
            screen.addstr(0,0, 'd ')
            screen.addstr(1, 0, 'Yaw clockwise')
            rudder += rg

        elif char == ord('r'): #RESET
            screen.addstr(0,0, 'RESET ')
            reset_inputs()

        command = "%i,%i,%i,%i" %(throttle, aileron, elevator, rudder)
        # string commands to the Arduino are prefaced with  [PC]
        screen.addstr(5, 0, "[PC]: " + command )
        arduino.write(command + "\n")

except KeyboardInterrupt:
    pass

finally:    
    # close the connection
    arduino.close()
    # re-open the serial port which will also reset the Arduino Uno and
    # this forces the quadcopter to power off when the radio loses conection. 
    arduino=serial.Serial(port, 115200, timeout=.01)
    # close it again so it can be reopened the next time it is run.    
    arduino.close()

    # shut down curses window cleanly    
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
