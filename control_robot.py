import pygame
import serial
import struct


pygame.init()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# Initialize the joysticks
pygame.joystick.init()

ser = serial.Serial(
    port="/dev/tty.usbmodem1411",
    baudrate=9600
)

l_speed = 0
r_speed = 0
f_speed = 0
steer_axis = 0

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
    # -------- Main Program Loop -----------
    while not joystick.get_button(6):
        for event in pygame.event.get():
            if event.axis == 5:
                f_speed = int(255 * (event.value + 1) / 2)

            if event.axis == 2:
                l_trigger = event.value

            if event.axis == 0:
                steer_axis = event.value

            continue

        l_speed = f_speed * (1 - abs(min(0, steer_axis)))
        r_speed = f_speed * (1 - max(0, steer_axis))
        l = struct.pack('>B', int(l_speed))
        r = struct.pack('>B', int(r_speed))

        # print("Right Speed: %s Left Speed %s" % (r_speed, l_speed))
        ser.write(b'~')
        ser.write(l)
        ser.write(r)

        clock.tick(30)
        print(ser.readline())

finally:
    ser.close()
    pygame.quit()
