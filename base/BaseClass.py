import logging
import time

from utilities.ReportingEngine import ReportingEngine


class BaseClass(ReportingEngine):

    def BeforeAll(self, game, driver):

        self.createReportDirectory()
        self.addStartTime(game)

        # connect device and start Application
        driver.setUpConnection() #for mobile
        # driver.startApp("com.fingersoft.hillclimb")
        # driver.startApp("com.MaciejKitowski.Sudoku")

    def BeforeTest(self, testID, testDescription):
        self.addTest(testID, testDescription)


    def AfterAll(self, driver):
        # driver.stopApp("com.fingersoft.hillclimb")
        # driver.stopApp("com.MaciejKitowski.Sudoku")
        self.addEndTime()
        self.generateReport()
