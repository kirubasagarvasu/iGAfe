# -*- encoding=utf8 -*-
__author__ = "I3089"

from airtest.core.api import *
import json
import os


# import sys
# sys.path.append('/path/to/parent/directory')

from base.BaseClass import BaseClass
from keywords.GUIKeywordsClass import GUIKeywords
from scenarios.MenuValidation import MenuValidation
from scenarios.PlayGame import PlayGame
# from scenarios.SolvePuzzle_Suduko import SudukoSolver
from scenarios.SolveSudukoWeb01 import SudukoSolverWeb
from scenarios.SolveSudukoWeb02 import SudukoSolverWeb02
from scenarios.SolveSuduko_Human import SudukoSolverHuman

# Get the path of the current file
current_file = __file__

# Get the path of the parent directory
parent_directory = os.path.dirname(os.path.abspath(current_file))
gparent_directory = os.path.dirname(parent_directory)
jsonFile = open(f'{gparent_directory}/data/test.json')
testData = json.load(jsonFile)


obj = BaseClass()

driver = GUIKeywords(obj)

def startTest(testId):
    test = [x for x in testData['Tests'] if x['TestID'] == testId][0]
    if test['ExecutionFlag']:
        obj.BeforeTest(test['TestID'], test['TestDescription'])
    return test['ExecutionFlag']


# *** Before All Execution ***
obj.BeforeAll(testData['Game'], driver)


if startTest('TC001'):
    print("*** Start of Test Case #TC001 ***")
    menuValidation = MenuValidation(obj)
    menuValidation.TC001()
    print("*** End of Test Case #TC001 ***")

if startTest('TC002'):
    print("*** Start of Test Case #TC002 ***")
    gamePlay = PlayGame(obj)
    gamePlay.TC002()
    print("*** End of Test Case #TC002 ***")

if startTest('TC003'):
    print("*** Start of Test Case #TC003 ***")
    # sudoSol = SudukoSolver(obj)
    # sudoSol.TC003()
    print("*** End of Test Case #TC003 ***")

if startTest('TC004'):
    print("*** Start of Test Case #TC004 ***")
    sudoSol = SudukoSolverWeb(obj)
    sudoSol.TC004()
    print("*** End of Test Case #TC004 ***")

if startTest('TC005'):
    print("*** Start of Test Case #TC005 ***")
    sudoSol = SudukoSolverWeb02(obj)
    sudoSol.TC005()
    print("*** End of Test Case #TC005 ***")

if startTest('TC006'):
    print("*** Start of Test Case #TC006 ***")
    sudoSol = SudukoSolverHuman(obj)
    sudoSol.TC006()
    print("*** End of Test Case #TC006 ***")

# *** After All Execution ***
obj.AfterAll(driver)
# stop Application

