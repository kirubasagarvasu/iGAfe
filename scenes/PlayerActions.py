# -*- encoding=utf8 -*-
__author__ = "I3089"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
import cv2
from pathlib import Path


# defining action
from base.BaseClass import BaseClass


class PlayerActions(BaseClass):

    obj = None

    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj

    def accelerate(self, durationInSec, speed):
        try:
            touch(Template(r"../images/gas.png", record_pos=(0.386, 0.147), resolution=(2340, 1080)),
                  duration=durationInSec, times=speed)
            self.stepPass("Applying stable (0.2 seconds) Acceleration for 5 times")
        except:
            self.stepFail("Can't move forward. Game Over")

    def brake(self, speed):
        touch(Template(r"../images/brake.png", record_pos=(-0.35, 0.149), resolution=(2340, 1080)), duration=speed)

    def compareAndAccelerate(self, durationInSec, speed):
        currentDirectory = str(Path.cwd())
        # Save image
        snapshot(filename=currentDirectory + "\..\screenShots\screen.png")
        img = cv2.imread(currentDirectory + "\..\screenShots\screen.png")
        x, y, w, h = (700, 60, 300, 100)

        # Crop the image around the object's coordinates
        cropped_img = img[y:y + h, x:x + w]

        # Load the two images
        img1 = cropped_img
        img2 = cv2.imread(currentDirectory + "\..\images\previousDistance.png")

        # Compute the mean squared error between the two images
        mse = ((img1 - img2) ** 2).mean()

        # If the mean squared error is below a certain threshold, the images are considered similar
        if mse < 5:
            self.stepPass("More Acceleration Needed. Speeding Up (0.5 seconds) for 12 times ...!")
            self.accelerate(durationInSec, speed)

        # write image
        cv2.imwrite(currentDirectory + "\..\images\previousDistance.png", cropped_img)
