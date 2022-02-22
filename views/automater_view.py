from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QPushButton,
                             QHBoxLayout,
                             QVBoxLayout,
                             QLabel,
                             QDialog,
                             QGroupBox,
                             QComboBox,
                             QTextEdit,
                             QLineEdit,
                             QMessageBox)
import sys

from numpy import true_divide

mainWindow = """

#mainWidget{
    background-color : #555555;
}

QLabel{
    color : white;
}

QLabel#titleText{
    font-size : 25px;
    font-weight: bold;
}

#subjectLabel, #dateLabel, #newAnnouncementLabel{
    font-size: 14px;
    font-weight : bold;
    text-align : center;
}


QPushButton{   
    background-color: #F3CA20;
    color : white;
    border-radius : 12px;
    font-weight: bold;
    font-size : 15px;
    margin : 5px;
  
}

QPushButton#attendanceButton{
    font-size: 18px;
}

QPushButton:hover{
    background-color : #EDDD6D;
}

QTextEdit{
    background-color : #474747;
    color : white;
    border-radius : 10px;
    padding: 10px;
    font-size : 15px;
    margin-right : 10px;
}

QGroupBox{
    color : white;
    font-size : 18px;
    font-weight : bold;
    border-color : black;
}

QComboBox{
    background-color : #474747;
    color : white;
    border-radius : 10px;
    padding : 3px;
}
"""

dialog = """
QWidget{
    background-color : #555;
    color : white;
}

"""

loginWin ="""
QWidget{
    background-color : #555;
    color : white;
}

QLineEdit{
    background-color : #474747;
    border-radius: 10px;
    font-size : 15px;
    height : 30px;
    padding : 5px;
}

QPushButton{   
    background-color: #F3CA20;
    color : white;
    border-radius : 12px;
    font-weight: bold;
    font-size : 18px;
    margin-right : 10px;
  
}


QPushButton:hover{
    background-color : #EDDD6D;
}
"""

class MainWindow(QMainWindow):
    subjectChanged = QtCore.pyqtSignal(str)
    viewAnnouncement = QtCore.pyqtSignal(str,str)
    viewNewAnnouncement = QtCore.pyqtSignal(bool)
    takeAttendance = QtCore.pyqtSignal(bool)
    logOut = QtCore.pyqtSignal(bool)
    reset = QtCore.pyqtSignal(bool)

    def __init__(self):
        super(MainWindow,self).__init__()
        self.setWindowIcon(QtGui.QIcon("mmulogo.ico"))
        self.setFixedSize(1000, 900)
        self.setWindowTitle("MMLS Automater - 3.0")
        self._initUI()
        self.setStyleSheet(mainWindow)


    def _initUI(self):
        self._initMenu()
        self._initMainLayout()
        self._initAttendanceWidgets()
        self._initAnnouncementWidgets()

    def insertToDisplay(self,text):
        self.displayOutput.setText("")
        self.displayOutput.insertPlainText(text)
    
    def insertToSubjectBox(self,array):
        self.subjectBox.addItems(array)
    
    def insertToDateBox(self,array):
        self.dateBox.addItems(array)

    def updateNumerOfNewAnnouncement(self,text):
        self.numberOfNew.insertPlainText(text)
        self.numberOfNew.adjustSize()
    
    def on_subjectChanged(self):
        self.subjectChanged.emit(
            self.subjectBox.currentText()
        )
    
    def on_viewAnnouncement(self):
        self.viewAnnouncement.emit(
            self.subjectBox.currentText(),
            self.dateBox.currentText()
        )

    def on_viewNewAnnouncement(self):
       self.viewNewAnnouncement.emit(
           True
       ) 
    
    def on_openAttendanceWindow(self):
        self.attendanceWindow = AttendanceWindow()
        self.takeAttendance.emit(
            True
        )
        self.attendanceWindow.show()

    def on_report(self):
        self.dialogBox = QDialog()
        self.dialogBox.setWindowIcon(QtGui.QIcon("mmulogo.ico"))
        self.dialogBox.setStyleSheet(dialog)
        #deal with the "?"
        self.dialogBox.setWhatsThis("Hi there!")
        self.dialogBox.setWindowTitle("About The Application")
        self.dialogBox.setFixedSize(400,280)
        layout = QVBoxLayout()
        self.dialogBox.setLayout(layout)

        layout.addStretch()
        titleFont = QtGui.QFont("Normal",13)
        titleFont.setBold(True)
        titleFont.setUnderline(True)
        descFont = QtGui.QFont("Normal",10)

        title = QLabel()
        title.setText("Found Bugs? Report It!")        
        title.setFont(titleFont)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        desc = QLabel()
        desc.setText("Contact me on discord to report it!\nStAx#6239")
        desc.setFont(descFont)
        desc.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(desc)
        layout.addStretch()

        self.dialogBox.setModal(True)
        self.dialogBox.show()

    def on_logOut(self):
        self.logOut.emit(
            True
        )

    def on_reset(self):
        self.reset.emit(
            True
        )
    
    def on_aboutTheApp(self):
        self.dialogBox = QDialog()
        self.dialogBox.setWindowIcon(QtGui.QIcon("mmulogo.ico"))
        self.dialogBox.setStyleSheet(dialog)
        #deal with the "?"
        self.dialogBox.setWhatsThis("Hi there!")
        self.dialogBox.setWindowTitle("Report Bugs")
        self.dialogBox.setFixedSize(500,300)
        layout = QVBoxLayout()
        self.dialogBox.setLayout(layout)

        layout.addStretch()
        titleFont = QtGui.QFont("Normal",12)
        titleFont.setBold(True)
        titleFont.setUnderline(True)
        descFont = QtGui.QFont("Normal",8)

        aimTitle = QLabel()
        aimTitle.setFont(titleFont)
        aimTitle.setAlignment(QtCore.Qt.AlignCenter)
        aimTitle.setText("Aim")
        aimTitle.adjustSize()
        layout.addWidget(aimTitle)
        
        aimDesc = QLabel()
        aimDesc.setMargin(10)
        aimDesc.setFont(descFont)
        aimDesc.setAlignment(QtCore.Qt.AlignLeft)
        aimDesc.setText("This application is mainly focused on\n-Notify MMU students whether if there's new announcements\n-Allow them to take the attendance without having\n to scan the QR Code.\n-Make their life easier essentially :)\n-Make MY LIFE EASIER")
        aimDesc.adjustSize()
        layout.addWidget(aimDesc)


        aboutMeTitle = QLabel()
        aboutMeTitle.setFont(titleFont)
        aboutMeTitle.setAlignment(QtCore.Qt.AlignCenter)
        aboutMeTitle.setText("About Me")
        aboutMeTitle.adjustSize()
        layout.addWidget(aboutMeTitle)

        aboutMeDesc = QLabel()
        aboutMeDesc.setMargin(10)
        aboutMeDesc.setFont(descFont)
        aboutMeDesc.setAlignment(QtCore.Qt.AlignLeft)
        aboutMeDesc.setText("I am essentially a MMU student, as y'all might already know\nUh, there's really nothing special about me!\nCheck out my GitHub:\nhttps://github.com/wyhong3103")
        aboutMeDesc.adjustSize()
        layout.addWidget(aboutMeDesc)
        layout.addStretch(2)
        self.dialogBox.setModal(True)
        self.dialogBox.show()
    

    def _initActionHandler(self):
        self.exitAction.triggered.connect(self.close)
        self.aboutTheApp.triggered.connect(self.on_aboutTheApp)
        self.logoutAction.triggered.connect(self.on_logOut)
        self.resetAction.triggered.connect(self.on_reset)
        self.reportAction.triggered.connect(self.on_report)
        #report opens up a window to my contact

    def _createActions(self):
        self.exitAction = QtWidgets.QAction("Exit",self)
        self.aboutTheApp = QtWidgets.QAction("About This Application",self)
        self.logoutAction = QtWidgets.QAction("Log Out",self)
        self.resetAction = QtWidgets.QAction("Reset Automater",self) 
        self.reportAction = QtWidgets.QAction("Report Bugs", self)
        self._initActionHandler()

    def _createMenuBar(self):
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setObjectName("menubar")
        self.applicationMenu = self.menuBar.addMenu("Application")
        self.applicationMenu.setObjectName("applicationMenu")
        self.applicationMenu.addAction(self.exitAction)
        self.applicationMenu.addAction(self.aboutTheApp)
        self.accountMenu =  self.menuBar.addMenu("Account")
        self.accountMenu.addAction(self.logoutAction)
        self.helpMenu =  self.menuBar.addMenu("Help")
        self.helpMenu.addAction(self.resetAction)
        self.helpMenu.addAction(self.reportAction)
        self.setMenuBar(self.menuBar)


    def _createAttendancButton(self):
        self.attendanceButton = QPushButton("Take Attendance")
        self.attendanceButton.setObjectName("attendanceButton")
        self.attendanceLayout.addWidget(self.attendanceButton,2)
        self.attendanceButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.attendanceButton.setMinimumHeight(70)
        self.attendanceButton.clicked.connect(self.on_openAttendanceWindow)

    def _createTitle(self):
        self.titleText = QLabel("MMLS Automater 3.0")
        self.titleText.setObjectName("titleText")
        self.titleText.setAlignment(QtCore.Qt.AlignRight)
        self.titleText.setContentsMargins(0,30,0,0)
        self.titleText.adjustSize()
        self.attendanceLayout.addWidget(self.titleText,5)

    def _createAnnouncementLayout(self):
        announcementMenuWidget = QWidget()
        self.annoucementMenuLayout = QVBoxLayout()
        announcementMenuWidget.setLayout(self.annoucementMenuLayout)

        announcementDisplayWidget = QWidget()
        
        self.announcementLayout.addWidget(announcementMenuWidget)
        self.announcementLayout.addWidget(announcementDisplayWidget)

    def _createAnnouncementMenuWidgets(self):
        self.annoucementMenuLayout.addStretch(2)
        newAnnouncementsLabel = QLabel("New Announcements")
        newAnnouncementsLabel.setObjectName("newAnnouncementLabel")
        labelFont = QtGui.QFont("Normal",9)
        newAnnouncementsLabel.setAlignment(QtCore.Qt.AlignCenter)
        labelFont.setWeight(5)
        newAnnouncementsLabel.setFont(labelFont)
        newAnnouncementsLabel.setMargin(0)
        self.annoucementMenuLayout.addWidget(newAnnouncementsLabel,0)

        self.numberOfNew = QTextEdit()
        self.numberOfNew.setReadOnly(True)
        self.annoucementMenuLayout.addWidget(self.numberOfNew,0)
        self.annoucementMenuLayout.setAlignment(self.numberOfNew,QtCore.Qt.AlignCenter)

        self.annoucementMenuLayout.addStretch(1)
        self.viewNewButton = QPushButton("View All\n New Announcements")
        self.viewNewButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.viewNewButton.setMinimumHeight(60)
        self.viewNewButton.clicked.connect(self.on_viewNewAnnouncement)
        self.annoucementMenuLayout.addWidget(self.viewNewButton)

        self.annoucementMenuLayout.addStretch(2)

        subjectLabel = QLabel("Subject")
        subjectLabel.setObjectName("subjectLabel")
        subjectLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.annoucementMenuLayout.addWidget(subjectLabel)
        self.subjectBox = QComboBox()
        self.subjectBox.addItem("-")
        self.subjectBox.setMaximumWidth(230)
        self.subjectBox.setMinimumHeight(45)
        self.subjectBox.currentTextChanged.connect(self.on_subjectChanged)
        self.annoucementMenuLayout.addWidget(self.subjectBox,5)
        
        dateLabel = QLabel("Date")
        dateLabel.setObjectName("dateLabel")
        dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.annoucementMenuLayout.addWidget(dateLabel)
        self.dateBox = QComboBox()
        self.dateBox.addItem("-")
        self.dateBox.setMaximumWidth(230)
        self.dateBox.setMinimumHeight(45)
        self.annoucementMenuLayout.addWidget(self.dateBox,5)

        self.viewAnnouncementButton = QPushButton("View\n Announcement")

        self.viewAnnouncementButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.viewAnnouncementButton.setMinimumWidth(170)
        self.viewAnnouncementButton.setMinimumHeight(60)
        self.viewAnnouncementButton.clicked.connect(self.on_viewAnnouncement)
        self.annoucementMenuLayout.addWidget(self.viewAnnouncementButton,5)
        self.annoucementMenuLayout.setAlignment(self.viewAnnouncementButton,QtCore.Qt.AlignCenter)

        self.annoucementMenuLayout.addStretch(4)


    def _createAnnouncementDisplayWidgets(self):
        self.displayOutput = QTextEdit()
        self.displayOutput.setFixedWidth(700)
        self.displayOutput.setReadOnly(True)
        self.announcementLayout.addWidget(self.displayOutput)
        sb = self.displayOutput.verticalScrollBar()
        sb.setValue(sb.maximum())
    

    def _initMainLayout(self):
        """
        Only those objects that will be used afterwards will be the property of the class
        """
        mainVlayoutwidget = QWidget()
        mainVlayoutwidget.setObjectName("mainWidget")
        mainVlayout = QVBoxLayout()
        mainVlayout.setObjectName("mainLayout")
        mainVlayoutwidget.setLayout(mainVlayout)
        self.setCentralWidget(mainVlayoutwidget)

        #Layout for attendance 
        attendanceWidget = QWidget()
        self.attendanceLayout = QHBoxLayout()
        attendanceWidget.setLayout(self.attendanceLayout)
        mainVlayout.addWidget(attendanceWidget,1)

        #Layout for announcement
        announcementGroup = QGroupBox("MMLS Announcements")
        self.announcementLayout = QHBoxLayout()
        announcementGroup.setLayout(self.announcementLayout)
        mainVlayout.addWidget(announcementGroup, 5)


    def _initMenu(self):
        self._createActions()
        self._createMenuBar()

    def _initAttendanceWidgets(self):
        self._createAttendancButton()
        self._createTitle()

    def _initAnnouncementWidgets(self):
        self._createAnnouncementLayout()
        self._createAnnouncementMenuWidgets()
        self._createAnnouncementDisplayWidgets()


class LoginWindow(QWidget):

    submitted = QtCore.pyqtSignal(str,str)

    def __init__(self):
        super(LoginWindow,self).__init__()
        self.setWindowIcon(QtGui.QIcon("mmulogo.ico"))
        self.setFixedSize(500, 250)
        self.setWindowTitle("MMLS Automater - 3.0 - Login")
        self._initui()
        self.setStyleSheet(loginWin)

    def _initui(self):
        self._initLayOut()
        self._initWidgets()
    
    def _initLayOut(self):
        self.loginLayout = QVBoxLayout()
        self.setLayout(self.loginLayout)
    
    def loginMessageBox(self, isLogin):
        messagebox = QMessageBox()
        if isLogin:
            messagebox.information(self,"Success","You are logged in.")
        else:
            messagebox.warning(self,"Failed","Invalid Credential")

    def submitIdPw(self):
        userid = self.userIdBox.text()
        userpw = self.passwordBox.text()
        self.submitted.emit(userid,userpw)
    
    def _initWidgets(self):
        
        self.loginLayout.addStretch()

        textLabel = QLabel("You're not login, please login to continue.")
        textLabel.setFont(QtGui.QFont('Normal', 10))
        self.loginLayout.addWidget(textLabel)

        self.loginLayout.addStretch()
        userIdWidget = QWidget()
        userIdLayout = QHBoxLayout()
        userIdWidget.setLayout(userIdLayout)
        userIdLabel = QLabel("User ID : ")
        userIdLabel.setFont(QtGui.QFont('Normal', 10))
        self.userIdBox = QLineEdit()
        self.userIdBox.setMinimumHeight(25)
        userIdLayout.addWidget(userIdLabel,1)
        userIdLayout.addWidget(self.userIdBox,2)
        
        passwordWidget = QWidget()
        passwordLayout = QHBoxLayout()
        passwordWidget.setLayout(passwordLayout)
        passwordLabel = QLabel("Password : ")
        passwordLabel.setFont(QtGui.QFont('Normal', 10))
        self.passwordBox = QLineEdit()
        self.passwordBox.setEchoMode(QLineEdit.Password)
        self.passwordBox.setMinimumHeight(25)
        passwordLayout.addWidget(passwordLabel,1)
        passwordLayout.addWidget(self.passwordBox,2)

        self.loginButton = QPushButton("Login", clicked=self.submitIdPw)
        self.loginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loginButton.setMinimumHeight(40)
        self.loginButton.setMinimumWidth(200)


        self.loginLayout.addWidget(userIdWidget)
        self.loginLayout.addWidget(passwordWidget)
        self.loginLayout.addWidget(self.loginButton)
        self.loginLayout.setAlignment(self.loginButton, QtCore.Qt.AlignRight)

class AttendanceWindow(QDialog):
    
    takeAttendance = QtCore.pyqtSignal(bool)
    
    def __init__(self):
        super(AttendanceWindow,self).__init__()
        self.setWindowIcon(QtGui.QIcon("mmulogo.ico"))
        self.setFixedSize(700,300)
        self.setWindowTitle("Take Attendance")
        self.setModal(True)
        self.setWhatsThis("TIME TO TAKE ATTENDANCE!")
        self._initUI()
        self.setStyleSheet(dialog)
    
    def on_takeAttendance(self):
        self.takeAttendance.emit(
            True
        )

    def clearWidgets(self):
        self.deleteItemsOfLayout()

    def insertLabel(self,text):
        label = QLabel(text)
        label.setFont(QtGui.QFont("Normal",10))
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(label)
        


    def deleteItemsOfLayout(self):
        layout = self.layout
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout()        
    

    def updateTimer(self):
        if self.timerCount >= 0:
            self.timerLabel.setText(str(self.timerCount))
            self.timerCount -= 1
        else:
            self.timerLabel.setText("Processing...")
            self.timer.stop()
            self.clearWidgets()
            self.on_takeAttendance()

    def _initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        attendanceLabel = QLabel("Please make sure the qr code is on the screen.")
        attendanceLabel.setFont(QtGui.QFont("Normal",11))
        attendanceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(attendanceLabel)

        self.layout.addStretch(1)

        self.timerCount = 5
        self.timerLabel = QLabel()
        self.timerLabel.setFont(QtGui.QFont("LCD",30))
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setText(str(self.timerCount))
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)
        
        self.layout.addWidget(self.timerLabel)

        self.layout.addStretch(2)
    
def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__" :
    main()