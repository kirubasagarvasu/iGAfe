import shutil
from datetime import datetime
import json
import os
from airtest.core.api import *
from pathlib import Path
from shutil import copy


class ReportingEngine():
    startTime = None
    EndTime = None
    reportFolder = ''
    screenShotNum = 1
    grandparent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

    testResults = {
        "Tests": [],
        "Total_TC_Count": 0,
        "Passed_TC_Count": 0,
        "Failed_TC_Count": 0,
        "Game": "",
        "StartTime": "",
        "EndTime": "",
        "Duration": ""
    }

    currentTest = {
        "ID": "",
        "Description": "",
        "Status": "Pass",
        "Steps": []
    }

    def createReportDirectory(self):
        ReportingEngine.reportFolder = str(datetime.now().strftime("Report_%b_%d_%Y_%I_%M_%S_%p"))
        parent_dir = self.grandparent_dir + r"\Report"
        src_path = self.grandparent_dir + r"\iGafe\resources\report"
        dst_path = os.path.join(parent_dir, ReportingEngine.reportFolder)
        shutil.copytree(src_path, dst_path)

    def addStartTime(self, game):
        self.testResults['Game'] = game
        self.startTime = datetime.today()
        self.testResults['StartTime'] = str(self.startTime)

    def addEndTime(self):
        self.EndTime = datetime.today()
        self.testResults['EndTime'] = str(self.EndTime)
        duration = str(self.EndTime - self.startTime)
        h, m, s = duration.split(':')
        self.testResults['Duration'] = (h + ' hr ' if int(h) > 0 else '') + (m + ' min ' if int(m) > 0 else '') + \
                                       s.split('.')[0] + ' sec'

    def addTest(self, testID, testDescription):
        test = {
            "ID": testID,
            "Description": testDescription,
            "Status": "Pass",
            "Steps": []
        }
        self.currentTest = test
        self.testResults['Tests'].append(test)
        self.testResults['Total_TC_Count'] += 1

    def stepInfo(self, stepDescription):
        self.addStep(stepDescription, "Info")
        print("\033[1m" + "\033[36m" + stepDescription + "\033[0m")

    def stepPass(self, stepDescription):
        self.addStep(stepDescription, "Pass")
        print("\033[32m" + stepDescription + "\033[0m")

    def stepFail(self, stepDescription):
        self.addStep(stepDescription, "Fail")
        print("\033[91m" + stepDescription + "\033[0m")

    def addStep(self, stepDescription, stepStatus):
        step = None
        if stepStatus == 'Info':
            step = {
                "Description": stepDescription,
                "Status": stepStatus,
                "ScreenshotPath": ''}
            self.currentTest["Steps"].append(step)
        else:
            snapshot(
                filename=self.grandparent_dir + r"\Report/" + ReportingEngine.reportFolder + '\screenshots/' + self.currentTest[
                    'ID'] + '_' + str(self.screenShotNum) + '.png', msg="test")
            step = {
                "Description": stepDescription,
                "Status": stepStatus,
                "ScreenshotPath": 'screenshots/' + self.currentTest['ID'] + '_' + str(self.screenShotNum) + '.png'}
            self.screenShotNum += 1
            self.currentTest["Steps"].append(step)

    def generateReport(self):
        self.generateJSONReport()
        self.generateHTMLReport()

    def generateJSONReport(self):

        for tc in self.testResults['Tests']:
            # tcID = tc['ID']
            if len([step for step in tc['Steps'] if step['Status'] == 'Fail']) > 0:
                tc['Status'] = 'Fail'
                self.testResults['Failed_TC_Count'] += 1
            else:
                self.testResults['Passed_TC_Count'] += 1

        json_object = json.dumps(self.testResults, indent=4)
        with open("../../Report/" + ReportingEngine.reportFolder + "/results.json", "w") as outfile:
            outfile.write(json_object)

    def generateHTMLReport(self):

        section = ""

        index = 1
        for tc in self.testResults['Tests']:
            if tc['Status'] == 'Pass':
                section += '''<input type="radio" name="accordion" id="cb''' + str(index) + '''" />
                            <section class="box">
                            <label class="box-title passedTitle" style='color:green;' for="cb''' + str(index) + '''">
                            <img src='Logos/car_status.png' class='indiumLogoNew' width=auto height='25' style='vertical-align:middle;' />
                            ''' + tc['ID'] + ' : ' + tc['Description'] + '''</label>
                            <label class="box-close" for="acc-close"></label>
                            <div class="box-content">
                            '''
            else:
                section += '''<input type="radio" name="accordion" id="cb''' + str(index) + '''" />
                            <section class="box">
                             <label class="box-title failedTitle" style='color:red;' for="cb''' + str(index) + '''">
                            <img src='Logos/car_status.png' class='indiumLogoNew' width=auto height='25' style='vertical-align:middle; transform: rotate(160deg);' />
                            ''' + tc['ID'] + ' : ' + tc['Description'] + '''</label><label class="box-close" for="acc-close"></label>
                            <div class="box-content">
                            '''

            section += '''<table class='stepsTable'>
                            <thead>
                                <tr>
                                <th style='width:50px; padding: 10px; width: 10%;'>Sl. No</th>
                                <th style='text-align:left;padding-left: 20px; width: 70%;'>Description</th>
                                <th style='text-align:left; width: 20%;'>Status</th>
                                </tr>
                            </thead>
                            <tbody>'''

            stepNum = 1
            for step in tc['Steps']:
                stepColor = 'green' if step['Status'] == 'Pass' else ('red' if step['Status'] == 'Fail' else 'blue')
                stepNumber = str(stepNum) if step['Status'] != 'Info' else ''
                screenshotPath = step['ScreenshotPath']
                hasScreenshot = True if len(screenshotPath) > 0 else False
                section += '''<tr style='height:30px;'>                                <td style='color:''' + stepColor + ''';'>''' + stepNumber + '''</td><td style='text-align:left;padding-left: 20px; color:''' + stepColor + ''';'>''' + \
                           step[
                               'Description'] + '''</td>    <td style='text-align:left; color:''' + stepColor + ''';'>''' + \
                           step['Status'] + '''</td>'''
                if hasScreenshot:
                    section += '''<td style='text-align:center;'>''' + '''<a class="viewScreenshot" style="color:blue" target="_blank" href="''' + screenshotPath + '''">''' + '''<img class="imgcapture" src="Logos/screenshot.png" width="25" height="25">''' + '''</a>   <div class="image_preview" style='box-shadow: 0px 0px 15px ''' + stepColor + ''';'>   <img src="''' + screenshotPath + '''">    </div>                    </td>'''
                    section += '''</tr>'''
                stepNum += 1 if step['Status'] != 'Info' else 0

            section += '''</tbody>
				        </table>
                        </div>
		                </section>'''

            index += 1

        html = '''<html>

                <link rel='stylesheet' type='text/css' href='./Extras/styleCopy.css'>
                     <link rel='stylesheet' id='themeStylesheetLink' type='text/css' href='./Extras/themes/forest.css'>
                
                </br>
                <title>HTML REPORTING</title>
                <body >          

                
                </div>
                    <div id='headerDiv' style=''>
                        <div id='header' >
                            <img src='Logos/Indium-Software-Logo.png' class='indiumLogoNew' width=auto height='75' /> <img src='Logos/client_logo.png' class='clientLogoNew' width=auto height='75' />
                            <h1 style='color:white; '>iGAFE - Game Automation Report</h1>
                        </div>
                    </div>
                        
                    <div id='forest'>
                        <div class="forest"></div>
                        
                        <div class="forest-background"></div>
                        <div class="car-container">
                            <img src="Logos/car.png" alt="car">
                        </div>
                        
                    </div>

                    <div class='container'>
                    <div id='ddb'>
                        <p class='ddb'><strong>Date:</strong> ''' + str(datetime.today().strftime('%d-%m-%Y')) + '''
                        &ensp;&ensp;&ensp;&ensp;&ensp;<span><strong>Game:</strong> ''' + self.testResults['Game'] + ''' </span>
                        <span><strong>Duration:</strong> ''' + self.testResults['Duration'] + ''' </span></p>
                    </div>
                    <hr width='65%' color='#024073' style=' width: 60%; margin-top: 2%; height:0.4px; background-color: #e5e5e5; border: none;'>
                    
                    <nav class="accordion arrows">
                        <header class="box">
                            <label for="acc-close" class="box-title">Test Execution Report -&ensp;&ensp;&ensp;
                            Total: ''' + str(self.testResults['Total_TC_Count']) + '&ensp;&ensp;&ensp;' + '''
                            <img src='Logos/car_status.png' class='indiumLogoNew' width=auto height='35' style='vertical-align:middle; display:none;' />
                            Passed: ''' + str(self.testResults['Passed_TC_Count']) + '&ensp;&ensp;&ensp;' + ''' 
                            <img src='Logos/car_status.png' class='indiumLogoNew' width=auto height='35' style='vertical-align:middle; display:none; transform: rotate(160deg);' />
                            Failed: ''' + str(self.testResults['Failed_TC_Count']) + '''
                            </label>
                        </header>''' + section + '''
                        <input type="radio" name="accordion" id="acc-close" />
                    </nav>
                    </div>
                    
                    
                    
                </body>
                <script type='text/javascript' src='./Extras/canvasjs.min.js'></script>
                </html>'''

        with open("../../Report/" + ReportingEngine.reportFolder + "/Report.html", "w") as outfile:
            outfile.write(html)
