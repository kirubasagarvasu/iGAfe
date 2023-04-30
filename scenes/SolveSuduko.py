# from airtest.core.api import *
# # from iGafe.base.BaseClass import BaseClass
# # from iGafe.keywords.GUIKeywordsClass import GUIKeywords
# from poco.drivers.unity3d import UnityPoco
# from base.BaseClass import BaseClass
# from keywords.GUIKeywordsClass import GUIKeywords
#
# M = 9
# box = []
#  poco = UnityPoco()
# class SolveSuduko(BaseClass):
#
#     obj = None
#     keyword = None
#
#
#     def __init__(self, obj):
#         self.testResults = obj.testResults
#         self.currentTest = obj.currentTest
#         self.obj = obj
#         self.keyword = GUIKeywords(obj)
#
#     def puzzle(self, a):
#         for i in range(M):
#             for j in range(M):
#                 print(a[i][j], end=" ")
#                 box.append(a[i][j])
#             print()
#         return box
#
#     def solve(self, grid, row, col, num):
#         for x in range(9):
#             if grid[row][x] == num:
#                 return False
#
#         for x in range(9):
#             if grid[x][col] == num:
#                 return False
#
#         startRow = row - row % 3
#         startCol = col - col % 3
#         for i in range(3):
#             for j in range(3):
#                 if grid[i + startRow][j + startCol] == num:
#                     return False
#         return True
#
#     def Suduko(self, grid, row, col):
#         if (row == M - 1 and col == M):
#             return True
#         if col == M:
#             row += 1
#             col = 0
#         if grid[row][col] > 0:
#             return self.Suduko(grid, row, col + 1)
#         for num in range(1, M + 1, 1):
#
#             if self.solve(grid, row, col, num):
#
#                 grid[row][col] = num
#                 if self.Suduko(grid, row, col + 1):
#                     return True
#             grid[row][col] = 0
#         return False
#
#
#     def getSudukoData(self):
#         cell = []
#         j = 0
#         for u in range(3):
#             a = 0
#             for v in range(3):
#                 for x in range(1):
#                     i = 0
#                     for z in range(3):
#                         b = 0
#                         parentGrid = str(i) + "x" + str(j)
#                         print("\n grid :" + parentGrid)
#                         for y in range(3):
#                             childGrid = str(b) + "x" + str(a)
#                             print(childGrid, end=" ")
#                             if poco("Board").child(parentGrid).child(childGrid).child("Value").get_text() == "":
#                                 cell.append("0")
#                             else:
#                                 cell.append(poco("Board").child(parentGrid).child(childGrid).child("Value").get_text())
#                             b = b + 1
#                         i = i + 1
#                     print("\n")
#                 a = a + 1
#             j = j + 1
#         return cell
#
#     def solveSuduko(self, gridCells):
#         j = 0
#         cell = 0
#         for u in range(3):
#             a = 0
#             for v in range(3):
#                 for x in range(1):
#                     i = 0
#                     for z in range(3):
#                         b = 0
#                         parentGrid = str(i) + "x" + str(j)
#                         print("\n grid :" + parentGrid)
#                         for y in range(3):
#                             childGrid = str(b) + "x" + str(a)
#                             print(childGrid, end=" ")
#                             if poco("Board").child(parentGrid).child(childGrid).child("Value").get_text() == "":
#                                 poco("Board").child(parentGrid).child(childGrid).child("Value").click()
#                                 print(str(gridCells[cell]))
#                                 poco(str(gridCells[cell])).click()
#                                 cell = cell + 1
#                             else:
#                                 cell = cell + 1
#                             b = b + 1
#                         i = i + 1
#                     print("\n")
#                 a = a + 1
#             j = j + 1
#
#     def selectSudoku(self):
#             poco("Button (Select Level)").click()
#             poco("Button (New Game)").click()
#
