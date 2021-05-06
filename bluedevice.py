import pydbus
import logging
import blue_utils

class Bluedevice:
    def __init__(self, device_path):
        bus = pydbus.SystemBus()
        #bus.get('org.bluez', '/org/bluez/hci0/dev_38_18_4C_0E_05_E0')
        self.dev = bus.get('org.bluez', device_path)
        self.path = device_path
        self.address = self.dev.Address
        self.device_class = self.dev.Class
        self.name = self.dev.Name
        self.alias = self.dev.Alias
        self.supported = blue_utils.check(self.name)
        self.audio = blue_utils.is_audio(self.device_class)

    def volume_up(self):
        self.dev.VolumeUp()

    def volume_down(self):
        self.dev.VolumeDown()


if __name__ == "__main__":
    pass
