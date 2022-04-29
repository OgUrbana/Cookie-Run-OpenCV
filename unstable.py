from tabnanny import check
import cv2 as cv
from cv2 import matchTemplate
import numpy as np
import os
from time import sleep, time
from ppadb.client import Client
import numpy
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from edgefilter import EdgeFilter
from touch import touchScreen
from pixel import checkImage

os.chdir(os.path.dirname(os.path.abspath(__file__)))

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

device = devices[0]

unstable_count = 0

hsv_filter = HsvFilter(0, 0, 0, 179, 255, 255, 0, 0, 0, 123) #menus


if len(devices) == 0:
    print('You must start bluestacks or connect a phone first!')

checkImage('BlueStacks', 'extraimages/SmithyName.jpg', hsv_filter, None, True)