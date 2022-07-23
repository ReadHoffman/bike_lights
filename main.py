
from bike_lights_test import *
# from rotary_encoder_switch import *
from rotary_encoder_switch2 import *
#from rotary_enc_sw_adafruit import *
from defs import *
import sys, signal
def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    pixels.fill((0, 0, 0))
    pixels.show()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


pixels.fill((0, 0, 0))
pixels.show()
time.sleep(1)

# def valueChanged(value, direction):
#     print("* New value: {}, Direction: {}".format(value, direction))

# # initialize rotary encoder
# rotenc = RotEnc(GPIO_ROT_ENC_CLK,GPIO_ROT_ENC_DT,GPIO_ROT_ENC_SW)#,valueChanged)


def select_run_mode():
#     
#     modes = [rainbow_cycle, all_green , flashing_red ]
#     modes_len = len(modes)
    
    while button_status==1:
        cycle_value = get_cycle_value()
        mode_to_run = modes[cycle_value]
        print(mode_to_run)
        while get_cycle_value()==cycle_value:
            mode_to_run()
            if GPIO.input(GPIO_ROT_ENC_SW)==0:
                button_status==0
                break
            
        
       
                
            


def run():
    select_run_mode()

if __name__ == "__main__":
    run()
    
    