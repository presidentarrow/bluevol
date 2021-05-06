import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import logging

import blue_utils
from bluedevice import Bluedevice

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BlueWindow(Gtk.Window):
    def __init__(self):
        devices = blue_utils.get_connected_devices(audio_only=True)
        self.blue_device = None
        Gtk.Window.__init__(self, title="bluevol v0.1")
        self.set_border_width(10)

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        device_store = Gtk.ListStore(str, str)
        for device in devices:
            device_store.append([device['name'], device['path']])

        devices_combo = Gtk.ComboBox.new_with_model(device_store)
        devices_combo.connect("changed", self.on_combo_change)
        renderer_text = Gtk.CellRendererText()
        devices_combo.pack_start(renderer_text, True)
        devices_combo.add_attribute(renderer_text, "text", 0)
        self.box.pack_start(devices_combo, False, False, True)


        self.vol_up_button = Gtk.Button(label="vol+")
        self.vol_up_button.connect("clicked", self.on_vol_up_button_clicked)
        self.box.pack_start(self.vol_up_button, True, True, 0)

        self.vol_down_button = Gtk.Button(label="vol-")
        self.vol_down_button.connect("clicked", self.on_vol_down_button_clicked)
        self.box.pack_start(self.vol_down_button, True, True, 0)

    def on_vol_up_button_clicked(self, widget):
        if self.blue_device is not None:
            self.blue_device.volume_up()
            logging.info("device {} Volume+".format(self.blue_device.name))
        else:
            logging.error("no device selected")

    def on_vol_down_button_clicked(self, widget):
        if self.blue_device is not None:
            self.blue_device.volume_down()
            logging.info("device {} Volume-".format(self.blue_device.name))
        else:
            logging.error("no device selected")

    def on_combo_change(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            device_path = model[tree_iter][1]
            self.blue_device = Bluedevice(device_path)
            logging.info("selected device: {} {}".format(self.blue_device.name,self.blue_device.path))

if __name__ == "__main__":

    win = BlueWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()