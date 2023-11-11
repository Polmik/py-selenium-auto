import pytest
from selenium.common import NoAlertPresentException, UnexpectedAlertPresentException

from py_selenium_auto.browsers.browser_services import BrowserServices
from py_selenium_auto.browsers.enums.alert_actions import AlertAction
from tests.integration.forms_test_app.the_internet.forms.java_script_alerts_form import JavaScriptAlertsForm
from tests.integration.test_ui import TestUI


class TestAlert(TestUI):
    alerts_form = JavaScriptAlertsForm()

    def setup_method(self):
        self.alerts_form.open()

    def test_accept_alert(self):
        self.alerts_form.js_alert_button.click()
        BrowserServices.Instance.browser.handle_alert(AlertAction.Accept)
        assert "You successfully clicked an alert" == self.alerts_form.result_label.text

    def test_accept_confirmation_alert(self):
        self.alerts_form.js_confirm_button.click()
        BrowserServices.Instance.browser.handle_alert(AlertAction.Accept)
        assert "You clicked: Ok" == self.alerts_form.result_label.text

    def test_accept_confirmation_alert_in_wait_for(self):
        def _predicate(driver):
            try:
                BrowserServices.Instance.logger.debug(f"Current url: {driver.current_url}")
                return False
            except UnexpectedAlertPresentException as e:
                BrowserServices.Instance.logger.debug(f"Alert appeared: {str(e.msg)}")

                # TODO: Workaround, because the alert closes after receiving the url
                self.alerts_form.js_confirm_button.click()
                BrowserServices.Instance.browser.handle_alert(AlertAction.Accept)
                return True

        self.alerts_form.js_confirm_button.click()
        BrowserServices.Instance.conditional_wait.wait_for_driver(_predicate)
        assert "You clicked: Ok" == self.alerts_form.result_label.text

    def test_decline_confirmation_alert(self):
        self.alerts_form.js_confirm_button.click()
        BrowserServices.Instance.browser.handle_alert(AlertAction.Decline)
        assert "You clicked: Cancel" == self.alerts_form.result_label.text

    def test_accept_prompt_alert_with_text(self):
        text = "accept alert text"

        self.alerts_form.js_prompt_button.click()
        BrowserServices.Instance.browser.handle_alert(AlertAction.Accept, text)
        assert f"You entered: {text}" == self.alerts_form.result_label.text

    def test_decline_prompt_alert_with_text(self):
        self.alerts_form.js_prompt_button.click()
        BrowserServices.Instance.browser.handle_alert(AlertAction.Decline, "decline alert text")
        assert "You entered: null" == self.alerts_form.result_label.text

    @pytest.mark.parametrize(
        "action",
        [
            AlertAction.Accept,
            AlertAction.Decline,
        ],
    )
    def test_throw_no_alert_present_if_no_alert_present(self, action):
        try:
            BrowserServices.Instance.browser.handle_alert(action)
        except NoAlertPresentException:
            return
        assert False, "Expected an error: NoAlertPresentException"

    @pytest.mark.parametrize(
        "action",
        [
            AlertAction.Accept,
            AlertAction.Decline,
        ],
    )
    def test_throw_no_alert_present_if_no_prompt_alert_present(self, action):
        try:
            BrowserServices.Instance.browser.handle_alert(action, "Hello")
        except NoAlertPresentException:
            return
        assert False, "Expected an error: NoAlertPresentException"
