import sys
from server import Device
from server import db


if len(sys.argv) == 2:
    for arg in sys.argv:
        try:
            device_number = int(arg)
        except:
            pass
    for id in range(device_number):
        new_device = Device(id+1, 0, '-')
        db.session.add(new_device)
        db.session.commit()

else:
    print('Wrong parameters')


