from py_selenium_auto.browsers.browser_services import BrowserServices


class TestUI:
    def teardown_method(self, method):
        if BrowserServices.Instance.is_browser_started:
            BrowserServices.Instance.browser.quit()
