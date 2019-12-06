#!/usr/bin/env pybricks-micropython

import socket
import time
from threading import Thread
from time import sleep

from pybricks import ev3brick as brick
from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.parameters import (Align, Button, Color, Direction, ImageFile,
                                 Port, SoundFile, Stop)
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, print, wait

# Write your program here
brick.sound.beep()

def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            data = str(data)
            x = data.split('\\r\\n\\r\\n')
            abc = 'abc'
            if len(x) == 2:
                abc = x[1]
                abc = abc[:-1]
                return abc
        else:
            break
    s.close()

def loop(dir):
    if dir == 1:
        test_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    else:
        test_motor = Motor(Port.A)

    ret = http_get("https://us-central1-ev3tempcontrol.cloudfunctions.net/getOccupiedRoom")
    print(ret)
    if ret == 'true':
        # test_motor.run_target(500, 90)
        test_motor.run_time(500,2000)
    wait(1000)

ts1 = TouchSensor(Port.S1)
ts2 = TouchSensor(Port.S2)

threads = list()

class threadA(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            if ts1.pressed():
                print('A')
                http_get("https://us-central1-ev3tempcontrol.cloudfunctions.net/increaseCurrentTemperature")
            if ts2.pressed():
                print('B')
                http_get("https://us-central1-ev3tempcontrol.cloudfunctions.net/decreaseCurrentTemperature")



class threadB(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        dir = 0
        while True:
            if dir == 0:
                dir = 1
            elif dir == 1:
                dir = 0
            loop(dir)



if __name__ == "__main__":
    threadA()
    threadB()
    while True:
        pass


# http_get("https://us-central1-ev3tempcontrol.cloudfunctions.net/helloWorld")
# http_get("https://us-central1-ev3tempcontrol.cloudfunctions.net/getOccupiedRoom")
# http_get("https://us-central1-ev3tempcontrol.cloudfunctions.net/increaseCurrentTemperature")
# http_get("https://us-central1-ev3tempcontrol.cloudfunctions.net/decreaseCurrentTemperature")
