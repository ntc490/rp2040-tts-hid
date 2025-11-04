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
button = digitalio.DigitalInOut(board.GP24)
button.switch_to_input(pull=digitalio.Pull.UP)

# Our serial port setup
data_serial = usb_cdc.data  # this is the "data" port

# Application banner
print("Watching button and listening for text on data serial for HID events...")
was_pressed = False
while True:
    # Check for button change and print state changes to REPL
    pressed = not button.value
    if pressed != was_pressed:
        was_pressed = pressed
        # Report to host (can be over serial)
        msg = "BTN_ON\n" if pressed else "BTN_OFF\n"
        print(msg.strip())  # visible in REPL

    # Read any text from host
    if data_serial.in_waiting:
        # Read data from whisper.cpp or other
        try:
            text = data_serial.read(data_serial.in_waiting).decode("utf-8")
        except Exception as e:
            print("Decode error:", e)
            text = ""

        # May need to expand this for special handling
        text = text.strip("\r")
        print(f"Got text: {text.strip()}")
        layout.write(text)

    time.sleep(0.01)
