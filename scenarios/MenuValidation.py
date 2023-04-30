# -*- encoding=utf8 -*-
__author__ = "I3089"

from airtest.core.api import *

from base.BaseClass import BaseClass
from scenes.HomeScene import HomeScene




class MenuValidation(BaseClass):
    obj = None


    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj


    def TC001(self):

        self.stepInfo("Hill Climb Game Menu Validation")
        homeScene = HomeScene(self.obj)
        # Accept Terms And Condition
        homeScene.acceptTermsAndCondition()

        # HomeScreen Validation
        homeScene.validateSettingsButton()
        homeScene.validateHighScoreButton()
        homeScene.validateDailyMissionsButton()
        homeScene.validateBoosterPackButton()
        homeScene.validateMainMenuButtons()
        homeScene.clickOnStartButton()
