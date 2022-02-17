import json
from Locators.general_locators import GeneralLocators
from Locators.page_locators import PageLocators
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from parser.announcement_parser import Parser
import logging


class AnnouncementPage:
    def __init__(self,page,userid, userpw):
        self.userid = userid
        self.userpw = userpw
        self.page = page
        self.page.get("https://mmls2.mmu.edu.my/")

    def isElementPresent(self,locator):
        """
        This function check if a certain element exists.
        """
        try:
            logging.info(f"Checking if \"{locator}\" present.")
            self.page.find_element_by_css_selector(locator)
            return True
        except:
            return False

    def login(self):
        """
        This function login to MMLS.
        """
        username_login = self.page.find_element(By.CSS_SELECTOR,GeneralLocators.LOGIN_ID)
        userpw_login = self.page.find_element(By.CSS_SELECTOR,GeneralLocators.LOGIN_PASSWORD)
    
        username_login.send_keys(self.userid)
        userpw_login.send_keys(self.userpw)
        userpw_login.send_keys(Keys.ENTER)
        logging.info("Selenium is attempting to login using user information provided.")

        try:
            WebDriverWait(self.page,3).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR,GeneralLocators.SUBJECT_CARD)
                )
            )
        except:
            if self.isElementPresent(GeneralLocators.INVALID_LOGIN):
                logging.info("Login unsucessful! Reinitializing username and password, reask from user.")
                return False
        return True
            
    @property
    def getSubjectTags(self):
        """
        This function return all the html tags of the subject cards.
        """
        logging.info("Getting all the subject cards as an element tag.")
        subject_cards = GeneralLocators.SUBJECT_CARD
        card_list = self.page.find_elements(By.CSS_SELECTOR,subject_cards)
        return card_list
    
    def subjects_checker(self):
        """
        This function checks for new announcements, and provide the menu for navigation.
        """
        for i in range(len(self.getSubjectTags)):
            #rerendering 
            element = self.getSubjectTags[i]
            #i.text somehow return the name of the subject without having you find it again with css selector
            subjectName = element.text
            logging.info(f"{subjectName} is being checked for new announcements.")
            element.click()

            Parser(self.page).updateAnnouncements(subjectName, self.userid)

            #back to home page, to select the next subject card
            home_button = self.page.find_element(By.CSS_SELECTOR,PageLocators.HOME_BUTTON)
            home_button.click()

                    


