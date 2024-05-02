import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService


driver = None
service = None

def pytest_addoption(parser):
    parser.addoption(
        "--platform", action="store", default="android"
    )

@pytest.fixture()
def setup(request):
    global driver
    global service
    platformType = request.config.getoption("platform")
    url = 'http://127.0.0.1:4723'
    service = AppiumService()
    # service.start(args=['--address', '127.0.0.1', '-p', '4723', '--use-plugins', 'images'])
    service.start(args=['--use-plugins', 'images'])


    capabilities = None
    if platformType == "android":
        capabilities = dict(
            platformName='Android',
            automationName='uiautomator2',
            deviceName='samsung SM-S901E',
            appPackage='com.nexon.bluearchiveteen',
            appActivity='.MxUnityPlayerActivity',
            noReset='true',
            newCommandTimeout = '150'
        )

    # adb shell "dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'"

    # com.nexon.bluearchiveone/com.nexon.bluearchiveone.MxUnityPlayerActivity
    # adb shell dumpsys package | grep -i ' + com.nexon.bluearchiveone + ' | grep Activity

    driver = webdriver.Remote(url, options=UiAutomator2Options().load_capabilities(capabilities))
    driver.implicitly_wait(30)
    driver.update_settings({"getMatchedImageResult": True})
    #driver.update_settings({"fixImageTemplateScale": True})
    driver.update_settings({"autoUpdateImageElementPosition": True})
    driver.update_settings({"imageMatchThreshold": 0.7})

    driver.activate_app("com.nexon.bluearchiveteen")
    request.cls.driver = driver


    # window = pyautogui.getWindowsWithTitle('BlueStacks')[0]
    # window.activate()
    # window.maximize()
    

    print("Test setup complete\n")
    yield
    print("Test tearing down\n")

    driver.terminate_app("com.nexon.bluearchiveteen")
    driver.quit()
    service.stop()
    


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
        driver.get_screenshot_as_file(name)

