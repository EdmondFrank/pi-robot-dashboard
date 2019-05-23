import time
# 检查导入是否成功
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")

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
e18_d80nk_chan = {'left' : 31, 'right' : 29, 'left_back' : 36, 'right_back' : 32}

input_chan = flatten([list(i.values()) for i in [infrared_chan, grayscale_chan, e18_d80nk_chan]])

# 电机Pwm引脚分配
motor = {'left_pwm1': 21, 'left_pwm2': 23 ,'right_pwm1' : 26,'right_pwm2' : 24}

# 红外避障传感器-手势启动
gesture_chan = 38

# 边缘状态
# 0: 初始化
# 1: 左后遇到边缘
# 2: 左前遇到边缘
# 6: 左边两个均遇到边缘
# 3: 右前遇到边缘
# 8: 前面遇到边缘
# 4: 右后遇到边缘
# 7: 右边两个均遇到边缘
# 5: 后面遇到边缘
edge_status = 0


#传感器初始化下降沿激活
GPIO.setup(list(input_chan), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(gesture_chan, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#电机初始化代码
# EN=0   PWML1=占空比可调PWM信号  PWML2=1   电机正转（改变占空比就可调速）
# EN=0   PWML1=1  PWML2=占空比可调PWM信号   电机反转（改变占空比就可调速）
# EN=0   PWML1=1  PWML2=1   电机刹车
# EN=1   PWML1=1  PWML2=1   电机自由

GPIO.setup(list(motor.values()), GPIO.OUT, initial=GPIO.HIGH)


# 引脚及频率设置
#GPIO.PWM(channel,frequent)
#PWM频率一定要10K以上，这样电流电压涌动很小，最好40-50K
left_pwm1 = GPIO.PWM(motor['left_pwm1'], 44*1000)
left_pwm2 = GPIO.PWM(motor['left_pwm2'], 44*1000)
right_pwm1 = GPIO.PWM(motor['right_pwm1'], 44*1000)
right_pwm2 = GPIO.PWM(motor['right_pwm2'], 44*1000)

all_pwm = [left_pwm1, left_pwm2, right_pwm1, right_pwm2]

# 设定pwm初始值,停车状态
for i in all_pwm: i.start(0)

def delay(ms):
    time.sleep(ms)


def stop():
    for i in all_pwm: i.ChangeDutyCycle(0)

def up(speed=50):
    #EN = 0
    left_pwm1.ChangeDutyCycle(speed)
    left_pwm2.ChangeDutyCycle(0)
    right_pwm1.ChangeDutyCycle(speed)
    right_pwm2.ChangeDutyCycle(0)

def back(speed=50):
    #EN = 0
    left_pwm1.ChangeDutyCycle(0)
    left_pwm2.ChangeDutyCycle(speed)
    right_pwm1.ChangeDutyCycle(0)
    right_pwm2.ChangeDutyCycle(speed)

def left(speed):
    left_pwm1.ChangeDutyCycle(speed)
    left_pwm2.ChangeDutyCycle(0)
    right_pwm1.ChangeDutyCycle(0)
    right_pwm2.ChangeDutyCycle(0)

def right(speed):
    left_pwm1.ChangeDutyCycle(0)
    left_pwm2.ChangeDutyCycle(0)
    right_pwm1.ChangeDutyCycle(speed)
    right_pwm2.ChangeDutyCycle(0)

#手势启动
def delay_start(time):
    #上台且前进到擂台中央
    back()
    delay(1000)
    stop()
    up()
    delay(4000)
    stop()

    #执行主程序
    main()

def attack(direction, speed):
    if direction == "left_front":
        #Todo
        pass
    elif direction == "front_1":
        #Todo
        pass
    elif direction == "front_2":
        #Todo
        pass
    elif direction == "right_front":
        #Todo
        pass
    else:
        pass

def escape(direction, speed):
    if direction == "back_1":
        pass
    elif direction == "back_2":
        pass
    else:
        pass

def turn_or_attack(direction, speed):
    if direction == "left":
        pass
    elif direction == "right":
        pass
    else:
        pass

def edge_detect(direction):
    if direction == "left":
        if GPIO.input(e18_d80nk_chan['left_back']) == 0:
            edge_status = 6
        elif GPIO.input(e18_d80nk_chan['right']) == 0:
            edge_status = 8
        else:
            edge_status = 2
    elif direction == "right":
        if GPIO.input(e18_d80nk_chan['right_back']) == 0:
            edge_status = 7
        elif GPIO.input(e18_d80nk_chan['left']) == 0:
            edge_status = 8
        else:
            edge_status = 3
    elif direction == "left_back":
        if GPIO.input(e18_d80nk_chan['left']) == 0:
            edge_status = 6
        elif GPIO.input(e18_d80nk_chan['right_back']) == 0:
            edge_status = 5
        else:
            edge_status = 1
    elif direction == "right_back":
        if GPIO.input(e18_d80nk_chan['left_back']) == 0:
            edge_status = 5
        elif GPIO.input(e18_d80nk_chan['right']) == 0:
            edge_status = 7
        else:
            edge_status = 4

    adjust_robot(edge_status)


def platform_detect(item):
    if item == "left":
        pass
    elif item == "right":
        pass
    else:
        pass

def adjust_robot(stauts):
    if status == 1:
        # 前进，右转，后退
        up()
        delay(400)
        right()
        delay(400)
        back()
    elif status == 2:
        # 后退，左转，前进
        back()
        delay(400)
        left()
        delay(400)
        up()
    elif status == 3:
        #后退，右转，前进
        back()
        delay(400)
        right()
        delay(400)
        up()
    elif status == 4:
        #前进，左转，后退
        up()
        delay(400)
        left()
        delay(400)
        back()
    elif status == 6:
        # 右转，前进
        right()
        delay(400)
        up()
    elif status == 7:
        # 左转，前进
        left()
        delay(400)
        up()
#GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(13, GPIO.OUT,initial=GPIO.HIGH)

# def my_callback(channel):
#     print("haha",time.time())
#     GPIO.output(13,GPIO.input(37))

# GPIO.add_event_detect(37, GPIO.BOTH, callback=my_callback)
# 边缘识别

# 红外接近

# 灰度识别

# 事件监听 - 下降沿触发
#手势启动-防抖时间4s
GPIO.add_event_detect(gesture_chan, GPIO.DOWN, callback=lambda : delay_start(time.time), bouncetime=4000)


def main():
    # 前端红外传感器识别响应
    for direction in ["left_front", "front_1", "front_2", "right_front"]:
        GPIO.add_event_detect(infrared_chan[direction], GPIO.FALLING, callback=lambda : attack(direction,500))

    # 后方红外传感器识别响应
    for direction in ["back_1, back_2"]:
        GPIO.add_event_detect(infrared_chan[direction], GPIO.FALLING, callback=lambda : escape(direction,800))

    # 左右红外传感器识别响应
    for direction in ["left", "right"]:
        GPIO.add_event_detect(infrared_chan[direction], GPIO.FALLING, callback=lambda : turn_or_attack(direction,400))

    #e18_d80nk_chan = {'left' : 31, 'right' : 29, 'left_back' : 36, 'right_back' : 32}
    for direction in e18_d80nk_chan.values():
        GPIO.add_event_detect( e18_d80nk_chan[direction], GPIO.FALLING, callback=lambda : edge_detect(direction))

    for item in grayscale_chan.values():
        GPIO.add_event_detect(grayscale_chan[item], GPIO.FALLING, callback=lambda : platform_detect(item))


    while True:
        try:
            time.sleep(1)
            #print "Waiting for falling edge on port 23"
            #GPIO.wait_for_edge(15, GPIO.FALLING)
            #print "Falling edge detected. Here endeth the second lesson."
        except KeyboardInterrupt:
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
        break
GPIO.cleanup()              # clean up GPIO on normal exit
