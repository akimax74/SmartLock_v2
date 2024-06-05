import RPi.GPIO as GPIO
import time

# BOARDでpin指定
GPIO.setmode(GPIO.BOARD)

# 制御パルスの出力
gp_out = 33
GPIO.setup(gp_out, GPIO.OUT)

servo = GPIO.PWM(gp_out, 50)
servo.start(0)

def unlock():  # 解錠

    print("open")
    
    GPIO.setup(gp_out, GPIO.OUT)
    time.sleep(0.5)


    servo.ChangeDutyCycle(2.5)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    GPIO.cleanup(gp_out)


def lock():  # 施錠

    print("close")

    GPIO.setup(gp_out, GPIO.OUT)
    time.sleep(0.5)


    servo.ChangeDutyCycle(12)
    time.sleep(0.5)

    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)

    GPIO.cleanup(gp_out)