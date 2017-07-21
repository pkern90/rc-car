import pygame
import serial
import struct
import cv2
import os
from datetime import datetime
import time
from multiprocessing import Process, Queue


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


steer_thresh = 0.01

is_recording = False
img_path = os.path.join('rec', 'img')
log_path = 'rec'

queue = Queue()

if not os.path.exists(img_path):
    os.makedirs(img_path)

if not os.path.exists(log_path):
    os.makedirs(log_path)

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
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240);
except Error as e:
    print("Error accessing the camera")
    print(e)




def writer(queue):
    try:
        f = open(os.path.join(log_path, 'log.csv'), 'w', encoding="utf-8")
    except:
        print("Error opening the file")
        
    while True:
        f_speed, steer_axis  = queue.get()
        if f_speed is not None :
            ret, frame = cap.read()
            if ret:
                print('capure image')
                
                ts = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H_%M_%S_%fZ')
                img_name = 'img_%s.jpg' % ts
                cv2.imwrite(os.path.join(img_path, img_name), frame)

                log_line = '%s,%d,%0.7f\n' % (img_name, f_speed, steer_axis)
                f.write(log_line)
                f.flush()

    f.close()


writer_p = Process(target=writer, args=((queue),))
writer_p.daemon = True
writer_p.start() 

try:
    # -------- Main Program Loop -----------
    while not joystick.get_button(6):
        for event in pygame.event.get():
            if hasattr(event, 'axis'):
                if event.axis == 5:
                    f_speed = int(255 * (event.value + 1) / 2)

                if event.axis == 2:
                    l_trigger = event.value

                if event.axis == 0:
                    if abs(event.value) > steer_axis: 
                        steer_axis = event.value
                    else:
                        steer_axis = 0

            if hasattr(event, 'button'):
                if event.button == 4 and event.type == pygame.JOYBUTTONUP:
                    is_recording = not is_recording
            continue

        if is_recording == True:
            queue.put((f_speed, steer_axis))
                                


        l_speed = f_speed * (1 - abs(min(0, steer_axis)))
        r_speed = f_speed * (1 - max(0, steer_axis))
        l = struct.pack('>B', int(l_speed))
        r = struct.pack('>B', int(r_speed))

        # print("Right Speed: %s Left Speed %s" % (r_speed, l_speed))
        ser.write(b'~')
        ser.write(l)
        ser.write(r)

        clock.tick(10)
        print(ser.readline())

finally:
    ser.close()
    pygame.quit()

    while True:
        writer_p.terminate()
        time.sleep(0.1)
        if not writer_p.is_alive():
            writer_p.join(timeout=1.0)
            queue.close()
