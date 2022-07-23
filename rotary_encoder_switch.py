from defs import *
import RPi.GPIO as GPIO
import time

class RotEnc:
    def __init__(self, leftPin, rightPin, buttonPin):#, callback=None):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.buttonPin = buttonPin
        self.leftPin_value = 0
        self.rightPin_value = 0
        self.value = 0
        self.button_value = 1
        self.state = '00'
        self.direction = None
        self.rot_changed = False
        self.last_updated = time.time()
        #self.callback = callback
        GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.leftPin, GPIO.RISING, callback=self.update)#,bouncetime=100)  
        GPIO.add_event_detect(self.rightPin, GPIO.RISING, callback=self.update)#,bouncetime=100) 
        GPIO.add_event_detect(self.buttonPin, GPIO.BOTH, callback=self.update)#,bouncetime=100)  
# 
#     def print_direction_and_value(self):
#         print( self.direction," ",self.value)
# 
#     def update_left(self,channel):
# #         print("update left")
#         self.changed = True
#         self.value -= 1
#         
#     def update_right(self,channel):
# #         print("update right")
#         self.changed = True
#         self.value += 1
#         
#     def update_button(self,channel):
#         print("update button")
#         self.changed = True
#         self.button_value = GPIO.input(self.buttonPin)

    def update(self,channel):
        new_button_value = GPIO.input(self.buttonPin)
        if self.button_value != new_button_value:
            self.button_changed = True
            self.button_value = new_button_value

        new_leftPin_value = GPIO.input(self.leftPin)
        if self.leftPin_value != new_leftPin_value:
            self.rot_changed = True
            self.leftPin_value = new_leftPin_value

        new_rightPin_value = GPIO.input(self.rightPin)
        if self.rightPin_value != new_rightPin_value:
            self.rot_changed = True
            self.rightPin_value = new_rightPin_value
            

        newState = "{}{}".format(self.leftPin_value, self.rightPin_value)
   
        if self.state != newState:
            if self.state == "00": # Resting position
                if newState == "01": # Turned right 1
                    self.direction = "R"
                    self.value += 1
                elif newState == "10": # Turned left 1
                    self.direction = "L"
                    self.value -= 1

            elif self.state == "01": # R1 or L3 position
                if newState == "11": # Turned right 1
                    self.direction = "R"
                    self.value += 1
                elif newState == "00": # Turned left 1
                    if self.direction == "L":
                        self.value -= 1
#                         if self.callback is not None:
#                             self.callback(self.value, self.direction)

            elif self.state == "10": # R3 or L1
                if newState == "11": # Turned left 1
                    self.direction = "L"
                    self.value -= 1
                elif newState == "00": # Turned right 1
                    if self.direction == "R":
                        self.value += 1
#                         if self.callback is not None:
#                             self.callback(self.value, self.direction)

            elif self.state == "11":
                if newState == "01": # Turned left 1
                    self.direction = "L"
                    self.value -= 1
                elif newState == "10": # Turned right 1
                    self.direction = "R"
                    self.value += 1
                elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                    if self.direction == "L":
                        self.value -= 1
#                         if self.callback is not None:
#                             self.callback(self.value, self.direction)
                    elif self.direction == "R":
                        self.value += 1
#                         if self.callback is not None:
#                             self.callback(self.value, self.direction)
        else:
            self.changed = False
                
        self.state = newState


    def getValue(self):
        return self.value
    