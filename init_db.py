import sys
from device import Device
from device import db


if len(sys.argv) == 3:
    for arg in sys.argv:
        try:
            device_number = int(arg)
        except:
            pass
        if '.db' in arg:
            database = arg
    for id in range(device_number):
        new_device = Device(id, 0, '-')
        db.session.add(new_device)
        db.session.commit()

else:
    print('Wrong parameters')


