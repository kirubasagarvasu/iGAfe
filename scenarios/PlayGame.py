# -*- encoding=utf8 -*-
__author__ = "I3089"

import multiprocessing
from threading import Thread

from airtest.core.api import *

from base.BaseClass import BaseClass
from scenes.HomeScene import HomeScene
from scenes.PlayerActions import PlayerActions





class PlayGame(BaseClass):

    obj = None

    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj

    def TC002(self):
        self.stepInfo("Hill Climb Game Play Validation")
        homeScene = HomeScene(self.obj)
        playScene = PlayerActions(self.obj)
        # Game Play
        while homeScene.gameOver() == "no":
            playScene.accelerate(0.2, 5)
            playScene.compareAndAccelerate(0.5, 12)
            # t = multiprocessing.Process(target=home.validateLevel1, args=(20, ))
            # t.start()
