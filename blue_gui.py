import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import logging
import blue_utils
from bluedevice import Bluedevice

import webbrowser

logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BlueHandler:
    def __init__(self):
        self.blue_device = None
    
    def set_device(self, device_path):
        self.blue_device = Bluedevice(device_path)
    
    def on_destroy(self, *args):
        logging.info('bye bye')
        Gtk.main_quit()
    
    def on_about(self, *args):
        webbrowser.open('https://github.com/presidentarrow/bluevol', new=2)

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


class BlueBuilder(Gtk.Builder):
    def __init__(self):
        super().__init__()
        self.init_devices(audio_only=False)
        self.add_from_file("blue_ui.glade")
        self.combo_device = self.get_object('combo_devices')
        self.blue_handler = BlueHandler()
        self.connect_signals(self.blue_handler)
        self.set_list_store()
        
    def init_devices(self, audio_only):
        self.devices = blue_utils.get_connected_devices(audio_only)
        self.device_store = Gtk.ListStore(str, str)
        for device in self.devices:
            self.device_store.append([device['name'], device['path']])
            logging.info("found device: {} {}".format(device['name'],device['path']))


    def set_list_store(self):
        device_store = Gtk.ListStore(str, str)
        for device in self.devices:
            device_store.append([device['name'], device['path']])
        self.combo_device.set_model(device_store)
        renderer_text = Gtk.CellRendererText()
        self.combo_device.pack_start(renderer_text, True)
        self.combo_device.add_attribute(renderer_text, "text", 0)

    
    def show(self):
        window = self.get_object("blue_window")
        window.show_all()
        Gtk.main()


if __name__ == "__main__":
    BlueBuilder().show()