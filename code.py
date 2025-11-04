import usb_cdc
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import board, digitalio, time

import usb_cdc
usb_cdc.enable(console=True, data=True)

kbd = Keyboard(usb_hid.devices)

button = digitalio.DigitalInOut(board.GP24)
button.switch_to_input(pull=digitalio.Pull.UP)

data_serial = usb_cdc.data  # this is the "data" port

print("Listening for text on data serial...")

was_pressed = False

while True:
    # Check for button change
    pressed = not button.value
    if pressed != was_pressed:
        was_pressed = pressed
        # Report to host (can be over serial)
        msg = "BTN_ON\n" if pressed else "BTN_OFF\n"
        print(msg)  # visible in REPL

    # Read any text from host
    if data_serial.in_waiting:
        text = data_serial.read(data_serial.in_waiting).decode("utf-8", errors="ignore")
        print(f"Got text: {text.strip()}")
        # Echo text back as HID keystrokes
#for ch in text:
#    if ch == "\n":
#        kbd.press(Keycode.ENTER)
#        kbd.release_all()
#    elif ch == "\r":
#        pass
#    else:
#        try:
#            kbd_layout.write(ch)  # use KeyboardLayoutUS if needed
#        except Exception as e:
#            print("Unsupported char:", repr(ch))
#kbd.release_all()

    time.sleep(0.01)
