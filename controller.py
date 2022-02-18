from models.pages.announcement_page import AnnouncementPage
from models.pages.attendance_page import AttendancePage, invalidCredential
from views.automater_view import MainWindow,LoginWindow
from selenium_header import *
import json
import logging
import os
import shutil

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
            logging.info("Failed Login! Running log in window...")
            self.runLoginWindow()
        else:
            logging.info("Login successfully! Running main window!")
            self.runMainWindow()

    def initUserJson(self):
        directory_list = os.listdir("json")
        logging.info("Checking if userinfo.json exist...")
        if "userinfo.json" not in directory_list:
            logging.info("Initializing userinfo.json")
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
        logging.info("Starting login window...")
        self.loginWin = LoginWindow()
        self.loginWin.show()
        self.loginWin.submitted.connect(self.getIdPwLW)
        self.loginWin.submitted.connect(self.loginWithGUI)

    def updateSubjectBox(self):
        logging.info("Updating the subject box!")
        with open(f"json\\{self.userId}_subject_info.json", "r") as js:
            subjectList = json.load(js).keys()

        self.mainWindow.insertToSubjectBox(subjectList)

    def updateDateBox(self, subject):
        logging.info(f"User selected {subject}, updating the date combobox...")
        self.mainWindow.dateBox.clear()
        self.mainWindow.dateBox.addItem("-")
        if subject == "-":
            return
        with open(f"json\\{self.userId}_subject_info.json","r") as js:
            subjectDict = json.load(js)
        
        date = subjectDict[subject]["announcements"].keys()
        logging.info("Sucessfully updated the date box!")
        self.mainWindow.insertToDateBox(date)

    def updateNumberOfNewAnnouncements(self):
        """
        This function update the number of new annonucements.
        """
        logging.info("Updating the new announcement label!")
        with open(f"json\\{self.userId}_subject_info.json","r") as js:
            subjectDict = json.load(js)
        
        string = ""
        for subject in subjectDict.keys():
            numberOfNew = len(subjectDict[subject]["dateOfNew"])
            if numberOfNew > 0:
                string += f"{subject} - {numberOfNew}\n"
        
        if not string:
            string = "No New Announcements!"
        
        logging.info("Successfully updated the new announcement label!")
        self.mainWindow.updateNumerOfNewAnnouncement(string)


    def updateAnnouncement(self, subject, date):
        """
        This function update the desired announcement to the text box.
        """
        logging.info(f"Grabbing the announcement of {subject} on {date}...")
        if subject == "-" or date == "-":
            self.mainWindow.insertToDisplay("Invalid Option Selected!")
            return
        
        with open(f"json\\{self.userId}_subject_info.json","r") as js:
            subjectDict = json.load(js)
        
        string = ""
        for i in subjectDict[subject]["announcements"][date]:
            string += i
            string += "\n---------------------------------------------\n"
        
        logging.info(f"Successfully updated the announcement to the text box.")
        self.mainWindow.insertToDisplay(string)


    def updateNewAnnouncement(self):
        """
        This function update the new announcement to the text box.
        """
        logging.info("Grabbing all the new announcements...")
        if self.mainWindow.numberOfNew.toPlainText() == "No New Announcements!":
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
        
        logging.info("Successfully updated the new announcement in the text box!")
        self.mainWindow.insertToDisplay(string)

    def takeAttendance(self):
        userinfo = self.getIdPw()
        attendance_page = AttendancePage(chrome,userinfo[0],userinfo[1])
        logging.info("Initializing attendance page...")
        attendance_page.qrcode_read()
        logging.info("Reading QR Code and converting it to the links....")
        try:
            resultGenerator = attendance_page.takeAttendance()
            firstLabel = next(resultGenerator)
            logging.info(f"Links provided in QR Code returned: {firstLabel}")
            #Clearing the widgets only before the first QR
            self.mainWindow.attendanceWindow.clearWidgets()
            self.mainWindow.attendanceWindow.insertLabel("If you see your name that means attendance has been taken.")
            self.mainWindow.attendanceWindow.insertLabel(firstLabel)

            for i in resultGenerator:
                logging.info(f"Links provided in QR Code returned: {i}")
                self.mainWindow.attendanceWindow.insertLabel(i)                

        except invalidCredential:
            self.mainWindow.attendanceWindow.close()
            self.mainWindow.close()
            self.runLoginWindow()
            self.loginWin.loginMessageBox(False)


    def initAttendanceSlot(self):
        """
        This function handles the signal and slot thing between attendance page and the GUI.
        """
        self.mainWindow.attendanceWindow.takeAttendance.connect(self.takeAttendance)

    def logOut(self):
        self.mainWindow.close()
        logging.info("Closing Main Window and starting Log In Window...")
        self.runLoginWindow()
    
    def resetAutomator(self):
        logging.info("Reseting Automator, the json files will be reinitialized....")
        self.mainWindow.close()
        shutil.rmtree("json")
        os.mkdir("json")
        self.runLoginWindow()

    def runMainWindow(self):
        """
        This function start the main window and initialize its slots.
        """
        logging.info("Starting Main Window and initializing its slots...")
        self.mainWindow = MainWindow() 
        self.updateNumberOfNewAnnouncements()
        self.updateSubjectBox()
        self.mainWindow.show()
        self.mainWindow.subjectChanged.connect(self.updateDateBox)
        self.mainWindow.viewAnnouncement.connect(self.updateAnnouncement)
        self.mainWindow.viewNewAnnouncement.connect(self.updateNewAnnouncement)
        self.mainWindow.takeAttendance.connect(self.initAttendanceSlot)
        self.mainWindow.logOut.connect(self.logOut)
        self.mainWindow.reset.connect(self.resetAutomator)
        logging.info("Successfully intialized the slot.")
    

    def start(self):
        """
        This function start the main controller.
        """
        self.initUserJson()
        userinfo = self.getIdPw()
        logging.info("Grabbing user id and password from userinfo.json in order to log in...")
        # try:
        #     if userinfo: 
        #         logging.info("Attempting to login with the user id and password provided from userinfo.json")
        #         self.login(userinfo)
        #     else:
        #         logging.info("userinfo.json contains no user information! Starting login window...")
        #         self.runLoginWindow()
        # except Exception as exception:
        #     execpt = type(exception).__name__
        #     logging.error(f"{execpt} has been thrown by the application! Exiting program...")
        #     print(f"\nSomething went wrong! {execpt}\n")
        if userinfo: 
            logging.info("Attempting to login with the user id and password provided from userinfo.json")
            self.login(userinfo)
        else:
            logging.info("userinfo.json contains no user information! Starting login window...")
            self.runLoginWindow()


        
        
            
        

        


