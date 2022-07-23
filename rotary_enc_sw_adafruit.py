import rotaryio
import board
import digitalio


button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

encoder = rotaryio.IncrementalEncoder(board.D17, board.D18)


button_state = None
last_position = encoder.position

# while True:
#     current_position = encoder.position
#     position_change = current_position - last_position
#     if position_change > 0:
#         for _ in range(position_change):
#             #cc.send(ConsumerControlCode.VOLUME_INCREMENT)
#         print(current_position)
#     elif position_change < 0:
#         for _ in range(-position_change):
#             #cc.send(ConsumerControlCode.VOLUME_DECREMENT)
#         print(current_position)
#     last_position = current_position
#     if not button.value and button_state is None:
#         button_state = "pressed"
#     if button.value and button_state == "pressed":
#         print("Button pressed.")
#         #cc.send(ConsumerControlCode.PLAY_PAUSE)
#         button_state = None

def encoder_update():
    current_position = encoder.position
    position_change = current_position - last_position
    last_position = current_position
    if not button.value and button_state is None:
        button_state = "pressed"
    if button.value and button_state == "pressed":
        button_state = None
    return(position_change,button_state)