#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Serial_test.py

Sends commands to Arduino Uno via serial port to control a drone
using the nRF24L01 wireless boards.

The arrow keys control elevator and aileron (forward/reverse and left/right)
and the w,s keys control throttle, and the a,d, keys control the rudder (yaw)

# This uses the msvcrt library, so it only works under Windows. 

This is modified to implement kbhit and getch functions of msvcrt for Linux using direct
STDIO calls based on the recipe:
http://code.activestate.com/recipes/572182-how-to-implement-kbhit-on-linux/

Created on Sat Nov 25 18:54:10 2017

@author: perrytsao
@author: botmayank
"""
import serial, time, sys
from select import select

throttle=1000 
aileron=1500 #roll 
elevator=1500 # pitch
rudder=1500 # yaw, rotates the drone

tg=10
ag=50
eg=50
rg=50

port = '/dev/ttyUSB0'

arduino = serial.Serial(port, 115200, timeout=0.01)


def getch():
    return sys.stdin.read(1)

def kbhit():
    dr, dw, de = select([sys.stdin], [], [], 0)
    return dr != []
try:
    arduino=serial.Serial(port, 115200, timeout=.01)
    time.sleep(1) #give the connection a second to settle
    #arduino.write("1500, 1500, 1500, 1500\n")
    while True:        
        data = arduino.readline()
        if data:
            #String responses from Arduino Uno are prefaced with [AU]
            print "[AU]: "+data             
        if kbhit():
            key = ord(getch())
            if key == 27: #ESC
                print "[PC]: ESC exiting"
                break
            elif key == 13: #Enter
                select()
                print "[PC]: Enter"
            elif key == 119: #w
                throttle+=tg
            elif key == 97: #a
                rudder-=rg         
            elif key == 115: #s
                throttle-=tg
            elif key == 100: #d
                rudder+=rg
            elif key == 224: #Special keys (arrows, f keys, ins, del, etc.)
                key = ord(getch())
                if key == 80: #Down arrow
                    elevator-=eg
                elif key == 72: #Up arrow
                    elevator+=eg
                elif key == 77: #right arroww
                    aileron+=ag
                elif key == 75: #left arrow
                    aileron-=ag               
            
            command="%i,%i,%i,%i"% (throttle, aileron, elevator, rudder)
            # string commands to the Arduino are prefaced with  [PC]           
            print "[PC]: "+command 
            arduino.write(command+"\n")

finally:
    # close the connection
    arduino.close()
    # re-open the serial port which will also reset the Arduino Uno and
    # this forces the quadcopter to power off when the radio loses conection. 
    arduino=serial.Serial(port, 115200, timeout=.01)
    arduino.close()
    # close it again so it can be reopened the next time it is run.  
