import pygame
import serial
import struct
import cv2
import os
import numpy as np
from datetime import datetime
import time
from multiprocessing import Process, Queue
from keras.models import model_from_json


pygame.init()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# Initialize the joysticks
pygame.joystick.init()

ser = serial.Serial(
    port="/dev/ttyACM0",
    baudrate=9600
)

l_speed = 0
r_speed = 0
f_speed = 0
steer_axis = 0

# TODO check max speed
MAX_SPEED = 100


steer_thresh = 0.01

is_auto = False
model_path = os.path.join('models', 'model1')


try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
except:
    print("Joystick not found")

try:
    ser.isOpen()
except:
    print("Error while opening serial")


try:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
except Error as e:
    print("Error accessing the camera")
    print(e)


with open(os.path.join(model_path, 'model.json'), 'r') as jfile:
    loaded_model_json = jfile.read()
    model = model_from_json(loaded_model_json)
model.load_weights(os.path.join(model_path, 'model.h5'))
print('model loaded')

try:
    # -------- Main Program Loop -----------
    while not joystick.get_button(6):
        for event in pygame.event.get():
            if hasattr(event, 'button'):
                if event.button == 4 and event.type == pygame.JOYBUTTONUP:
                    is_auto = not is_auto
                    l_trigger = 0
                    f_speed = 0
                    

            if hasattr(event, 'axis') and not is_auto:
                if event.axis == 5:
                    f_speed = int(255 * (event.value + 1) / 2)

                if event.axis == 2:
                    l_trigger = event.value

                if event.axis == 0:
                    if abs(event.value) > steer_axis: 
                        steer_axis = event.value
                    else:
                        steer_axis = 0
            continue

        if is_auto:
            ret, frame = cap.read()
            if ret:
                frame = frame.astype(np.float32) / 127.5 - 1
                frame = np.mean(frame, -1)
                frame = np.expand_dims(frame, 0)
                frame = np.expand_dims(frame, -1)

                steer_axis = model.predict(frame)[0][0]
                f_speed = MAX_SPEED
            else:
                f_speed = 0
                steer_axis = 0

        f_speed = min(MAX_SPEED, f_speed)
        l_speed = int(f_speed * (1 - abs(min(0, steer_axis))))
        r_speed = int(f_speed * (1 - max(0, steer_axis)))
        l = struct.pack('>B', l_speed)
        r = struct.pack('>B', r_speed)

        print("Right Speed: %s Left Speed %s" % (r_speed, l_speed))
        ser.write(b'~')
        ser.write(l)
        ser.write(r)
        
        clock.tick(10)
        print(ser.readline())

finally:
    ser.close()
    pygame.quit()
