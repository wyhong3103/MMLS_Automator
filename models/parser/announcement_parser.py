from typing import Dict
from Locators.page_locators import PageLocators,CardLocators
from selenium.webdriver.common.by import By
import json
import re
import logging
from datetime import datetime

class Parser:
    def __init__(self,parent):
        self.parent = parent

    def updateJSON(self,subject_dict : str,subjectName : str) -> Dict:
        """
        This function helps to grab the new announcements and return it to the caller function.
        """
        logging.info("Subjects' JSON File is being updated")
        if subjectName not in subject_dict:
            logging.info(f"{subjectName} is not found in the JSON, it's being initialized.")
            subject_dict[subjectName] = {
                                         "dateOfNew": [],
                                        "announcements" : dict()
                                        }

        announcementCards = self.parent.find_elements(By.CSS_SELECTOR,PageLocators.CARD_ANNOUNCEMENT)[1:]
        announcements =  subject_dict[subjectName]["announcements"]
        dateOfNew = []
        dateKeys = announcements.keys()

        logging.info("New announcements are being updated to the JSON object.")
        #If dateKeys is empty that means we're going to grab all available announcements
        if dateKeys:
            lastDate = dateKeys[-1]
            for i in announcementCards:
                title = i.find_element(By.CSS_SELECTOR,CardLocators.TITLE).text
                author = i.find_element(By.CSS_SELECTOR,CardLocators.AUTHOR).text
                date = re.search("Published at : (.+)\n")[1]
                
                #This code of block below here make sure we stop grabbing the announcements 
                #if the announcements were before the date of our last announcement
                dateObj = datetime.strp(date,"%d %b %Y")
                lastDateObj = datetime.strp(lastDate, "%d %b %Y")
                if (int(dateObj - lastDateObj) < 0) : break
                
                task = i.find_element(By.CSS_SELECTOR,CardLocators.TASK).text
                
                if date in announcements.keys():
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
                date = re.search("Published at : (.+)\n")[1]
                task = i.find_element(By.CSS_SELECTOR,CardLocators.TASK).text
                announcementStr = f"Title:\n{title}\n\n{author}\n\nAnnouncement:\n{task}"
                announcements[date].append(announcementStr)
                if date not in dateOfNew:
                    dateOfNew.append(date)

        subject_dict[subjectName] = {
            "dateOfNew" : dateOfNew,
            "announcements" : announcements
        }

        return subject_dict


    def updateAnnouncements(self,subjectName : str, userid : str) -> Dict:
        """
        This function loads the old announcements from the JSON, and update it.
        """
        with open(f"json\\{userid}_subject_info","r") as json_file:
            logging.info(f"subject_info json for {userid} is being read.")
            subject = json.load(json_file)

        newSubDict = self.updateJSON(subject,subjectName)
        
        with open("json\\{userid}_subject_info","w") as json_file:
            logging.info(f"subject_info json for {userid} is being written.")
            json.dump(newSubDict,json_file)
        
        return newSubDict

            