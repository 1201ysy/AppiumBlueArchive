import time
import pyautogui
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy

from BaseClass import BaseClass

class TestBlueStack(BaseClass):


    def test_appiumImage(self):

        log = self.getLogger()

        time.sleep(10) # Wait for game to load

        wifiDownloadElement = self.trySearchForImageElement("wifiDownload")

        if wifiDownloadElement is not None:
            self.trySearchForImageElement("confirm").click()
            log.info("Wifi Download needed")
            time.sleep(50)

        
        time.sleep(10)


        dontShowElement = self.trySearchForImageElement("dontshowtoday")
    
        while dontShowElement is not None:
            log.info("Ad pop up; Don't show today")
            dontShowElement.click()
            time.sleep(3)
            self.driver.implicitly_wait(10) # Wait reduced to 10s
            dontShowElement = self.trySearchForImageElement("dontshowtoday")
            self.driver.implicitly_wait(30) # Wait back to normal

        menuElement = self.trySearchForImageElement("menu")
        #element.click()

        assert (menuElement is not None) # Check Game is in start page

       
        self.driver.find_element(By.ID, "com.nexon.bluearchiveteen:id/unitySurfaceView").click()


        time.sleep(3)


        self.driver.find_element(By.XPATH, "//android.widget.Button[@text='게스트로 로그인']").click()

        self.driver.find_element(By.ID, "com.nexon.bluearchiveteen:id/alert_btn_positive").click()

        checkBoxes = self.driver.find_elements(By.ID, "com.nexon.bluearchiveteen:id/npterms_item_checkbox")
        for i in range(3):
            checkBoxes[i].click()


        self.driver.find_element(By.ID, "com.nexon.bluearchiveteen:id/npterms_agree_and_start").click()


        self.tryFindElement(By.ID, "com.nexon.bluearchiveteen:id/permissionAgreeButton", click= True)
        self.tryFindElement(By.ID, "com.android.packageinstaller:id/permission_allow_button", click= True)

        accountCreatedElement = self.trySearchForImageElement("accountCreated")

        assert (accountCreatedElement is not None)
        log.info("Account Successfully created!")
        self.trySearchForImageElement("confirm").click()

        time.sleep(10)





    def pyautogui(self):

        menuImage = "./resources/images/menu.png"

        isSafe = False
        btn = None
        time.sleep(20)

        while(btn == None):

            try:
                btn = pyautogui.locateCenterOnScreen(menuImage, grayscale=False, confidence=0.7)
                if btn is not None:
                    pyautogui.click(btn)
                    isSafe = True   
                    print("Image Found")
            except Exception as e:
                #acc -= 0.05
                isSafe = False
                print(e)

            if isSafe:
                break

        time.sleep(10)