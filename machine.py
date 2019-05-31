#coding=utf-8
import RPi.GPIO as GPIO
import time

#import pigpio
#pi = pigpio.pi()


GPIO.setmode(GPIO.BOARD)
#IN1 = 17
#IN2 = 18
#IN3 = 22
#IN4 = 23
IN1 = 11
IN2 = 12
IN3 = 37
IN4 = 38

def init():
        global p1
        global p2
        global p3
        global p4
        # pi.set_mode(IN1, pigpio.OUTPUT)
        # pi.set_mode(IN2, pigpio.OUTPUT)
        # pi.set_mode(IN3, pigpio.OUTPUT)
        # pi.set_mode(IN4, pigpio.OUTPUT)

        GPIO.setup(IN1, GPIO.OUT)   #设置引脚模式
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)

        p1= GPIO.PWM(IN1, 10000)      #设定pwm启动参数
        p2= GPIO.PWM(IN2, 10000)
        p3= GPIO.PWM(IN3, 10000)
        p4= GPIO.PWM(IN4, 10000)

        p1.start(0)                 #设置PWM初始值
        p2.start(0)
        p3.start(0)
        p4.start(0)

        # pi.set_PWM_frequency(IN1, 10000)
        # pi.set_PWM_frequency(IN2, 10000)
        # pi.set_PWM_frequency(IN3, 10000)
        # pi.set_PWM_frequency(IN4, 10000)

        # print(pi.get_PWM_real_range(IN1))
        # print(pi.get_PWM_real_range(IN2))
        # print(pi.get_PWM_real_range(IN3))
        # print(pi.get_PWM_real_range(IN4))

        # pi.set_PWM_range(IN1, 100)
        # pi.set_PWM_range(IN2, 100)
        # pi.set_PWM_range(IN3, 100)
        # pi.set_PWM_range(IN4, 100)

        # pi.set_PWM_dutycycle(IN1, 0)
        # pi.set_PWM_dutycycle(IN2, 0)
        # pi.set_PWM_dutycycle(IN3, 0)
        # pi.set_PWM_dutycycle(IN4, 0)
        #pi.hardware_PWM(IN1, 10000, 0*1000000)
        #pi.hardware_PWM(IN2, 10000, 0*1000000)
        #pi.hardware_PWM(IN3, 10000, 0*1000000)
        #pi.hardware_PWM(IN4, 10000, 0*1000000)

def stop():
        # pi.set_PWM_dutycycle(IN1, 0)
        # pi.set_PWM_dutycycle(IN2, 0)
        # pi.set_PWM_dutycycle(IN3, 0)
        # pi.set_PWM_dutycycle(IN4, 0)

        p1.ChangeDutyCycle(0)       #改变pwm占空比的值
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(0)
        p4.ChangeDutyCycle(0)

def up():
        # pi.set_PWM_dutycycle(IN1, 50)
        # pi.set_PWM_dutycycle(IN2, 0)
        # pi.set_PWM_dutycycle(IN3, 50)
        # pi.set_PWM_dutycycle(IN4, 0)

        p1.ChangeDutyCycle(50)
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(50)
        p4.ChangeDutyCycle(0)

def down():
        # pi.set_PWM_dutycycle(IN1, 0)
        # pi.set_PWM_dutycycle(IN2, 50)
        # pi.set_PWM_dutycycle(IN3, 0)
        # pi.set_PWM_dutycycle(IN4, 50)

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
                GPIO.setup(IN1, GPIO.IN)   #设置引脚模式
                GPIO.setup(IN2, GPIO.IN)
                GPIO.setup(IN3, GPIO.IN)
                GPIO.setup(IN4, GPIO.IN)
                # p1.stop()
                # p2.stop()
                # p3.stop()
                # p4.stop()
                GPIO.cleanup()
                #pi.stop()

#pi.set_mode(IN1, pigpio.INPUT)
#pi.set_mode(IN2, pigpio.INPUT)
#pi.set_mode(IN3, pigpio.INPUT)
#pi.set_mode(IN4, pigpio.INPUT)
#pi.stop()
GPIO.cleanup()
