import cv2
import pyautogui
from pyzbar import pyzbar
import time
import os
import json
from selenium.common.exceptions import TimeoutException
from models.Locators.attendance_locators import AttendanceLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import logging
import re


class noQrCodeFound(ValueError):
    pass

class invalidCredential(ValueError):
    pass

class AttendancePage:
    def __init__(self,parent,userid, userpw):
        self.userid = userid
        self.userpw = userpw
        self.parent = parent
        self.qrcodes = None
    

    def qrcode_read(self):
        """
        This function convert the QR Code on your screen to URL, and return it.
        """
        try:
            logging.info("Preparing to scan QR Code.")
            screenshot = pyautogui.screenshot()
            logging.info("QRCode.jpg is being saved, and waiting to be scan.")
            screenshot.save("qrcode.jpg")
            img = cv2.imread("qrcode.jpg")
            logging.info("QRCode is scanned and decoded into strings.")
            qrcode = pyzbar.decode(img)
            #detect and decode returns a few argument, the first is what you want, the string
            qrcodes = []
            for qr in qrcode:
                qrcodes.append(qr.data.decode("utf-8"))
            os.remove("qrcode.jpg")
            logging.info("QRCode.jpg is removed and deleted from the machine.")
            if not qrcodes:
                raise noQrCodeFound
            self.qrcodes = qrcodes
        except noQrCodeFound:
            logging.info("QR code is not detected!")
            self.qrcodes = []

    def attendanceLogin(self):
        usernameInput = self.parent.find_element(By.CSS_SELECTOR,AttendanceLocators.USERNAME)
        pwInput = self.parent.find_element(By.CSS_SELECTOR,AttendanceLocators.PASSWORD)
        
        usernameInput.send_keys(self.userid)
        pwInput.send_keys(self.userpw)
        pwInput.send_keys(Keys.ENTER)
        logging.info("Selenium is attempting to login with the user information provided from JSON.")

        try:
            WebDriverWait(self.parent,3).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR,AttendanceLocators.HOME_BUTTON)
                )
            )
        except TimeoutException:
            logging.info("TimeoutException is raised, it's either of the slow connection or login unsucessful.")
            if self.parent.current_url != "https://mmls2.mmu.edu.my/attendance/success/home":
                logging.info("Login Unsucessful, invalid credential.")
                with open("json\\userinfo.json","w") as json_file:
                        userinfo = {"username":"","password":""}
                        json.dump(userinfo,json_file)
                logging.info("Reinitialized the user information in JSON file. Will be asking for it again.")
                return False
        return True

    def returnStatus(self) -> str:
        """
        This function grab the message from MMLS after taking attendance.
        """
        logging.info("Login successfully and taking attendance...")
        message = self.parent.find_element(By.CSS_SELECTOR,AttendanceLocators.MESSAGE).text
        return f"\n{message}\n"

    def takeAttendance(self) -> str:
        """
        This function take the attendance.
        """
        if self.qrcodes:
            logging.info("Iterating through the QR Codes...")
            for i,url in enumerate(self.qrcodes):
                pattern = "https://mmls2.mmu.edu.my/attendance.+"
                logging.info("Using regular expression to validate the link provided.")
                if re.search(pattern,url):
                    if self.parent.current_url == "https://mmls2.mmu.edu.my/attendance/success/home":
                        home_button = self.parent.find_element(By.CSS_SELECTOR,AttendanceLocators.HOME_BUTTON)
                        home_button.click()
                    self.parent.get(url)
                    logging.info(f"Accessing : {url}")
                    if self.attendanceLogin():
                        logging.info("Accessing to the attendance site.")
                        yield f"QR Code {i+1}: {self.returnStatus()}"
                    else:
                        raise invalidCredential
                else:
                    logging.info("QR Code contains non-mmls link.")
                    yield f"QR Code {i+1}: This QR Code contains non-mmls link." 
        else:
            yield "No QR Code is found on the screen."
        






    
        


