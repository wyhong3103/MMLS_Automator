from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QPushButton,
                             QHBoxLayout,
                             QVBoxLayout,
                             QLabel,
                             QGroupBox,
                             QComboBox,
                             QTextEdit,
                             QLineEdit)
import sys

"""
Insert Subjects/dates to combo box
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setGeometry(600,200,1000,600)
        self.setFixedSize(1000, 600)
        self.setWindowTitle("MMLS Automater - 3.0")
        self._initUI()
        #self.setStyleSheet(self.styleSheet)


    @property
    def styleSheet(self):
        #show border stylesheet
        stylesheet = "background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); "
        return stylesheet

    def _initUI(self):
        self._initMenu()
        self._initMainLayout()
        self._initAttendanceWidgets()
        self._initAnnouncementWidgets()


    def _createActions(self):
        self.loginAction = QtWidgets.QAction("Log In",self)
        self.logoutAction = QtWidgets.QAction("Log Out",self)
        self.resetAction = QtWidgets.QAction("Reset Automater",self) 
        self.reportAction = QtWidgets.QAction("Report Bugs", self)

    def _createMenuBar(self):
        self.menuBar = QtWidgets.QMenuBar(self)
        self.accountMenu =  self.menuBar.addMenu("Account")
        self.accountMenu.addAction(self.loginAction)
        self.accountMenu.addAction(self.logoutAction)
        self.helpMenu =  self.menuBar.addMenu("Help")
        self.helpMenu.addAction(self.resetAction)
        self.helpMenu.addAction(self.reportAction)
        self.setMenuBar(self.menuBar)


    def _createAttendancButton(self):
        self.attendanceButton = QPushButton("Take Attendance")
        self.attendanceLayout.addWidget(self.attendanceButton,2)
        self.attendanceButton.setMinimumHeight(50)

    def _createTitle(self):
        self.titleText = QLabel("MMLS Automater 3.0")
        self.titleText.setFont(QtGui.QFont('Times New Roman',15))
        self.titleText.setAlignment(QtCore.Qt.AlignRight)
        self.titleText.setContentsMargins(0,15,0,0)
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
        newAnnouncementsLabel = QLabel("Number of new announcements")
        newAnnouncementsLabel.setMargin(0)
        self.annoucementMenuLayout.addWidget(newAnnouncementsLabel,0)
        self.numberOfNew = QLabel("1")
        self.numberOfNew.setAlignment(QtCore.Qt.AlignCenter)
        self.annoucementMenuLayout.addWidget(self.numberOfNew,0)

        self.annoucementMenuLayout.addStretch(2)

        subjectLabel = QLabel("Subject")
        subjectLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.annoucementMenuLayout.addWidget(subjectLabel)
        self.subjectBox = QComboBox()
        self.subjectBox.setMaximumWidth(200)
        self.subjectBox.setMinimumHeight(30)
        self.annoucementMenuLayout.addWidget(self.subjectBox,5)

        
        dateLabel = QLabel("Date")
        dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.annoucementMenuLayout.addWidget(dateLabel)
        self.dateBox = QComboBox()
        self.dateBox.setMaximumWidth(200)
        self.dateBox.setMinimumHeight(30)
        self.annoucementMenuLayout.addWidget(self.dateBox,5)

        self.viewAnnouncementButton = QPushButton("View Announcement")
        self.viewAnnouncementButton.setMaximumWidth(150)
        self.viewAnnouncementButton.setMinimumHeight(30)
        self.annoucementMenuLayout.addWidget(self.viewAnnouncementButton,5)
        self.annoucementMenuLayout.setAlignment(self.viewAnnouncementButton,QtCore.Qt.AlignCenter)

        self.annoucementMenuLayout.addStretch(4)


    def _createAnnouncementDisplayWidgets(self):
        self.displayOutput = QTextEdit()
        self.displayOutput.setReadOnly(True)
        self.announcementLayout.addWidget(self.displayOutput)
        sb = self.displayOutput.verticalScrollBar()
        sb.setValue(sb.maximum())
    
    def _insertToDisplay(self,text):
        self.displayOutput.insertPlainText(text)


    def _initMainLayout(self):
        """
        Only those objects that will be used afterwards will be the property of the class
        """
        mainVlayoutwidget = QWidget()
        mainVlayout = QVBoxLayout()
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
    def __init__(self):
        super(LoginWindow,self).__init__()
        self.setGeometry(750,300,500,250)
        self.setFixedSize(500, 250)
        self.setWindowTitle("MMLS Automater - 3.0 - Login")
        self._initui()

    def _initui(self):
        self._initLayOut()
        self._initWidgets()
    
    def _initLayOut(self):
        self.loginLayout = QVBoxLayout()
        self.setLayout(self.loginLayout)
    
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

        self.loginButton = QPushButton("Login")
        self.loginButton.setMinimumHeight(40)
        self.loginButton.setMaximumWidth(200)


        self.loginLayout.addWidget(userIdWidget)
        self.loginLayout.addWidget(passwordWidget)
        self.loginLayout.addWidget(self.loginButton)
        self.loginLayout.setAlignment(self.loginButton, QtCore.Qt.AlignRight)



def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__" :
    main()