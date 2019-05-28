#from ../drive_api import Motor
import sys
import json
#sys.path.append("..")
sys.path.append(".")
from drive_api import Motor
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
# motor = Motor(11, 12, 16, 15)

# motor.stop()

# GPIO.cleanup()

# def init_settings(fname="settings.json"):
#     f = open(fname)
#     settings = json.loads(f.read())
#     f.close()
#     return settings

# print(init_settings())
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

v = 0
for case in switch(v):
    if case(0):
        print 1
        break
    if case(1):
        print 3
        break
    if case(4):
        print 10
        break
    if case(11):
        print 11
        break
    if case(): # default, could also just omit condition or 'if True'
        print "something else!"
