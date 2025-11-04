import usb_cdc
import storage

usb_cdc.enable(console=True, data=True)
# Switch this based on Button status in the future
storage.enable_usb_drive()
