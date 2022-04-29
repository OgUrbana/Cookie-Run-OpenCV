import os
from ppadb.client import Client

os.chdir(os.path.dirname(os.path.abspath(__file__)))

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

device = devices[0]



if len(devices) < 0:
    print('You must start bluestacks or connect a phone first!')


def touchScreen(x_cord, y_cord):

    return device.shell("input tap {0} {1}".format(x_cord, y_cord))