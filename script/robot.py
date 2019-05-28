-import time
import sys
import json
sys.path.append(".")
from drive_api import Motor
# 检查导入是否成功
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")

def init_settings(fname="settings.json"):
    f = open(fname)
    settings = json.loads(f.read())
    f.close()
    return settings


def flatten(lst):
     for x in lst:
         if isinstance(x, list):
             for x in flatten(x):
                 yield x
         else:
             yield x

# 树莓派编码方式：物理引脚编码
GPIO.setmode(GPIO.BOARD)

#引脚初始化
# 红外接近开关引脚分配
infrared_chan = { 'front_1' : 15, 'front_2' : 7,
                  'left_front' : 13, 'right_front' : 12,
                  'left' : 19, 'right' : 22 ,
                  'back_1' : 16, 'back_2' : 18}
# 灰度传感器引脚分配
grayscale_chan = { 'left' : 33, 'right' : 37 }
# 光电传感器引脚分配
e18_d80nk_chan = {'left_front' : 31, 'right_front' : 29, 'left_back' : 36, 'right_back' : 32}

input_chan = flatten([list(i.values()) for i in [infrared_chan, grayscale_chan, e18_d80nk_chan]])

# 电机Pwm引脚分配＋电机初始化
#GPIO.PWM(channel,frequent)
motor = Motor(21,23,26,24)

#motor = {'left_pwm1': 21, 'left_pwm2': 23 ,'right_pwm1' : 26,'right_pwm2' : 24}

# 边缘状态
# 0: 没有遇到边缘
# 1: 左前遇到边缘
# 2: 右前遇到边缘
# 3: 前面遇到边缘
# 4: 左后遇到边缘
# 5: 右后遇到边缘
# 6: 后面遇到边缘
# 7: 左边两个均遇到边缘
# 8: 右边两个均遇到边缘

def edge():
    elf = GPIO.input(e18_d80nk_chan['left_front'])
    erf = GPIO.input(e18_d80nk_chan['right_front'])
    elb = GPIO.input(e18_d80nk_chan["left_back"])
    erb = GPIO.input(e18_d80nk_chan["right_back"])

    if elf == 1 and erf == 0:
        if elb == 0:
            return 7
        else:
            return 1
    elif elf == 0 and erf == 1:
        if erb == 0:
            return 8
        else:
            return 2
    elif elf == 1 and erf == 1:
        if elb == 1 and erb == 0:
            return 7
        elif elb == 0 and erb == 1:
            return 8
        else:
            return 3
    elif elf == 0 and erf == 0:
        if elb == 1 and erb == 0:
            return 4
        elif elb == 0 and erb == 1:
            return 5
        elif elb == 1 and erb == 1:
            return 6
    # if infra_left == 0 and infra_right == 1:
    #     return 7
    # elif infra_left == 1 and infra_right == 0:
    #     return 8
    return 0

#检测敌人
#0: 无敌人
#1: 左前有敌人
#2: 右前有敌人
#3: 正前方有敌人
#4: 左后有敌人
#5: 右后有敌人
#6: 正后有敌人
#7: 正左方有敌人
#8: 正右方有敌人
def enemy():
    infra_lf=GPIO.input(infrared_chan["left_front"])
    infra_rf=GPIO.input(infrared_chan["right_front"])

    infra_front1 = GPIO.input(infrared_chan["front1"])
    infra_front2 = GPIO.input(infrered_chan["front2"])

    infra_left = GPIO.input(infrared_chan["left"])
    infra_right = GPIO.input(infrared_chan["right"])

    infra_back1 = GPIO.input(infrared_chan["back1"])
    infra_back2 = GPIO.input(infrered_chan["back2"])

    if infra_front1 == 0 or infra_front2 == 0:
        return 3
    elif infra_lf == 0 and infra_rf == 1:
        return 1
    elif infra_lf == 1 and infra_rf == 0:
        return 2
    elif infra_left == 0:
        return 7
    elif infra_right == 0:
        return 8

    if infra_back1 == 0 or infra_back2 == 0:
        return 6


#传感器初始化下降沿激活
GPIO.setup(list(input_chan), GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(gesture_chan, GPIO.IN, pull_up_down=GPIO.PUD_UP)

settings = init_settings()

# 引脚及频率设置

def delay(ms):
    time.sleep(ms/1000)

# 上台
def go():
    speed = settings["up_speed"]

    motor.forward(speed)
    delay(1000)
    motor.stop()

    motor.backward()
    delay(4000)
    motor.stop()
    #调头开始巡航,右转调头
    speed = settings["turn_speed"]
    motor.forward_right(speed)
    delay(2000)
    motor.stop()

def check_out():
    gray_left_front = GPIO.input(grayscale_chan['left'])
    gray_right_front = GPIO.input(grayscale_chan['right'])
    if gray_left_front == 1 and gray_right_front == 1:
        speed = settings["esc_speed"]
        motor.stop()
        motor.backward(speed)
        delay(500)

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

def main():
    #双手手势启动
    while True:
        left = GPIO.input(infrared_chan["left"])
        right = GPIO.input(infrared_chan["right"])
        if left == 0 and right == 0:
            break
        delay(10)
    #上台
    go()
    motor.stop()
    edge_status = 0
    enemy_status = 0
    search_sp = settings["search_speed"]
    turn_sp = settings["turn_speed"]
    attack_sp = settings["attack_speed"]
    ecs_sp = settings["esc_speed"]
    while True:
        edge_status = edge()
        for case in switch(edge_status):
            if case(0):
                #没有检测到边缘
                enemy_status = enemy()
                for task in switch(enemy_status):
                    if task(0):
                        #没有敌人
                        motor.forward(search_sp)
                        break

                    if task(1):
                        #左前方有敌人
                        motor.forward_move(turn_sp, search_sp)
                        check_out()
                        break

                    if task(2):
                        #右前方有敌人
                        motor.forward_move(search_sp, turn_sp)

                        check_out()
                        break

                    if task(3):
                        #正前方有敌人
                        motor.forward(attack_speed)
                        check_out()
                        break
                    if task(4):
                        break
                    if task(5):
                        break
                    if task(6):
                        #正后方有敌人
                        motor.stop()
                        motor.forward_right(esc_sp)
                        delay(300)
                        break

                    if task(7):
                        # 正左方有敌人
                        motor.stop()
                        motor.forward_left(turn_sp)
                        delay(300)
                        break

                    if task(8):
                        #正右方有敌人
                        motor.stop()
                        motor.forward_right(turn_sp)
                        delay(300)
                        break
                break
            if case(1):
                #左前方检测到边缘
                motor.stop()
                motor.backward_move(search_sp, turn_sp)
                delay(100)
                motor.stop()
                motor.forward_right(turn_sp)
                delay(200)
                break
            if case(2):
                #右前方检测到边缘
                motor.stop()
                motor.backward_move(turn_sp, search_sp)
                delay(100)
                motor.stop()
                motor.forward_left(turn_sp)
                delay(200)
                break
            if case(3):
                #前方检测到边缘
                motor.stop()
                motor.backward(esc_sp)
                delay(100)
                motor.forward_left(turn_sp)
                delay(500)
                break
            if case(4):
                #左后方检测到边缘
                motor.stop()
                motor.forward_move(search_sp, turn_sp)
                delay(200)
                break
            if case(5):
                #右后方检测到边缘
                motor.stop()
                motor.forward_move(turn_sp, search_sp)
                delay(200)
                break
            if case(6):
                #后方检测到边缘
                motor.stop()
                motor.forward(esc_sp)
                delay(200)
                break
            if case(7):
                #左侧监测到边缘
                motor.stop()
                motor.forward_right(turn_sp)
                delay(200)
                break
            if case(8):
                #右侧监测到边缘
                motor.stop()
                motor.forward_right(turn_sp)
                break
            if case():
                #default
                break
        delay(50)

    # while True:
    #     try:
    #         time.sleep(1)
    #         #print "Waiting for falling edge on port 23"
    #         #GPIO.wait_for_edge(15, GPIO.FALLING)
    #         #print "Falling edge detected. Here endeth the second lesson."
    #     except KeyboardInterrupt:
    #         GPIO.cleanup()       # clean up GPIO on CTRL+C exit
    #     break
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
GPIO.cleanup()              # clean up GPIO on normal exi
