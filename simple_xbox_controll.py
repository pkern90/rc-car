import math

import RPi.GPIO as GPIO
import xbox

GPIO_RIGHT_BACK = 17
GPIO_RIGHT_FRONT = 18
GPIO_LEFT_BACK = 27
GPIO_LEFT_FRONT = 22
GPIO_LEFT_EN = 23
GPIO_RIGHT_EN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(GPIO_RIGHT_BACK, GPIO.OUT)
GPIO.setup(GPIO_RIGHT_FRONT, GPIO.OUT)
GPIO.setup(GPIO_LEFT_BACK, GPIO.OUT)
GPIO.setup(GPIO_LEFT_FRONT, GPIO.OUT)
GPIO.setup(GPIO_LEFT_EN, GPIO.OUT)
GPIO.setup(GPIO_RIGHT_EN, GPIO.OUT)

def update_motors(x, y):
    if x < 0.0:
        # Stand still
        GPIO.output(GPIO_LEFT_BACK, 0)
        GPIO.output(GPIO_LEFT_FRONT, 0)
    elif x > 0.0:
        # third quadrant
        GPIO.output(GPIO_RIGHT_BACK, 0)
        GPIO.output(GPIO_RIGHT_FRONT, 0)


if __name__ == '__main__':
    joy = xbox.Joystick()
    GPIO.output(GPIO_RIGHT_EN, 1)
    GPIO.output(GPIO_LEFT_EN, 1)

    while not joy.Back():
        if joy.leftTrigger():
            GPIO.output(GPIO_RIGHT_BACK, 1)
            GPIO.output(GPIO_RIGHT_FRONT, 0)
            GPIO.output(GPIO_LEFT_BACK, 1)
            GPIO.output(GPIO_LEFT_FRONT, 0)
        elif joy.rightTrigger():
            GPIO.output(GPIO_RIGHT_BACK, 0)
            GPIO.output(GPIO_RIGHT_FRONT, 1)
            GPIO.output(GPIO_LEFT_BACK, 0)
            GPIO.output(GPIO_LEFT_FRONT, 1)
        else:
            GPIO.output(GPIO_RIGHT_BACK, 0)
            GPIO.output(GPIO_RIGHT_FRONT, 0)
            GPIO.output(GPIO_LEFT_BACK, 0)
            GPIO.output(GPIO_LEFT_FRONT, 0)

        x, y = joy.leftStick()
        update_motors(x, y)

    joy.close()
    GPIO.output(GPIO_RIGHT_EN, 0)
    GPIO.output(GPIO_LEFT_EN, 0)
