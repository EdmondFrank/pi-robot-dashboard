#coding=utf-8
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
IN1 = 11
IN2 = 12
IN3 = 16
IN4 = 15

def init():
        global p1
        global p2
        global p3
        global p4
        GPIO.setup(IN1, GPIO.OUT)   #设置引脚模式
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)

        p1= GPIO.PWM(IN1, 100)      #设定pwm启动参数
        p2= GPIO.PWM(IN2, 100)
        p3= GPIO.PWM(IN3, 100)
        p4= GPIO.PWM(IN4, 100)

        p1.start(0)                 #设置PWM初始值
        p2.start(0)
        p3.start(0)
        p4.start(0)

def stop():
        p1.ChangeDutyCycle(0)       #改变pwm占空比的值
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(0)

def up():
        p1.ChangeDutyCycle(50)
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(50)
        p4.ChangeDutyCycle(0)

def down():
        p1.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(50)
        p3.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(50)

if __name__ == "__main__":
        try:
            init()        #初始化引脚
            time.sleep(1)
            while True:
                res = raw_input()
                print("The input value is:",res)
                if (res == "w" or res == "W"):#按w并回车确认，电机以50占空比转动
                    up()
                    print("forward",time.ctime())

                if (res == "s" or res == "S"):#按s并回车确认，电机停止转动
                    stop()
                    print("stop",time.ctime())

                if (res == "d" or res == "D"):#按d并回车确认，电机以50占空比转动
                    down()
                    print("back",time.ctime())
        except KeyboardInterrupt:
            GPIO.cleanup()
GPIO.cleanup()
