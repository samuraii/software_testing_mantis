from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.soap import SoapHelper


class Application:

    def __init__(self, browser, configuration):
        if browser == 'chrome':
            self.wd = webdriver.Chrome()
        elif browser == 'firefox':
            self.wd = webdriver.Firefox()
        elif browser == 'safari':
            self.wd = webdriver.Safari()
        elif browser == 'ie':
            self.wd = webdriver.Ie()
        else:
            raise ValueError('I don\'t know this browser - {}'.format(browser))
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.homepage = configuration['web']['url']
        # self.james = JamesHelper(self)
        self.config = configuration
        # self.signup = SignupHelper(self)
        self.soap = SoapHelper(self)

    def is_valid(self):
        try:
            url = self.wd.current_url
            return True
        except:
            return False

    def accept_alert(self):
        try:
            self.wd.switch_to_alert().accept()
        except NoAlertPresentException:
            pass

    def open_homepage(self):
        self.wd.get(self.homepage)

    def complete(self):
        self.wd.quit()
