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
            motor.forward_left(speed)
        elif '38' in command:
            print("forward")
            motor.forward(speed)
        elif '39' in command:
            print("right")
            motor.forward_right(speed)
        elif '40' in command:
            print("backward")
            motor.backward(speed)
        else:
            print("stop")
            motor.stop()
class Motor:
    def __init__(self, LeftForward, LeftBackward, RightForward,
     RightBackward):
        """ Initialize the motor with its control pins and start pulse-width
             modulation """

        self.LeftForward = LeftForward
        self.LeftBackward = LeftBackward
        self.RightForward = RightForward
        self.RightBackward = RightBackward
        #self.pinLeft = pinLeft
        #self.pinRight = pinRight


        #GPIO.setup(self.pinLeft, GPIO.OUT)
        #GPIO.setup(self.pinRight, GPIO.OUT)

        GPIO.setup(self.LeftForward, GPIO.OUT)
        GPIO.setup(self.LeftBackward, GPIO.OUT)
        GPIO.setup(self.RightForward, GPIO.OUT)
        GPIO.setup(self.RightBackward, GPIO.OUT)

        # GPIO.output([self.LeftForward, self.LeftBackward, self.RightForward, self.RightBackward], GPIO.HIGH)



        self.pwm_left_1 = GPIO.PWM(self.LeftForward, 10000)
        self.pwm_left_2 = GPIO.PWM(self.LeftBackward, 10000)
        self.pwm_right_1 = GPIO.PWM(self.RightForward, 10000)
        self.pwm_right_2 = GPIO.PWM(self.RightBackward, 10000)

        self.pwm_left_1.start(0)
        self.pwm_left_2.start(0)
        self.pwm_right_1.start(0)
        self.pwm_right_2.start(0)

    def forward(self, speed):
        #self.pwm_right.ChangeDutyCycle(speed)
        #self.pwm_left.ChangeDutyCycle(speed)

        self.pwm_left_1.ChangeDutyCycle(speed)
        self.pwm_left_2.ChangeDutyCycle(0)
        self.pwm_right_1.ChangeDutyCycle(speed)
        self.pwm_right_2.ChangeDutyCycle(0)

        # GPIO.output(self.LeftForward, GPIO.HIGH)
        # GPIO.output(self.LeftBackward, GPIO.LOW)
        # GPIO.output(self.RightForward, GPIO.HIGH)
        # GPIO.output(self.RightBackward, GPIO.LOW)

    def backward(self, speed):
        #self.pwm_right.ChangeDutyCycle(speed)
        #self.pwm_left.ChangeDutyCycle(speed)
        self.pwm_left_1.ChangeDutyCycle(0)
        self.pwm_left_2.ChangeDutyCycle(speed)
        self.pwm_right_1.ChangeDutyCycle(0)
        self.pwm_right_2.ChangeDutyCycle(speed)

        # GPIO.output(self.LeftForward, GPIO.LOW)
        # GPIO.output(self.LeftBackward, GPIO.HIGH)
        # GPIO.output(self.RightForward, GPIO.LOW)
        # GPIO.output(self.RightBackward, GPIO.HIGH)


    def forward_right(self, speed):
        #self.pwm_right.ChangeDutyCycle(speed)
        #self.pwm_left.ChangeDutyCycle(100)
        self.pwm_left_1.ChangeDutyCycle(speed)
        self.pwm_left_2.ChangeDutyCycle(0)
        self.pwm_right_1.ChangeDutyCycle(0)
        self.pwm_right_2.ChangeDutyCycle(speed)

        # GPIO.output(self.LeftForward, GPIO.LOW)
        # GPIO.output(self.LeftBackward, GPIO.HIGH)
        # GPIO.output(self.RightForward, GPIO.HIGH)
        # GPIO.output(self.RightBackward, GPIO.LOW)


    def forward_left(self, speed):
        #self.pwm_right.ChangeDutyCycle(100)
        #self.pwm_left.ChangeDutyCycle(speed)
        self.pwm_left_1.ChangeDutyCycle(0)
        self.pwm_left_2.ChangeDutyCycle(speed)
        self.pwm_right_1.ChangeDutyCycle(speed)
        self.pwm_right_2.ChangeDutyCycle(0)

        # GPIO.output(self.LeftForward, GPIO.HIGH)
        # GPIO.output(self.LeftBackward, GPIO.LOW)
        # GPIO.output(self.RightForward, GPIO.LOW)
        # GPIO.output(self.RightBackward, GPIO.HIGH)


    def forward_move(self, speed_left, speed_right):
        self.pwm_left_1.ChangeDutyCycle(speed_left)
        self.pwm_left_2.ChangeDutyCycle(0)
        self.pwm_right_1.ChangeDutyCycle(speed_right)
        self.pwm_right_2.ChangeDutyCycle(0)

    def backward_move(self, speed_left, speed_right):
        self.pwm_left_1.ChangeDutyCycle(0)
        self.pwm_left_2.ChangeDutyCycle(speed_left)
        self.pwm_right_1.ChangeDutyCycle(0)
        self.pwm_right_2.ChangeDutyCycle(speed_right)

    def stop(self):
        """ Set the duty cycle of both control pins to zero
            to stop the motor. """
        #self.pwm_left.ChangeDutyCycle(0)
        #self.pwm_right.ChangeDutyCycle(0)
        self.pwm_left_1.ChangeDutyCycle(0)
        self.pwm_left_2.ChangeDutyCycle(0)
        self.pwm_right_1.ChangeDutyCycle(0)
        self.pwm_right_2.ChangeDutyCycle(0)
        # GPIO.output(self.LeftForward, GPIO.HIGH)
        # GPIO.output(self.LeftBackward, GPIO.HIGH)
        # GPIO.output(self.RightForward, GPIO.HIGH)
        # GPIO.output(self.RightBackward, GPIO.HIGH)


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
    motor = Motor(12, 11, 38, 37)
    log_entries = []
    settings = {'speed':float(args['speed_percent'])}
    app = make_app(settings)
    app.listen(3000)
    tornado.ioloop.IOLoop.current().start()
