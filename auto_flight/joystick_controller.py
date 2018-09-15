#!/usr/bin/python2
import sys
import time

import pygame

try:
    import curses
except:
    curses = False

DASHBOARD = """
 Flight control for Eachine/JJRC

            throttle                            pitch

               [w]                               [up]

              {throttle_u:>3}%                               {pitch_u:>3}%

 yaw [a] {yaw_l:>3}%      {yaw_r:>3}%  [d]         [left] {roll_l:>3}%      {roll_r:>3}%  [right]  roll

              {throttle_d:>3}%                               {pitch_d:>3}%

               [s]                              [down]


roll:{roll:>3} pitch:{pitch:>3} throttle:{throttle:>3} yaw:{yaw:>3}
pressed: {pressed_keys}
Command for drone: 0x{hex_command}

Unix time: {unixtime}

Press Ctrl+C to exit
"""

JOYSTICK = {
    'BTN_START': 9,
    'BTN_SELECT': 8,
    'BTN_L1': 4,
    'BTN_L2': 6,
    'BTN_R1': 5,
    'BTN_R2': 7,
    'BTN_1': 0,
    'BTN_2': 1,
    'BTN_3': 2,
    'BTN_4': 3,
}


def detect_joystick():
    sys.stdout.write('joysticks: {}\n'.format(str(pygame.joystick.get_count())))
    if pygame.joystick.get_count() > 0:
        j = pygame.joystick.Joystick(0)
        j.init()
        sys.stdout.write('found: ' + j.get_name())
        return j
    return None


def wait_for_joystick():
    joystick_count = pygame.joystick.get_count()
    if joystick_count > 0:
        for i in range(joystick_count):
            j = pygame.joystick.Joystick(i)
            j.init()
            if j.get_name() == 'DragonRise Inc.   Generic   USB  Joystick  ':
                return j
    return None


def init_screen():
    screen = curses.initscr()
    curses.noecho()
    # set getch() non-blocking
    screen.nodelay(1)
    # escape sequences generated by some keys (keypad, function keys) will be interpreted by curses
    screen.keypad(1)
    screen.clearok(1)
    return screen


def redraw_screen(screen, roll, pitch, throttle, yaw, pressed=None, drone_command=''):
    if pressed is None:
        pressed = []

    state = {
        'throttle_u': int((throttle + 1) / 2.0 * 100),
        'throttle_d': int((1 - (throttle + 1) / 2.0) * 100),
        'yaw_r': int((yaw + 1) / 2.0 * 100),
        'yaw_l': int((1 - (yaw + 1) / 2.0) * 100),
        'pitch_u': int((pitch + 1) / 2.0 * 100),
        'pitch_d': int((1 - (pitch + 1) / 2.0) * 100),
        'roll_r': int((roll + 1) / 2.0 * 100),
        'roll_l': int((1 - (roll + 1) / 2.0) * 100),
        'unixtime': time.time(),
        'hex_command': drone_command,
        'pressed_keys': str(pressed),
        'roll': roll,
        'pitch': pitch,
        'throttle': throttle,
        'yaw': yaw,
    }

    screen.clear()

    for i, line in enumerate(DASHBOARD.split('\n')):
        screen.addstr(i, 0, line.format(**state))

    screen.refresh()


def parse_joystick_input(joystick):
    throttle = 0
    yaw = 0
    pitch = 0
    roll = 0
    commands = set()
    pressed = set()

    throttle = -joystick.get_axis(1)
    yaw = joystick.get_axis(0)
    pitch = -joystick.get_axis(4)
    roll = joystick.get_axis(3)

    for btn, code in JOYSTICK.items():
        if joystick.get_button(code) == 1:
            pressed.add(btn)

    if 'BTN_START' in pressed:
        commands.add('spin_up')
    if 'BTN_SELECT' in pressed:
        commands.add('shut_off')
    if 'BTN_R1' in pressed or 'BTN_R2' in pressed:
        commands.add('force')

    return roll, pitch, throttle, yaw, commands, pressed


DEBUG = True
if DEBUG:
    MAX_POWER = 1.0


def main_loop(screen=None, kbd=None, joystick=None):
    roll, pitch, throttle, yaw = 0, 0, 0, 0
    cmd = None

    joystick = wait_for_joystick()
    if joystick is None:
        time.sleep(1)
        sys.stdout.write('Joystick not found, exiting\n')
        sys.exit(1)
    try:
        while 1:
            roll, pitch, throttle, yaw, commands, pressed = parse_joystick_input(joystick)

            max_power = 1.0 if 'force' in commands else MAX_POWER

            if 'shut_off' in commands:
                cmd = 'shut_off'
            elif 'land' in commands:
                cmd = 'land'
            elif 'spin_up' in commands:
                cmd = 'spin_up'
            elif 'calibrate' in commands:
                cmd = 'calibrate'
            else:
                cmd = None

            yaw *= max_power
            pitch *= max_power
            roll *= max_power

            pygame.event.pump()

            if screen is not None:
                redraw_screen(screen, roll, pitch, throttle, yaw, pressed=pressed)
            clock.tick(20)
    finally:
        curses.endwin()


if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init()
    # if you are running script without TTY, don't install curses in virtualenv
    screen = init_screen() if curses else None
    kbd = None
    clock = pygame.time.Clock()
    main_loop(screen)
