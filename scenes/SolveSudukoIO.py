from airtest.core.api import *

from poco.drivers.unity3d import UnityPoco
from base.BaseClass import BaseClass
from keywords.GUIKeywordsClass import GUIKeywords
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import copy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


M = 9
box = []
puzzle = []
puzzleHuman = []
puzzleHmn = []
incrementedlst = []
lst = []

rows, cols = 9, 9
solved_grid = []
result = []
# driver = webdriver.Chrome(executable_path="C:\\Windows\\chromedriver.exe")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


class SolveSudukoWeb(BaseClass):
    obj = None
    keyword = None

    def __init__(self, obj):
        self.testResults = obj.testResults
        self.currentTest = obj.currentTest
        self.obj = obj
        self.keyword = GUIKeywords(obj)

    def launchApplication(self):
        # Launch the browser and navigate to the Sudoku website
        self.stepInfo('Launch the Sudoku Applicaion')
        driver.get("https://www.sudokuonline.io/")
        # driver.find_element(By.XPATH, "//a[@aria-label='dismiss cookie message']")
        driver.maximize_window()

    def get_sudoku_board(self ,puzzlegrid):
        # puzzle = [[] for _ in range(len(puzzle))]
        # puzzle.clear()
        # for sublst in puzzle:
        #     if sublst:
        #         sublst.clear()
        # puzzle = [[0 for j in range(9)] for i in range(9)]

        for i in range(9):
            row = []
            for j in range(9):
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                cell = driver.find_element(By.XPATH, cell_id)
                # text = cell.text.strip()
                text = cell.get_attribute("data-value").strip()
                if not text:
                    row.append(0)
                else:
                    row.append(int(text))
            puzzlegrid.append(row)
            # incrementedlst.append(row)

        # incrementedlst = puzzle.copy()

        # incrementedlst = copy.deepcopy(puzzle)
        # print(str(incrementedlst))
        self.stepPass(str(puzzlegrid))

    def get_sudoku_board_Human(self):

        for i in range(9):
            row = []
            for j in range(9):
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                cell = driver.find_element(By.XPATH, cell_id)
                # text = cell.text.strip()
                text = cell.get_attribute("data-value").strip()
                if not text:
                    row.append(0)
                else:
                    row.append(int(text))
            puzzleHmn.append(row)

        self.stepPass(str(puzzleHmn))

    def get_sudoku_boardinc(self):

        for i in range(9):
            row = []
            for j in range(9):
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                cell = driver.find_element(By.XPATH, cell_id)
                # text = cell.text.strip()
                text = cell.get_attribute("data-value").strip()
                if not text:
                    row.append(0)
                else:
                    row.append(int(text))

            incrementedlst.append(row)

        # incrementedlst = puzzle.copy()

        # incrementedlst = copy.deepcopy(puzzle)
        print(str(incrementedlst))

    # finds the next empty cell
    # no empty cells left means (i, j) == (-1, -1))
    def find(self, lst, searchEle):
        (i, j) = (-1, -1)
        for row in range(0, rows):
            for col in range(0, cols):
                if lst[row][col] == searchEle:
                    (i, j) = (row, col)
                    return (i, j)
        return (i, j)

    def printSol(self, lst):
        # print('\nSolution:')
        # for row in lst:
        #     print(row)
        #     solved_grid.append(row)

        for row in lst:
            solved_row = []
            for num in row:
                solved_row.append(num)
            solved_grid.append(solved_row)

        return solved_grid

    def sudokuSolver(self, lst):
        (i, j) = self.find(lst, 0)
        if (i, j) == (-1, -1):
            return self.printSol(lst)
            # return
        excludedNums = set()
        for row in range(0, rows):
            for col in range(0, cols):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])
        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for number in possibleNums:
            if number not in excludedNums:
                lst[i][j] = number
                solution = self.sudokuSolver(lst)
                if solution:
                    return solution
                lst[i][j] = 0

        return None

        self.stepPass("Solved the sudoku grid")


    def fill_puzzle(self):
        for i in range(9):
            for j in range(9):
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                cell = driver.find_element(By.XPATH, cell_id)
                text = cell.get_attribute("data-value").strip()
                if i == 8 & j == 8:
                    self.stepPass(str(puzzle))
                if not text:
                    value = str(puzzle[i][j])
                    cell.send_keys(value)

    def fill_puzzleHmn(self, solvedGrid):
        for i in range(9):
            for j in range(9):
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                cell = driver.find_element(By.XPATH, cell_id)
                delete = driver.find_element(By.XPATH, "//div[@id='del']")

                text = cell.get_attribute("data-value").strip()
                invalid = "invalid" in cell.get_attribute("class").strip()
                value = str(solvedGrid[i][j])
                if i == 8 & j == 8:
                    self.stepPass(str(solvedGrid))
                if text != value:
                    time.sleep(5)
    
                    cell.click()
                    delete.click()
                    # cell.clear()
                    cell.send_keys(value)

    def fill_puzzle_incremented(self, lst1, lst2):
        inc_result = self.compare_lists(lst1, lst2)
        for sub_list in inc_result:
            for i, num in enumerate(sub_list):
                if num == 0:
                    sub_list[i] += 1
                    break
        print("incremented lists")
        print(inc_result)
        for i in range(9):
            for j in range(9):
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                cell = driver.find_element(By.XPATH, cell_id)
                text = cell.get_attribute("data-value").strip()
                if i == 8 & j == 8:
                    self.stepPass(str(inc_result))
                if not text:
                    value = str(inc_result[i][j])
                    cell.send_keys(value)

    def validateSolution(self):

        self.stepPass(driver.find_element(By.XPATH, '//div[@id ="victory-screen"]//span[@id="well-done"]').text)
        self.stepInfo("Validate Sudoku Solving Time")
        solTime = driver.find_element(By.XPATH, '//div[@id="final-time-total"]').text
        self.stepPass("The total time to solve is " + solTime)
        self.stepInfo("End of execution")

    def captureGrid(self):
        sudoku_grid = driver.find_element(By.XPATH, '//div[@id="sudoku"]')
        with open('Sudoku_grid.png', 'wb') as file:
            sudoku_png = sudoku_grid.screenshot_as_png
            file.write(sudoku_png)

    def increment_list(self):
        """Increments the first 5 occurrences of 0 in the list"""
        count = 0
        for i, num in enumerate(lst):
            if num == 0:
                lst[i] += 1
                count += 1
            if count == 5:
                break
        return lst

    def compare_lists(self, lst1, lst2):
        """Compares two lists of lists and increments 0's in list1 that differ from list2"""
        print("Puzzle" + str(lst2))
        print("inclst" + str(lst1))
        for sub_list1, sub_list2 in zip(lst1, lst2):
            new_sub_list = []
            for num1, num2 in zip(sub_list1, sub_list2):
                if num1 == 0 and num1 != num2:
                    num1 = num2 + 1
                new_sub_list.append(num1)
            result.append(new_sub_list)
        print(str(result))
        return result

    list1 = [[0, 0, 0, 1, 9, 8, 7, 0, 6], [4, 0, 0, 0, 3, 0, 8, 0, 0], [0, 0, 0, 2, 0, 7, 0, 0, 0],
             [6, 0, 7, 0, 0, 0, 5, 0, 9], [8, 9, 0, 0, 0, 0, 0, 7, 2], [3, 0, 1, 0, 0, 0, 4, 0, 8],
             [0, 0, 0, 5, 0, 2, 0, 0, 0], [0, 0, 4, 0, 7, 0, 0, 0, 0], [9, 0, 6, 3, 1, 4, 0, 5, 0]]
    list2 = [[5, 3, 2, 1, 9, 8, 7, 4, 6], [4, 7, 9, 6, 3, 5, 8, 2, 1], [1, 6, 8, 2, 4, 7, 9, 3, 5],
             [6, 4, 7, 8, 2, 3, 5, 1, 9], [8, 9, 5, 4, 6, 1, 3, 7, 2], [3, 2, 1, 7, 5, 9, 4, 6, 8],
             [7, 1, 3, 5, 8, 2, 6, 9, 4], [2, 5, 4, 9, 7, 6, 1, 8, 3], [9, 8, 6, 3, 1, 4, 2, 5, 7]]

    def findinvalidCells(self):
        invalid_cell = "//div[@class='cell active invalid highlighted2']"
        invalidCells = driver.find_elements(By.XPATH, "//div[@class='cell invalid highlighted2']").count()
        cell = driver.find_element(By.XPATH, f"(//div[@class='cell invalid highlighted2']){invalidCells - 1}")
        j = driver.find_element(By.XPATH, invalid_cell).get_attribute("data-column")
        i = driver.find_element(By.XPATH, invalid_cell).get_attribute("data-row")
        driver.find_element(By.XPATH, invalid_cell).get_attribute("data-column and data-row")
        value = str(puzzle[i][j])
        cell.send_keys(value)

    def findErrorAndUndo(self):
        invalid_cell = "//div[@class='cell invalid highlighted2']"
        if (driver.find_elements(By.XPATH, invalid_cell) > 0):
            print("gh")
            driver.find_element(By.XPATH, "//div[@id='undo'']").click()

    def renterValues(self):
        empty_cell = "//div[@data-value='']"
        if (driver.find_elements(By.XPATH, empty_cell) > 0):
            # if (driver.find_element(By.XPATH, empty_cell).is_displayed()):
            i = driver.find_element(By.XPATH, empty_cell).get_attribute("data-row")
            j = driver.find_element(By.XPATH, empty_cell).get_attribute("data-column")
            driver.find_element(By.XPATH, empty_cell).send_keys(puzzle[i][j])

    def humanSudokuSolver(self, lst, solution):
        (i, j) = self.find(lst, 0)
        if (i, j) == (-1, -1):

            if lst == solution:
                print("Sudoku puzzle solved correctly!")
            else:
                print("Sudoku puzzle solved incorrectly.")
            return

        excludedNums = set()
        for row in range(0, 9):
            for col in range(0, 9):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])

        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for number in possibleNums:
            if number not in excludedNums:
                lst[i][j] = number
                row_num = i + 1
                col_num = j + 1
                # cell_id = f"cell-{row_num}-{col_num}"
                # cell = driver.find_element_by_id(cell_id)
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                cell = driver.find_element(By.XPATH, cell_id)
                # cell.send_keys(NUM_KEYS[number])
                cell.send_keys(number)
                self.sudokuSolver(lst, solution)
                cell.clear()  # Clear the cell after trying

                lst[i][j] = 0  # Reset the value after trying

    # Call the sudokuSolver function with the original grid and the correct solution
    # Replace `originalGrid` and `solution` with the appropriate values
    # originalGrid = [...]  # Replace with the original Sudoku grid
    # solution = [...]  # Replace with the correct solution
    # sudokuSolver(originalGrid, solution)
    tried_cells = set()

    def sudokuSolverHmn(self, lst):
        (i, j) = self.find(lst, 0)
        # print(str(i) +"__"+ str(j))
        if (i, j) == (-1, -1):
            return self.printSol(lst)
            # return
        excludedNums = set()
        for row in range(0, rows):
            for col in range(0, cols):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])
        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        original_value = lst[i][j]
        if original_value != 0:
            self.tried_cells.add((i, j))
        for number in possibleNums:
            if number not in excludedNums:
                lst[i][j] = number
                # print(str(i) + "__" + str(j))
                # print("value "+str(number))
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                if (i, j) not in self.tried_cells and original_value == 0:
                    print(str(i) + "__" + str(j))
                    print("value " + str(number))
                    self.tried_cells.add((i, j))
                    cell = driver.find_element(By.XPATH, cell_id)
                    # cell.send_keys(NUM_KEYS[number])
                    cell.send_keys(number)
                    solution = self.sudokuSolverHmn(lst)
                    if solution:
                        # print("Solution:")
                        print(solution)
                        # self.stepInfo("Solution:")
                        #
                        # self.stepPass(str(solution))
                        # self.stepPass(str(solution))
                        return solution
                    # cell.clear()
                    self.tried_cells.remove((i, j))
                # lst[i][j] = 0
                else:
                    solution = self.sudokuSolverHmn(lst)
                    if solution:
                        print(solution)
                        return solution
        lst[i][j] = original_value
        return None
        self.stepPass("Solved the sudoku grid")

    def fillGrid(self, lst):
        rows = len(lst)
        cols = len(lst[0])
        for i in range(rows):
            for j in range(cols):
                if lst[i][j] == 0:
                    excludedNums = set()
                    for row in range(rows):
                        for col in range(cols):
                            if lst[row][col] != 0:
                                if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                                    excludedNums.add(lst[row][col])
                    possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    for number in possibleNums:
                        if number not in excludedNums:
                            lst[i][j] = number
                            solution = self.sudokuSolver(lst)
                            if solution:
                                # Check if filled cell is red
                                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                                cell = driver.find_element(By.XPATH, cell_id)
                                if "red" in cell.get_attribute("class"):
                                    # If filled cell is red, fill with the second possible number
                                    cell.clear()
                                    cell.send_keys(possibleNums[1])
                                    solution = self.fillGrid(lst)
                                return solution
                            lst[i][j] = 0
                    return None
        return lst

    def fillGridNew(self, lst):
        rows = len(lst)
        cols = len(lst[0])
        for row in range(rows):
            for col in range(cols):
                if lst[row][col] == 0:
                    possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    for number in possibleNums:
                        if self.isValid(lst, row, col, number):
                            lst[row][col] = number
                            if self.isRed(lst, row, col):  # Check if the filled cell is red
                                continue  # Skip to the next number if it is red
                            if self.fillGridNew(lst):
                                return lst
                            lst[row][col] = 0  # Undo the filled number if it doesn't lead to a solution
                    return None
        return lst

    def isValid(self, lst, row, col, num):
        # Check if num is not in the same row, col, or 3x3 box
        for i in range(9):
            if (lst[row][i] == num) or (lst[i][col] == num) or (
                    lst[(row // 3) * 3 + i // 3][(col // 3) * 3 + i % 3] == num):
                return False
        return True

    def isRed(self, lst, row, col):
        print("REd")

    # identifies and fill red cells before completing grid
    def fillGridAndModify(self, lst):
        (i, j) = self.find(lst, 0)
        if (i, j) == (-1, -1):
            return self.printSol(lst)
        excludedNums = set()
        for row in range(0, rows):
            for col in range(0, cols):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])
        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        original_value = lst[i][j]
        if original_value != 0:
            self.tried_cells.add((i, j))
        for number in possibleNums:
            if number not in excludedNums:
                lst[i][j] = number
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                if (i, j) not in self.tried_cells and original_value == 0:
                    print(str(i) + "__" + str(j))
                    print("value " + str(number))
                    self.tried_cells.add((i, j))
                    cell = driver.find_element(By.XPATH, cell_id)
                    cell.send_keys(number)
                    solution = self.fillGridAndModify(lst)
                    if solution:
                        print(solution)
                        return solution
                    self.tried_cells.remove((i, j))
                else:
                    solution = self.fillGridAndModify(lst)
                    if solution:
                        print(solution)
                        return solution
        lst[i][j] = original_value

        # Check for red cells and fill them with remaining possible numbers
        red_cells = driver.find_elements(By.XPATH, "//div[contains(@class,'invalid2')]")
        for red_cell in red_cells:
            row = int(red_cell.get_attribute('data-row'))
            col = int(red_cell.get_attribute('data-column'))
            possible_nums = [num for num in possibleNums if num not in excludedNums]
            if possible_nums:
                lst[row][col] = possible_nums[0]
                red_cell.send_keys(possible_nums[0])
        return None

    def fillGridAndModify2(self, lst):
        (i, j) = self.find(lst, 0)
        if (i, j) == (-1, -1):
            return self.printSol(lst)
        excludedNums = set()
        for row in range(0, rows):
            for col in range(0, cols):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])
        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        original_value = lst[i][j]
        if original_value != 0:
            self.tried_cells.add((i, j))
        for number in possibleNums:
            if number not in excludedNums:
                lst[i][j] = number
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                if (i, j) not in self.tried_cells and original_value == 0:
                    print(str(i) + "__" + str(j))
                    print("value " + str(number))
                    self.tried_cells.add((i, j))
                    cell = driver.find_element(By.XPATH, cell_id)
                    cell.send_keys(number)
                    solution = self.fillGridAndModify2(lst)
                    if solution:
                        print(solution)
                        return solution
                    self.tried_cells.remove((i, j))
                else:
                    solution = self.fillGridAndModify2(lst)
                    if solution:
                        print(solution)
                        return solution
        lst[i][j] = original_value

        # Check for red cells and fill them with remaining possible numbers
        red_cells = driver.find_elements(By.XPATH, "//div[contains(@class,'invalid2')]")
        for red_cell in red_cells:
            row = int(red_cell.get_attribute('data-row'))
            col = int(red_cell.get_attribute('data-column'))
            possible_nums = [num for num in possibleNums if num not in excludedNums]
            if possible_nums:
                lst[row][col] = possible_nums[0]
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(row, col)
                cell = driver.find_element(By.XPATH, cell_id)
                cell.send_keys(possible_nums[0])
        return None

    def sudokuSolverHmn2(self, lst):
        (i, j) = self.find(lst, 0)
        if (i, j) == (-1, -1):
            return self.printSol(lst)
        excludedNums = set()
        for row in range(0, rows):
            for col in range(0, cols):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])
        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        original_value = lst[i][j]
        if original_value != 0:
            self.tried_cells.add((i, j))
        for number in possibleNums:
            if number not in excludedNums:
                lst[i][j] = number
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                if (i, j) not in self.tried_cells and original_value == 0:
                    self.tried_cells.add((i, j))
                    cell = driver.find_element(By.XPATH, cell_id)
                    cell.send_keys(str(number))
                    solution = self.sudokuSolverHmn2(lst)
                    if solution:
                        return solution
                    # cell.clear()
                    self.tried_cells.remove((i, j))
                else:
                    solution = self.sudokuSolverHmn2(lst)
                    if solution:
                        return solution
        lst[i][j] = original_value

        # Check for red cells and fill them
        red_cells = self.findRedCells()
        if red_cells:
            for cell in red_cells:
                row, col = cell
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(row, col)
                cell = driver.find_element(By.XPATH, cell_id)
                cell.send_keys(str(lst[row][col]))
        return None

    def areAllCellsFilled(self, lst):
        for row in range(rows):
            for col in range(cols):
                if lst[row][col] == 0:
                    return False
        return True

    def findRedCells(self):
        red_cells = []
        cells = driver.find_elements(By.XPATH, "//div[contains(@class,'invalid2')]")

        for cell in cells:
            row = int(cell.get_attribute('data-row'))
            col = int(cell.get_attribute('data-column'))
            red_cells.append((row, col))

        return red_cells

    def sudokuSolverHmn3(self, lst):
        (i, j) = self.find(lst, 0)
        if (i, j) == (-1, -1):
            return self.printSol(lst)
        excludedNums = set()
        for row in range(0, rows):
            for col in range(0, cols):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])
        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        original_value = lst[i][j]
        if original_value != 0:
            self.tried_cells.add((i, j))
        for number in possibleNums:
            if number not in excludedNums:
                lst[i][j] = number
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                if (i, j) not in self.tried_cells:
                    self.tried_cells.add((i, j))
                    cell = driver.find_element(By.XPATH, cell_id)
                    cell.send_keys(str(number))
                    solution = self.sudokuSolverHmn3(lst)
                    if solution:
                        return solution
                    # cell.clear()
                    self.tried_cells.remove((i, j))
                else:
                    solution = self.sudokuSolverHmn3(lst)
                    if solution:
                        return solution
        lst[i][j] = original_value

        # Check for red cells and fill them
        red_cells = self.findRedCells()
        if red_cells:
            for cell in red_cells:
                row, col = cell
                cell_id = "//div[@data-row='{}' and @data-column='{}']".format(row, col)
                cell = driver.find_element(By.XPATH, cell_id)
                cell.send_keys(str(lst[row][col]))
        return None

    def sudokuSolverHmn4(self, lst):
        # Create a list of lists to store possible numbers for each cell
        possible_nums = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]

        # Fill the possible numbers for cells with values
        for row in range(9):
            for col in range(9):
                if lst[row][col] != 0:
                    possible_nums[row][col] = set()

        # Function to update possible numbers for a cell
        def update_possible_nums(row, col, num):
            # Update possible numbers for the row
            for c in range(9):
                possible_nums[row][c].discard(num)
            # Update possible numbers for the column
            for r in range(9):
                possible_nums[r][col].discard(num)
            # Update possible numbers for the box
            box_row, box_col = row // 3 * 3, col // 3 * 3
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    possible_nums[r][c].discard(num)

        (i, j) = self.find(lst, 0)
        if (i, j) == (-1, -1):
            return self.printSol(lst)

        original_value = lst[i][j]
        if original_value != 0:
            self.tried_cells.add((i, j))
        for number in possible_nums[i][j]:
            lst[i][j] = number
            cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
            if (i, j) not in self.tried_cells and original_value == 0:
                self.tried_cells.add((i, j))
                cell = driver.find_element(By.XPATH, cell_id)
                cell.send_keys(str(number))
                update_possible_nums(i, j, number)
                solution = self.sudokuSolverHmn3(lst)
                if solution:
                    return solution
                # cell.clear()
                self.tried_cells.remove((i, j))
                update_possible_nums(i, j, number)
            else:
                solution = self.sudokuSolverHmn3(lst)
                if solution:
                    return solution
        lst[i][j] = original_value

        # Check if all empty cells are filled
        if self.find(lst, 0) == (-1, -1):
            # Generate the solution as a list of lists
            solution = [list(row) for row in lst]

            return solution

        return None

    def sudokuSolverHmn99(self, lst):
        (i, j) = self.findNew(lst, 0)
        if (i, j) == (-1, -1):
            return self.printSol(lst)

        excludedNums = set()
        for row in range(rows):
            for col in range(cols):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])

        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        original_value = lst[i][j]
        if original_value != 0:
            self.tried_cells.add((i, j))
        else:
            remaining_nums = [num for num in possibleNums if num not in excludedNums]
            if not remaining_nums:
                return None  # No remaining numbers, backtrack

            for possible_num in remaining_nums:
                lst[i][j] = possible_num  # Fill the current empty cell with a possible number

                if (i, j) not in self.tried_cells and original_value == 0:
                    cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                    print(str(i) + "__" + str(j))
                    print("value " + str(lst[i][j]))
                    self.tried_cells.add((i, j))
                    cell = driver.find_element(By.XPATH, cell_id)
                    cell.send_keys(lst[i][j])

                if self.sudokuSolverHmn99(lst):
                    return self.sudokuSolverHmn99(lst)

                if (i, j) not in self.tried_cells and original_value == 0:
                    self.tried_cells.remove((i, j))

                lst[i][j] = 0  # Reset the value of the current cell to 0 and backtrack
        # self.stepPass("Filled the empty cells with possible values")
        return None

    def sudokuSolverParallel(self, lst):
        (i, j) = self.findNew(lst, 0)
        if (i, j) == (-1, -1):
            return self.printSol(lst)

        excludedNums = set()
        for row in range(rows):
            for col in range(cols):
                if lst[row][col] != 0:
                    if i == row or j == col or (i // 3 == row // 3 and j // 3 == col // 3):
                        excludedNums.add(lst[row][col])

        possibleNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        original_value = lst[i][j]
        if original_value != 0:
            self.tried_cells.add((i, j))
        else:
            remaining_nums = [num for num in possibleNums if num not in excludedNums]
            if not remaining_nums:
                return None  # No remaining numbers, backtrack

            for possible_num in remaining_nums:
                lst[i][j] = possible_num  # Fill the current empty cell with a possible number

                if (i, j) not in self.tried_cells and original_value == 0:
                    cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                    self.stepInfo("Filling cell ({}, {}) with value {}".format(i, j, lst[i][j]))
                    self.tried_cells.add((i, j))
                    cell = driver.find_element(By.XPATH, cell_id)
                    cell.send_keys(str(lst[i][j]))

                if self.sudokuSolverParallel(lst):
                    return self.sudokuSolverParallel(lst)

                if (i, j) not in self.tried_cells and original_value == 0:
                    self.tried_cells.remove((i, j))

                lst[i][j] = 0  # Reset the value of the current cell to 0 and backtrack

                if original_value == 0:
                    cell_id = "//div[@data-row='{}' and @data-column='{}']".format(i, j)
                    self.stepInfo("Resetting cell ({}, {}) to 0".format(i, j))
                    cell = driver.find_element(By.XPATH, cell_id)
                    cell.clear()

        return None

    def excludedNums(self, row, col, lst):
        excluded = set()
        for r in range(rows):
            for c in range(cols):
                if lst[r][c] != 0 and (row == r or col == c or (row // 3 == r // 3 and col // 3 == c // 3)):
                    excluded.add(lst[r][c])
        return excluded

    def findNew(self, lst, value):
        for r in range(rows):
            for c in range(cols):
                if lst[r][c] == value:
                    return r, c
        return -1, -1

    def findWOValue(self, lst):
        for i in range(9):
            for j in range(9):
                if lst[i][j] == 0:
                    return i, j
        return -1, -1

    def isSafe(self, lst, row, col, num):
        for i in range(9):
            if lst[row][i] == num:
                return False
            if lst[i][col] == num:
                return False
            if lst[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
                return False
        return True

    def enter_value(self, row, col, num):
        # cell = self.driver.find_element(By.XPATH, f"//div[@class='cell'][{row + 1}][{col + 1}]")
        cell = driver.find_element(By.XPATH, "//div[@data-row='{}' and @data-column='{}']".format(row, col))
        # cell_id = "//div[@data-row='{}' and @data-column='{}']".format(row + 1, col + 1)
        cell.send_keys(str(num))

    def clear_value(self, row, col):
        # cell = self.driver.find_element(By.XPATH, f"//div[@class='cell'][{row + 1}][{col + 1}]")
        cell = driver.find_element(By.XPATH,
                                   "//div[@data-row='{}' and @data-column='{}']".format(row + 1, col + 1))
        cell.clear()

    def sudokuSolverHmn991(self, lst):
        row, col = self.findWOValue(lst)
        if row == -1 and col == -1:
            return True
        for num in range(1, 10):
            if self.isSafe(lst, row, col, num):
                lst[row][col] = num
                self.enter_value(row, col, num)
                if self.sudokuSolverHmn991(lst):
                    return True
                lst[row][col] = 0
                # self.clear_value(row, col)
        return False

    def solveSudokuHuman(self, lst):
        self.sudokuSolverHmn991(lst)
        return lst

    def checkForInvalidCells(self):
        print("")
        invalidcells = driver.find_elements(By.XPATH, "//div[contains(@class,'cell invalid')]")
        if len(invalidcells) > 0:
            self.stepInfo("The Sudoku grid has some invalid numbers")
            invalid_cells_list = []
            for cell in invalidcells:
                row = int(cell.get_attribute('data-row'))
                col = int(cell.get_attribute('data-column'))
                invalid_cells_list.append((row, col))
            print(str(invalid_cells_list))
            self.stepFail("The invalid numbers present in the cells" + str(invalid_cells_list))
        else:
            self.stepPass("The Sudoku grid doesn't have any invalid numbers")


