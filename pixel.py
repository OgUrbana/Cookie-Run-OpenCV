from concurrent.futures import process
from tkinter import E
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
from touch import touchScreen

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def checkImage(window_name, image_name, hsv_filter=None, edge_filter=None, debug=False):

    #initializing window capture class
    wincap = WindowCapture(window_name)

    screenshot = wincap.get_screenshot()

    vision_item = Vision(image_name)

    


    loop_time = time()
    while(True):
        processed_image = vision_item.apply_hsv_filter(screenshot, hsv_filter)

        edges_image = vision_item.apply_edge_filter(processed_image, edge_filter)

        keypoint_image = edges_image

        rectangles = vision_item.find(processed_image, 0.5) 


        output_image = vision_item.draw_rectangles(screenshot, rectangles)   
        
        if debug:
            kp1, kp2, matches, match_points = vision_item.match_keypoints(keypoint_image)
            match_image = cv.drawMatches(
            vision_item.needle_img,
            kp1,
            keypoint_image,
            kp2,
            matches,
            None)
            if match_points:
                center_point = vision_item.centeroid(match_points)

                center_point[0] += vision_item.needle_w

                match_image = vision_item.draw_crosshairs(match_image, [center_point])
            cv.imshow('Matches', output_image)
            # cv.imshow('Keypoint Search', match_image)
            # cv.imshow('Processed', processed_image)
            # cv.imshow('Edges', edges_image)

            print('FPS {}'.format( 1 / (time() - loop_time)))
            loop_time = time()
            #press 'q' with the output window focused to exit.
            #waits 1ms every loop to process key presses

            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                break
    return