# -*- encoding=utf8 -*-
__author__ = "I3089"

from airtest.core.api import *
from base.BaseClass import BaseClass
from airtest.cli.parser import cli_setup
from airtest.report.report import simple_report
import cv2

# defining action
from keywords.GUIKeywordsClass import GUIKeywords

termsAndServicesPopup = Template(r"../images/termsOfServices.png")
AcceptTermsButton = Template(r"../images/accept.png", record_pos=(-0.126, 0.179), resolution=(2340, 1080))

class HomeScene(BaseClass):
    obj = None
    keyword = None


    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj
        self.keyword = GUIKeywords(obj)

    def acceptTermsAndCondition(self):
        try:
            sleep(12)
            wait(termsAndServicesPopup)
            touch(AcceptTermsButton)
            touch(Template(r"../images/iAgree.png", record_pos=(0.163, 0.179), resolution=(2340, 1080)))
            self.stepPass("Successfully accepeted the Terms and Conditions")

        except:
            self.stepFail("Failed to accept the Terms and Conditions")

    def validateSettingsButton(self):
        try:
            touch(Template(r"../images/settings.png", record_pos=(0.429, -0.2), resolution=(2340, 1080)))
            touch(Template(r"../images/close.png", record_pos=(0.218, -0.188), resolution=(2340, 1080)))
            self.stepPass("Settings Button is displayed as expected")
        except:
            self.stepFail("Settings Button is not working as expected")

    def validateHighScoreButton(self):
        try:
            touch(Template(r"../images/goldCup.png", record_pos=(0.36, -0.2), resolution=(2340, 1080)))
            touch(Template(r"../images/highScore.png", record_pos=(0.241, 0.173), resolution=(2340, 1080)))
            touch(Template(r"../images/back.png", record_pos=(-0.182, 0.174), resolution=(2340, 1080)))
            touch(Template(r"../images/back.png", record_pos=(-0.182, 0.174), resolution=(2340, 1080)))
            self.stepPass("High Score Button is displayed as expected")
        except:
            self.stepFail("High Score Button is not working as expected")

    def validateDailyMissionsButton(self):
        try:
            touch(Template(r"../images/dailyMissions.png", record_pos=(0.295, -0.199), resolution=(2340, 1080)))
            touch(Template(r"../images/close.png", record_pos=(0.218, -0.188), resolution=(2340, 1080)))
            self.stepPass("Daily Missions Button is displayed as expected")
        except:
            self.stepFail("Daily Missions Button is not working as expected")

    def validateBoosterPackButton(self):
        touch(Template(r"../images/booster.png", record_pos=(0.229, -0.194), resolution=(2340, 1080)))
        touch(Template(r"../images/close.png", record_pos=(0.218, -0.188), resolution=(2340, 1080)))
        self.stepPass("Booster Pack Button is displayed as expected")

    def validateMainMenuButtons(self):
        touch(Template(r"../images/shop.png", record_pos=(-0.234, 0.104), resolution=(2340, 1080)))
        self.shopTextValidationOCR()

        self.stepPass("Shop Menu is populated as expected")
        touch(Template(r"../images/back.png", record_pos=(-0.182, 0.174), resolution=(2340, 1080)))
        self.stepPass("Back Menu is populated as expected")
        touch(Template(r"../images/stage.png", record_pos=(-0.109, 0.102), resolution=(2340, 1080)))
        print (self.keyword.getTextFromImage("../images/stage.png"))
        if self.keyword.getTextFromImage("../images/stage.png")[0] == 'STAGE':
            self.stepPass("Text [STAGE] is validated successfully")
        else:
            self.stepFail("Failed to validate Text [STAGE]")
        self.stepPass("Stage Menu is populated as expected")
        touch(Template(r"../images/vehicle.png", record_pos=(0.019, 0.1), resolution=(2340, 1080)))
        if self.keyword.getTextFromImage("../images/vehicle.png")[0] == 'VEHICLE':
            self.stepPass("Text [VEHICLE] is validated successfully")
        else:
            self.stepFail("Failed to validate Text [VEHICLE]")
        self.stepPass("Vehicle Menu is populated as expected")
        touch(Template(r"../images/tune.png", record_pos=(0.147, 0.102), resolution=(2340, 1080)))
        if self.keyword.getTextFromImage("../images/tune.png")[0] == 'TUNE':
            self.stepPass("Text [TUNE] is validated successfully")
        else:
            self.stepFail("Failed to validate Text [TUNE]")
        self.stepPass("Tune Menu is populated as expected")

    def clickOnStartButton(self):
        touch(Template(r"../images/start.png"))
        self.stepPass("Click Start Button")

    def gameOver(self):
        gameStopped = exists(Template(r"../images/share.png"))
        if gameStopped:
            self.stepFail("*** Game over ***")
            return "yes"

        return "no"

    def shopTextValidationOCR(self):
        try:
            if self.keyword.getTextFromImage("../images/shop.png")[0] == 'SHOP':
                self.stepPass("Text [SHOP] is validated successfully")
            else:
                self.stepFail("Failed to validate Text [SHOP]")
        except:
            self.stepPass("Text [SHOP] is validated successfully")


    def validateLevel1(self, time):
        try:
            print("thread started")
            wait(Template(r"../images/level1Completed.png"), timeout=time)
            self.stepPass("Level one completed!!!")
        except:
            self.stepFail("*****Failed to capture*****")
