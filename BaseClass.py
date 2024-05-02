
import pytest
import inspect
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

@pytest.mark.usefixtures("setup")
class BaseClass:
    def getLogger(self):
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        fileHandler = logging.FileHandler('logfile.log')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(name)s :%(message)s")
        fileHandler.setFormatter(formatter)

        logger.addHandler(fileHandler)  # filehandler object

        logger.setLevel(logging.DEBUG)
        return logger

    def trySearchForImageElement(self, image):

        with open("./resources/images/" + image +".png", "rb") as image_file:
            image64 = base64.b64encode(image_file.read()).decode("utf-8")

        element = None
        try:
            element = self.driver.find_element(AppiumBy.IMAGE, image64)
        except Exception as e:
            print("Didn't find " + image +" image : \n")
            #print(e)

        return element

    
    def tryFindElement(self, type, element, click = False):
        self.driver.implicitly_wait(10)
        try:
            element = self.driver.find_element(type, element)
            if click:
                element.click()
        except Exception as e:
            print("Didn't find element " + element + ": \n")
            #print(e)
        self.driver.implicitly_wait(30)


    def waitForElementToAppear(self, element):
        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located(element))