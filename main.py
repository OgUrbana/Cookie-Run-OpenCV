import cv2 as cv
from cv2 import matchTemplate
import numpy as np
import os
from time import time
from ppadb.client import Client
import numpy
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
from edgefilter import EdgeFilter

os.chdir(os.path.dirname(os.path.abspath(__file__)))

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('You must start bluestacks or connect a phone first!')

#initializing the Window Capture class
wincap = WindowCapture('Bluestacks')
#initializing the Vision class
vision_smithy = Vision('extraimages/SmithyName.jpg')
vision_smithy.init_control_gui()


# land hsv_filter = HsvFilter(0, 0, 0, 24, 255, 255, 104, 0, 255, 116)
hsv_filter = HsvFilter(0, 0, 0, 179, 255, 255, 0, 0, 0, 123) #menus

loop_time = time()
while(True):
    
    screenshot = wincap.get_screenshot()

    #pre-process image
    processed_image = vision_smithy.apply_hsv_filter(screenshot)

    #do edge detection
    edges_image = vision_smithy.apply_edge_filter(processed_image)

    # object detection
    # rectangles = vision_smithy.find(processed_image, 0.5) 

    #draw the detection results onto the original image
    # output_image = vision_smithy.draw_rectangles(screenshot, rectangles)    
 
    keypoint_image = edges_image

# add this to crop
    # x, w, y, h = [85, 910, 200, 290]
    # keypoint_image = keypoint_image[y:y+h, x:x+w]

    kp1, kp2, matches, match_points = vision_smithy.match_keypoints(keypoint_image)
    match_image = cv.drawMatches(
        vision_smithy.needle_img,
        kp1,
        keypoint_image,
        kp2,
        matches,
        None)

    if match_points:
        center_point = vision_smithy.centeroid(match_points)

        center_point[0] += vision_smithy.needle_w

        match_image = vision_smithy.draw_crosshairs(match_image, [center_point])
    # cv.imshow('Matches', output_image)
    cv.imshow('Keypoint Search', match_image)
    cv.imshow('Processed', processed_image)
    cv.imshow('Edges', edges_image)

    print('FPS {}'.format( 1 / (time() - loop_time)))
    loop_time = time()
    #press 'q' with the output window focused to exit.
    #waits 1ms every loop to process key presses

    key = cv.waitKey(1)

    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)
        

print('Bot Closed.')