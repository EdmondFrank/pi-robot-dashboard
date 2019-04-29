import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.OUT,initial=GPIO.HIGH)

def my_callback(channel):
    print("haha",time.time())
    GPIO.output(13,GPIO.input(37))

GPIO.add_event_detect(37, GPIO.BOTH, callback=my_callback)
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
