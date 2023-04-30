# -*- encoding=utf8 -*-
__author__ = "I3089"

from base.BaseClass import BaseClass
# from scenes.SolveSuduko import SolveSuduko
from scenes.SolveSudukoIO import SolveSudukoWeb, puzzle, solved_grid , puzzleHmn, puzzleHuman


class SudukoSolverHuman(BaseClass):
    obj = None

    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj

    def TC006(self):
        self.stepInfo("Suduko Game Play Validation")
        sudoScene = SolveSudukoWeb(self.obj)

        sudoScene.launchApplication()
        self.stepInfo("Extracting the Unsolved Suduko Grid")
        sudoScene.captureGrid()
        sudoScene.get_sudoku_board(puzzleHuman)
        self.stepInfo("Fill the empty cells with possible values")
        originalGrid = [...]
        solution = [...]
        # solvedgrid = sudoScene.sudokuSolver(puzzle)
        # sudoScene.sudokuSolverHmn(puzzle)
        # sudoScene.fillGrid(puzzle)
        # sudoScene.fillGridNew(puzzle)
        # sudoScene.fillGridAndModify(puzzle)
        # sudoScene.sudokuSolverHmn2(puzzle) #doesn't complete the grid first
        # sudoScene.sudokuSolverHmn3(puzzle) #solves the grid but doesn't complete the grid first
        # sudoScene.sudokuSolverHmn4(puzzle) #same issue
        # initial_puzzle = puzzle.copy()
        initial_puzzle = [row[:] for row in puzzleHuman]

        sudoScene.sudokuSolverHmn99(puzzleHuman) #  fills the grid first but doesn't solve it
        # sudoScene.solveSudokuHuman(puzzle)
        # sudoScene.captureGrid()
        # sudoScene.get_sudoku_board_Human()
        sudoScene.checkForInvalidCells()
        self.stepInfo("Solve the Suduko puzzle")
        solvedgrid1 = sudoScene.sudokuSolver(initial_puzzle)

        sudoScene.fill_puzzleHmn(initial_puzzle)
        

        self.stepInfo("Verify success Message")
        sudoScene.validateSolution()
