from typing import Dict
from models.Locators.page_locators import PageLocators,CardLocators
from selenium.webdriver.common.by import By
import json
import re
import logging
import os
from datetime import datetime

class Parser:
    def __init__(self,parent):
        self.parent = parent


    def updateJSON(self,subject_dict,subjectName : str) -> Dict:
        """
        This function helps to grab the new announcements and return it to the caller function.
        """
        logging.info(f"{subjectName} JSON File is being updated")
        if subjectName not in subject_dict:
            logging.info(f"{subjectName} is not found in the JSON, it's being initialized.")
            subject_dict[subjectName] = {
                                         "dateOfNew": [],
                                        "announcements" : dict()
                                        }

        announcementCards = self.parent.find_elements(By.CSS_SELECTOR,PageLocators.CARD_ANNOUNCEMENT)[1:]
        announcements =  subject_dict[subjectName]["announcements"]
        dateOfNew = []
        dateKeys = list(announcements.keys())

        logging.info("New announcements are being updated to the JSON object.")
        #If dateKeys is empty that means we're going to grab all available announcements
        if dateKeys:
            lastDate = dateKeys[0]
            for i in announcementCards:
                title = i.find_element(By.CSS_SELECTOR,CardLocators.TITLE).text
                author = i.find_element(By.CSS_SELECTOR,CardLocators.AUTHOR).text
                date = re.search("Published at : (.+)",author)[1]
                
                #This code of block below here make sure we stop grabbing the announcements 
                #if the announcements were before the date of our last announcement
                dateObj = datetime.strptime(date,"%d %b %Y").timestamp()
                lastDateObj = datetime.strptime(lastDate, "%d %b %Y").timestamp()
                if (int(dateObj - lastDateObj) < 0):
                    break
                
                task = i.find_element(By.CSS_SELECTOR,CardLocators.TASK).text
                
                if date not in announcements.keys():
                    announcements[date] = []
                announcementStr = f"Title:\n{title}\n\n{author}\n\nAnnouncement:\n{task}"

                #Code below basically check if the date we're currently checking 
                #is the date of the date of our last existing announcement
                #Because there might be pontential update on that day
                if date == lastDate:
                    if announcementStr in announcements[lastDate]:
                        continue
                announcements[date].append(announcementStr)

                if date not in dateOfNew:
                    dateOfNew.append(date)
        else:
            for i in announcementCards:
                title = i.find_element(By.CSS_SELECTOR,CardLocators.TITLE).text
                author = i.find_element(By.CSS_SELECTOR,CardLocators.AUTHOR).text
                date = re.search("Published at : (.+)",str(author))[1]
                task = i.find_element(By.CSS_SELECTOR,CardLocators.TASK).text
                announcementStr = f"Title:\n{title}\n\n{author}\n\nAnnouncement:\n{task}"

                if date not in announcements.keys():
                    announcements[date] = []

                announcements[date].append(announcementStr)

                if date not in dateOfNew:
                    dateOfNew.append(date)

        subject_dict[subjectName] = {
            "dateOfNew" : dateOfNew,
            "announcements" : announcements
        }

        return subject_dict

    def initJSON(self, userid):

        directory_list = os.listdir("json")
        if f"{userid}_subject_info.json" not in directory_list:
            logging.info(f"Creating subject json file for {userid} directory")
            with open(f"json\\{userid}_subject_info.json", "w") as js:
                js.write("{}")


    def updateAnnouncements(self,subjectName : str, userid : str) -> Dict:
        """
        This function loads the old announcements from the JSON, and update it.
        """
        self.initJSON(userid)

        with open(f"json\\{userid}_subject_info.json","r") as json_file:
            logging.info(f"subject_info json for {userid} is being read.")
            subject = json.load(json_file)

        newSubDict = self.updateJSON(subject,subjectName)
        
        with open(f"json\\{userid}_subject_info.json","w") as json_file:
            logging.info(f"subject_info json for {userid} is being written.")
            json.dump(newSubDict,json_file,indent=4)
        
        return newSubDict

            