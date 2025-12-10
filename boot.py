import usb_cdc
import storage
import board
import digitalio

usb_cdc.enable(console=True, data=True)

# Export a storage device if the 'usr' button is pressed
usr = digitalio.DigitalInOut(board.GP24)
usr.switch_to_input(pull=digitalio.Pull.UP)
if not usr.value:
    storage.enable_usb_drive()
