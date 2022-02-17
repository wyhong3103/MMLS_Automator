from datetime import datetime
import os
import logging
from PyQt5.QtWidgets import QApplication
from controller import *
import sys


#Intialize log file
directory_list = os.listdir()
if "logs" not in directory_list:
    logging.info("Creating logs directory")
    os.mkdir("logs")
if "json" not in directory_list:
    logging.info("Creating json directory")
    os.mkdir("json")

date = datetime.today().strftime("%d-%m-%y--%I-%M")
logging.basicConfig(
    format = "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    level = logging.INFO, 
    filename = f"logs\\logs-{date}.txt")

def main():
    logging.info("Starting main menu.")
    app = QApplication(sys.argv)
    controller = Controller()
    controller.start()

    logging.info("Ending this application.")
    sys.exit(app.exec_())

if __name__  == "__main__":
    main()
