from tests.integration.forms_test_app.the_internet.forms.checkboxes_form import CheckBoxesForm
from tests.integration.test_ui import TestUI


class TestCheckBox(TestUI):
    check_box_form = CheckBoxesForm()

    def setup_method(self):
        self.check_box_form.open()

    def test_toggle(self):
        checkbox_state = self.check_box_form.first_check_box.is_checked()
        self.check_box_form.first_check_box.toggle()
        assert checkbox_state is not self.check_box_form.first_check_box.is_checked()
        self.check_box_form.first_check_box.toggle()
        assert checkbox_state is self.check_box_form.first_check_box.is_checked()

    def test_uncheck(self):
        self.check_box_form.second_check_box.uncheck()
        assert not self.check_box_form.second_check_box.is_checked()
        self.check_box_form.second_check_box.check()
        assert self.check_box_form.second_check_box.is_checked()

    def test_check(self):
        self.check_box_form.first_check_box.check()
        assert self.check_box_form.first_check_box.is_checked()
        self.check_box_form.first_check_box.uncheck()
        assert not self.check_box_form.first_check_box.is_checked()

    def test_get_state_via_js(self):
        self.check_box_form.first_check_box.check()
        self.check_box_form.second_check_box.uncheck()
        assert self.check_box_form.first_check_box.js_actions.is_checked()
        assert not self.check_box_form.second_check_box.js_actions.is_checked()
