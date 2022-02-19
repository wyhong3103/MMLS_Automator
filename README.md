# MMLS Automator (3.0 With GUI!)

I've decided not to update it on the original repository. Because ,it's basically a remake at this point.
<br><br>
If you don't know already,
<br><br>
This python application let you automate stuff like taking attendance during your lecture without having your phone, or using the link, check your MMLS for any new announcements.
<br><br>
Inspiration : MMLS2 has no notification from lecturers, QR code is unscannable using MMLS mobile application, that's what inspired me to build this.

## What's New In This Version?
- There's GUI now! And it's built with PyQt5

- It's implemented in MVC architecture , probably.


## Instructions

1. Install a chromium-based browser (Google Chrome, Brave, Chromium, etc.). You can skip this step if you already have one downloaded. Although other browsers such as Firefox, also works with selenium, but this application is developed based on chrome, I am not entirely sure if there will be bugs with Firefox.

2. pip install the external modules using (Make sure your python is added to path)

    `$ pip install -r "requirements.txt"`

    (requirements.txt of this directory)

    OR run the following commands in sequence

    `$ pip install opencv-python`

    `$ pip install selenium`

    `$ pip install pyautogui`

    `$ pip install pyzbar`

    `$ pip install pillow`

    `$ pip install pyqt5`

3. Download [chromedriver.exe](https://chromedriver.chromium.org/downloads), make sure you downloaded the right version for your browser, and also include the path to it in selenium_header.py (check out the file , and you will see where should you put it on), also the path of your chrome.exe.

4. Run `$ py app.py` to start this application.

## Functionalities

- View announcements from MMLS, it also tells you whether there is new announcements

- Take attendance without using your phone (by scanning the QR Code with python script)

And that's essentially what it does.

## Modules Included

-PyQt5

- OpenCV 

- Selenium

- Logging

- Datetime

- PyAutoGui

- OS 

- Json

- Time

- Pyzbar

- Regular Expression

- Pillow

## Side Note

Username and password stored are not encrypted and all, so please, be aware of it, and use it on your own risk.

## Thoughts

It was a pretty fun project to do, it's been sometimes since the last time I dealt with selenium and other modules. Not sure how can we implement asyncIO in this application, but I am pretty sure this application can still be optimize and all.

## Bugs

- There might be bugs when you're not connected to the Internet, or MMLS site is down

## QnA

- *empty for now*

## License & copyright

Licensed under [MIT License](LICENSE)


### HAVE FUN USING IT
