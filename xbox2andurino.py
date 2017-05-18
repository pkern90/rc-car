import pygame

pygame.init()
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# Initialize the joysticks
pygame.joystick.init()

l_speed = 0
r_speed = 0
f_speed = 0
steer_axis = 0

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
except:
    print("Joystick not found")

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

    l_speed = int(f_speed * (1 - abs(min(0, steer_axis))))
    r_speed = int(f_speed * (1 - max(0, steer_axis)))

    print("Right Speed: %s Left Speed %s" % (r_speed, l_speed))

    # Limit to 30 frames per second
    clock.tick(30)
 
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

