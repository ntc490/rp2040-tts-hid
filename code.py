import usb_cdc
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
import board, digitalio, time

# Keyboard and layout config
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# Button setup
button = digitalio.DigitalInOut(board.GP18)
button.switch_to_input(pull=digitalio.Pull.UP)

# Our serial port setup
data_serial = usb_cdc.data  # this is the "data" port

# Button toggle state
btn_state = False
prev_pressed = False

# Application banner
print("Watching button and listening for text on data serial for HID events...")
while True:
    # Check for button change and print state changes to REPL
    pressed = not button.value

    # Pressing the button toggles the state
    if prev_pressed and not pressed:  # Released after being pressed
        btn_state = not btn_state     # Toggle state
        print("BTN_ON" if btn_state else "BTN_OFF")
    prev_pressed = pressed

    # Read any text from host
    if data_serial.in_waiting:
        # Read data from whisper.cpp or other
        try:
            text = data_serial.read(data_serial.in_waiting).decode("utf-8")
        except Exception as e:
            print("Decode error:", e)
            text = ""
        text = text.strip("\r")

        # May need to expand this for special handling
        if text:
            print(f"Typing: {repr(text)}")
            layout.write(text)

    time.sleep(0.01)
