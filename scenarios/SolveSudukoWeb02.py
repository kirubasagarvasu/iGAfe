# -*- encoding=utf8 -*-
__author__ = "I3089"

from base.BaseClass import BaseClass
# from scenes.SolveSuduko import SolveSuduko
from scenes.SolveSudukoIO import SolveSudukoWeb, puzzle, solved_grid


class SudukoSolverWeb02(BaseClass):
    obj = None

    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj

    def TC005(self):
        self.stepInfo("Suduko Game Play Validation")
        sudoScene = SolveSudukoWeb(self.obj)

        sudoScene.launchApplication()
        self.stepInfo("Extracting the Unsolved Suduko Grid")
        sudoScene.captureGrid()
        sudoScene.get_sudoku_board(puzzle)
        self.stepInfo("Solve the Suduko puzzle")
        solvedgrid = sudoScene.sudokuSolver(puzzle)

        sudoScene.fill_puzzle()
        self.stepInfo("Verify success Message")
        sudoScene.validateSolution()
