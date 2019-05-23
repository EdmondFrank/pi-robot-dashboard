import argparse
import tornado.ioloop
import tornado.web
from datetime import datetime
import os
import RPi.GPIO as GPIO
from time import sleep

class PostHandler(tornado.web.RequestHandler):

    # I don't understand decorators, but this fixed my "can't set attribute" error
    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self,settings):
        self._settings = settings

    def initialize(self, settings):
        self.settings = settings

    def post(self):
        #timestamp = datetime.now()
        data_json = tornado.escape.json_decode(self.request.body)
        allowed_commands = set(['37','38','39','40'])#direction
        command = data_json['command']
        command = list(command.keys())
        command = set(command)
        command = allowed_commands & command
        #file_path = str(os.path.dirname(os.path.realpath(__file__)))+"/session.txt" #save commands
        #log_entry = str(command)+" "+str(timestamp)  # datetime
        #log_entries.append((command,timestamp)) # direction combine
        #with open(file_path,"a") as writer:
        #    writer.write(log_entry+"\n")
        #print(log_entry)
        speed = self.settings['speed']
        if '37' in command:
            print("left")
            #motor.forward_left(speed)
        elif '38' in command:
            print("forward")
            #motor.forward(100)
        elif '39' in command:
            print("right")
            #motor.forward_right(speed)
        elif '40' in command:
            print("backward")
            #motor.backward(100)
        else:
            print("stop")
            #motor.stop()
class Motor:
    def __init__(self, pinForward, pinBackward, pinForward2,
     pinBackward2,pinLeft, pinRight):
        """ Initialize the motor with its control pins and start pulse-width
             modulation """

        self.pinForward = pinForward
        self.pinBackward = pinBackward
        self.pinForward2 = pinForward2
        self.pinLeft = pinLeft
        self.pinRight = pinRight
        self.pinBackward2 = pinBackward2


        GPIO.setup(self.pinLeft, GPIO.OUT)
        GPIO.setup(self.pinRight, GPIO.OUT)

        GPIO.setup(self.pinForward, GPIO.OUT)
        GPIO.setup(self.pinBackward, GPIO.OUT)
        GPIO.setup(self.pinForward2, GPIO.OUT)
        GPIO.setup(self.pinBackward2, GPIO.OUT)

        self.pwm_left = GPIO.PWM(self.pinLeft, 100)
        self.pwm_right = GPIO.PWM(self.pinRight, 100)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

    def forward(self, speed):
        self.pwm_right.ChangeDutyCycle(speed)
        self.pwm_left.ChangeDutyCycle(speed)
        GPIO.output(self.pinForward, True)
        GPIO.output(self.pinBackward, False)
        GPIO.output(self.pinForward2, True)
        GPIO.output(self.pinBackward2, False)

    def backward(self, speed):
        self.pwm_right.ChangeDutyCycle(speed)
        self.pwm_left.ChangeDutyCycle(speed)
        GPIO.output(self.pinForward, False)
        GPIO.output(self.pinBackward,  True)
        GPIO.output(self.pinForward2, False)
        GPIO.output(self.pinBackward2,  True)

    def forward_right(self, speed):
        self.pwm_right.ChangeDutyCycle(speed)
        self.pwm_left.ChangeDutyCycle(100)
        GPIO.output(self.pinForward, True)
        GPIO.output(self.pinBackward, False)
        GPIO.output(self.pinForward2, True)
        GPIO.output(self.pinBackward2, False)

    def forward_left(self, speed):
        self.pwm_right.ChangeDutyCycle(100)
        self.pwm_left.ChangeDutyCycle(speed)
        GPIO.output(self.pinForward, True)
        GPIO.output(self.pinBackward, False)
        GPIO.output(self.pinForward2, True)
        GPIO.output(self.pinBackward2, False)

    def stop(self):
        """ Set the duty cycle of both control pins to zero
            to stop the motor. """
        self.pwm_left.ChangeDutyCycle(0)
        self.pwm_right.ChangeDutyCycle(0)
        GPIO.output(self.pinForward,0)
        GPIO.output(self.pinBackward,0)
        GPIO.output(self.pinForward2,0)
        GPIO.output(self.pinBackward2,0)
def make_app(settings):
    return tornado.web.Application([
        (r"/keys", PostHandler, {'settings':settings})
    ])

if __name__ == "__main__":

    # Parse CLI args
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--speed_percent", required=True, help="Between 0 and 100")
    args = vars(ap.parse_args())
    #GPIO.cleanup(0)
    GPIO.setmode(GPIO.BOARD)
    motor = Motor(18, 19, 21, 22, 23, 24)
    log_entries = []
    settings = {'speed':float(args['speed_percent'])}
    app = make_app(settings)
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()