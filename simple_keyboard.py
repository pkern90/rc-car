import time
import serial

class _Getch:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


if __name__ == '__main__':
    print("Script started\n Use 'w', 'a', 's', 'd' to controll the car\n 'c' to stop")
    ser = serial.Serial(
	port="/dev/ttyACM0",
	baudrate=9600	
    )
    ser.isOpen()

    getch = _Getch()
    inp = "1"
    while inp != "c":
        inp = getch()
        if inp == "s":
            ser.write(b'b')
        elif inp == "w":
            ser.write(b'f')        
        elif inp == "d":
            ser.write(b'r')
        elif inp == "a":
            ser.write(b'l')
        time.sleep(0.1)

    ser.close()
   
