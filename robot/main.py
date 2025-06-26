#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, Motor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, MoveSteering
from time import sleep
from math import pi
import socket
import datetime
import os

robot = MoveSteering(left_motor_port=OUTPUT_A, right_motor_port=OUTPUT_B)
grabber = LargeMotor(address=OUTPUT_D)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def off():
    grabber.off()
    robot.off()

try:
    ip = os.popen('ip addr | grep "inet 192.168" | awk \'{print $2}\'').read().strip()
    ip = ip[0:ip.find('/')]
    port = 12350
    print("Using IP:", ip)
    print("and port:", port)

    server_socket.bind((ip, port))
    server_socket.listen(1)

    print("Waiting for connection...")
    conn, addr = server_socket.accept()

    userinputforMetoh = ''

    grabber.on(speed=100)

    def powerdown():
        off()
        conn.close()
        server_socket.close()
        exit()

    last_receivetime = datetime.datetime.now()
    while userinputforMetoh != 'q':
        userinputforMetoh = ''
        while userinputforMetoh == "":
            userinputforMetoh = conn.recv(4096).decode()

            timenow = datetime.datetime.now()
            deltatime = timenow - last_receivetime
            print("Time since last message:", deltatime.microseconds/1000, "ms")
            last_receivetime = timenow

            # Strip out blank lines
            lines = [line for line in userinputforMetoh.split("\n") if line.strip()]

            # If we don't have enough lines, bail
            if not lines:
                powerdown()

            # Use the last full line
            print("lines: ", len(lines))
            splitInput = lines[-1 if lines[-1][-1] == ';' else -2].split("#")

            # Safely parse input
            try:
                rotate = int(splitInput[0])
                speed = int(splitInput[1])
                vomit = splitInput[2] == "True"
            except (IndexError, ValueError):
                powerdown()

            grabber.on(speed=-100 if vomit else 100)

            print("speed: ", speed)
            print("rotate: ", rotate)
            #print("vomit: ", vomit)

            if (userinputforMetoh == 'd'):
                drop()

            robot.on(steering=rotate,speed=speed)

finally:
    server_socket.close()
    off()
