from models.pages.announcement_page import AnnouncementPage
from models.pages.attendance_page import AttendancePage, invalidCredential
from views.automater_view import MainWindow,LoginWindow
from selenium_header import *
import json
import logging
import os


class Controller():
    def __init__(self):
        self.browser = chrome 

    def loginWithGUI(self,userId,userPw):
        self.userId = userId
        self.announcementPage = AnnouncementPage(chrome,userId,userPw)
        isLogin = self.announcementPage.announcementLogin()
        if isLogin:
                self.loginWin.loginMessageBox(True)
                self.loginWin.close()
                self.runMainWindow()
        else:
                self.loginWin.loginMessageBox(False)
    
    def login(self, userinfo):
        self.userId, userPw= userinfo
        self.announcementPage = AnnouncementPage(chrome,self.userId,userPw)
        isLogin = self.announcementPage.announcementLogin()
        if not isLogin:
            self.runLoginWindow()
        else:
            self.runMainWindow()

    def initUserJson(self):
        directory_list = os.listdir("json")
        if "userinfo.json" not in directory_list:
            logging.info(f"Creating userinfo.json")
            with open(f"json\\userinfo.json", "w") as js:
                string = "{\"username\" : \"\" , \"password\" : \"\"}"
                js.write(string)


    def getIdPw(self): 
        """
        This function essentially asks for username and password, if it isn't exist in the json file.
        """
        has_info = False
        with open("json\\userinfo.json","r") as json_file:
            userinfo = json.load(json_file)
            if userinfo["username"] and userinfo["password"]:
                has_info = True
            
        if not has_info:
            return []

        return [userinfo["username"],userinfo["password"]]
    
    def getIdPwLW(self, userid, pw):
        userinfo = {
            "username" : userid,
            "password" : pw
        }
        with open("json\\userinfo.json","w") as json_file:
            json.dump(userinfo,json_file)

        return [userinfo["username"], userinfo["password"]]

    def runLoginWindow(self):
        self.loginWin = LoginWindow()
        self.loginWin.show()
        self.loginWin.submitted.connect(self.getIdPwLW)
        self.loginWin.submitted.connect(self.loginWithGUI)

    def updateSubjectBox(self):
        with open(f"json\\{self.userId}_subject_info.json", "r") as js:
            subjectList = json.load(js).keys()

        self.mainWindow.insertToSubjectBox(subjectList)

    def updateDateBox(self, subject):
        self.mainWindow.dateBox.clear()
        self.mainWindow.dateBox.addItem("-")
        if subject == "-":
            return
        with open(f"json\\{self.userId}_subject_info.json","r") as js:
            subjectDict = json.load(js)
        
        date = subjectDict[subject]["announcements"].keys()
        self.mainWindow.insertToDateBox(date)

    def updateNumberOfNewAnnouncements(self):
        with open(f"json\\{self.userId}_subject_info.json","r") as js:
            subjectDict = json.load(js)
        
        string = ""
        for subject in subjectDict.keys():
            numberOfNew = len(subjectDict[subject]["dateOfNew"])
            if numberOfNew > 0:
                string += f"{subject} - {numberOfNew}\n"
        
        if not string:
            string = "No New Announcements!"
        
        self.mainWindow.updateNumerOfNewAnnouncement(string)


    def updateAnnouncement(self, subject, date):
        if subject == "-" or date == "-":
            self.mainWindow.insertToDisplay("Invalid Option Selected!")
            return
        
        with open(f"json\\{self.userId}_subject_info.json","r") as js:
            subjectDict = json.load(js)
        
        string = ""
        for i in subjectDict[subject]["announcements"][date]:
            string += i
            string += "\n---------------------------------------------\n"
        
        self.mainWindow.insertToDisplay(string)


    def updateNewAnnouncement(self):
        if self.mainWindow.numberOfNew.text() == "No New Announcements!":
            self.mainWindow.insertToDisplay("There is no new announcement for today!")
            return

        with open(f"json\\{self.userId}_subject_info.json","r") as js:
            subjectDict = json.load(js)
        
        string = ""
        for subjectName in subjectDict:
            string += f"---------------\n{subjectName}\n---------------\n"
            for i in subjectDict[subjectName]["dateOfNew"]:
                for j in subjectDict[subjectName]["announcements"][i]:
                    string += j
                    string += "\n---------------------------------------------\n"
            string += "\n\n\n\n\n"
        
        self.mainWindow.insertToDisplay(string)

    def takeAttendance(self):
        userinfo = self.getIdPw()
        attendance_page = AttendancePage(chrome,userinfo[0],userinfo[1])
        attendance_page.qrcode_read()
        try:
            resultGenerator = attendance_page.takeAttendance()
            firstLabel = next(resultGenerator)
            #Clearing the widgets only before the first QR
            self.mainWindow.attendanceWindow.clearWidgets()
            self.mainWindow.attendanceWindow.insertLabel(firstLabel)

            for i in resultGenerator:
                self.mainWindow.attendanceWindow.insertLabel(i)                

        except invalidCredential:
            self.mainWindow.attendanceWindow.close()
            self.mainWindow.close()
            self.runLoginWindow()
            self.loginWin.loginMessageBox(False)



    def initAttendanceSlot(self):
        self.mainWindow.attendanceWindow.takeAttendance.connect(self.takeAttendance)


    def runMainWindow(self):
        self.mainWindow = MainWindow() 
        self.updateNumberOfNewAnnouncements()
        self.updateSubjectBox()
        self.mainWindow.show()
        self.mainWindow.subjectChanged.connect(self.updateDateBox)
        self.mainWindow.viewAnnouncement.connect(self.updateAnnouncement)
        self.mainWindow.viewNewAnnouncement.connect(self.updateNewAnnouncement)
        self.mainWindow.takeAttendance.connect(self.initAttendanceSlot)
    

    def start(self):
        self.initUserJson()
        userinfo = self.getIdPw()
        if userinfo: 
            self.login(userinfo)
        else:
            self.runLoginWindow()
        
        
            
        

        


