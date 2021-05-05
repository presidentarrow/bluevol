import pydbus

supported_devices = ['WF-XB700','LE_WH-XB900N']

def check(device):
    try:
        l_device = device.lower()
        return l_device in (s.lower() for s in supported_devices)
    except:
        return False

def is_audio(device_class):
    #ref https://www.bluetooth.com/specifications/assigned-numbers/baseband/
    return (device_class & (1<<21))!=0

def get_connected_devices(audio_only=True):
    bus = pydbus.SystemBus()
    #TODO: add support for adapter selection
    # adapter = bus.get('org.bluez', '/org/bluez/hci0')
    mngr = bus.get('org.bluez', '/')

    mngd_objs = mngr.GetManagedObjects()
    devices = []
    for path in mngd_objs:
        con_state = mngd_objs[path].get('org.bluez.Device1', {}).get('Connected', True)
        if con_state:
            device_class = mngd_objs[path].get('org.bluez.Device1', {}).get('Class')
            if device_class is not None:
                addr = mngd_objs[path].get('org.bluez.Device1', {}).get('Address')
                name = mngd_objs[path].get('org.bluez.Device1', {}).get('Name')
                if audio_only:
                    if is_audio(device_class):
                        devices.append({'name':name,'address':addr,'path':path, 'class': device_class,'audio':is_audio(device_class) ,'supported': check(name) })
                else:
                    devices.append({'name':name,'address':addr,'path':path, 'class': device_class,'audio': is_audio(device_class) ,'supported': check(name) })
    return devices


if __name__ == "__main__":
    print('WF-XB700: ',check('WF-XB700'))