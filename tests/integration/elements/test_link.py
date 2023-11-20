from py_selenium_auto.browsers.browser_services import BrowserServices
from tests.integration.forms_test_app.the_internet.forms.redirector_form import RedirectorForm
from tests.integration.forms_test_app.the_internet.forms.status_codes_form import StatusCodesForm
from tests.integration.test_ui import TestUI


def _wait_for_redirect():
    BrowserServices.Instance.conditional_wait.wait_for_condition(
        lambda: BrowserServices.Instance.browser.current_url == StatusCodesForm().url,
    )


class TestLink(TestUI):
    redirector_form = RedirectorForm()

    def setup_method(self):
        self.redirector_form.open()

    def test_click(self):
        self.redirector_form.redirect_link.click()
        _wait_for_redirect()
        assert StatusCodesForm().url.lower() == BrowserServices.Instance.browser.current_url.lower()

    def test_get_href(self):
        BrowserServices.Instance.browser.go_to(self.redirector_form.redirect_link.href)
        _wait_for_redirect()
        assert StatusCodesForm().url.lower() == BrowserServices.Instance.browser.current_url.lower()
