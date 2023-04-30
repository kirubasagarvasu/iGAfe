# -*- encoding=utf8 -*-
__author__ = "I3089"


from threading import Thread
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco

from base.BaseClass import BaseClass
# from scenes.SolveSuduko import SolveSuduko


class SudukoSolver(BaseClass):

    obj = None

    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj

    def TC003(self):
        self.stepInfo("Suduko Game Play Validation")
        # sudoScene = SolveSuduko(self.obj)
        # # poco = UnityPoco()
        # sudoScene.selectSudoku()
        # self.stepInfo("Extracting Suduko Grid")
        # gridData = sudoScene.getSudukoData()
        # if sudoScene.Suduko(gridData, 0, 0):
        #     values = sudoScene.puzzle(gridData)
        #     sudoScene.solveSuduko(values)
        # else:
        #     print("Solution does not exist:(")




