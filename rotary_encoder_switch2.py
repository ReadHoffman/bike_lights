
import RPi.GPIO as GPIO
import time
from defs import *
from bike_lights_test import *

GPIO.setmode(GPIO.BCM)

class Encoder(object):
    """
    Encoder class allows to work with rotary encoder
    which connected via two pin A and B.
    Works only on interrupts because all RPi pins allow that.
    This library is a simple port of the Arduino Encoder library
    (https://github.com/PaulStoffregen/Encoder) 
    """
    def __init__(self, A, B):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A, GPIO.IN)
        GPIO.setup(B, GPIO.IN)
        self.A = A
        self.B = B
        self.pos = 0
        self.state = 0
        if GPIO.input(A):
            self.state |= 1
        if GPIO.input(B):
            self.state |= 2
        GPIO.add_event_detect(A, GPIO.BOTH, callback=self.__update)
        GPIO.add_event_detect(B, GPIO.BOTH, callback=self.__update)

    """
    update() calling every time when value on A or B pins changes.
    It updates the current position based on previous and current states
    of the rotary encoder.
    """
    def __update(self, channel):
        state = self.state & 3
        if GPIO.input(self.A):
            state |= 4
        if GPIO.input(self.B):
            state |= 8

        self.state = state >> 2

        if state == 1 or state == 7 or state == 8 or state == 14:
            self.pos += 1
        elif state == 2 or state == 4 or state == 11 or state == 13:
            self.pos -= 1
        elif state == 3 or state == 12:
            self.pos += 2
        elif state == 6 or state == 9:
            self.pos -= 2


    """
    read() simply returns the current position of the rotary encoder.
    """
    def read(self):
        return self.pos


encoder = Encoder(GPIO_ROT_ENC_CLK,GPIO_ROT_ENC_DT)

GPIO.setup(GPIO_ROT_ENC_SW,GPIO.IN,pull_up_down=GPIO.PUD_UP)

button_status = 1
def enc_button_release(channel):
    print("button released")


    
GPIO.add_event_detect(GPIO_ROT_ENC_SW,GPIO.FALLING,callback=enc_button_release,bouncetime=30)

def get_cycle_value(range_size = 5):
    cycle_value = int(encoder.read()/range_size) % modes_len
    return(cycle_value)

