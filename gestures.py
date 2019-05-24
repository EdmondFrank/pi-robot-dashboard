import RPi.GPIO as GPIO
#import tornado.ioloop
#import tornado.web
from time import sleep
import time
import argparse
import os
import sys
import requests

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("Hello, world")

time_diff = 0
last = 0
now = 0

def detect(channel,wait,exec_id):
    global now,last,time_diff
    now = time.time()
    time_diff = now - last
    if time_diff > wait:
        print(channel, wait, exec_id)
        res = requests.post("http://raspberrypi:9292/start/"+exec_id)
        #if res['status'] == -1:
        #    sys.exit(0)
    last = now

# def make_app():
#     return tornado.web.Application([
#         (r"/", MainHandler),
#     ])

if __name__ == "__main__":

    # Parse CLI args
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--pin", required=True, help="signal input pin")
    ap.add_argument("-e", "--exec", required=True, help="command to exec")
    ap.add_argument("-d", "--debounce", default=2, help="debounce time")
    ap.add_argument("-i", "--init",choices=["down","up"], default="down", help="down or up")
    args = vars(ap.parse_args())

    last = time.time()

    pin = int(args['pin'])
    wait = int(args['debounce'])
    exec_id = args['exec']
    GPIO.setmode(GPIO.BOARD)
    pull_type = GPIO.PUD_DOWN if (args['init'] == "down") else GPIO.PUD_UP
    GPIO.setup(pin, GPIO.IN, pull_up_down=pull_type)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=lambda ch : detect(ch,
    wait, exec_id), bouncetime=500)

    #app = make_app()
    #app.listen(5000)
    #tornado.ioloop.IOLoop.current().start()
    while True:
        sleep(1)

GPIO.clean_up()
