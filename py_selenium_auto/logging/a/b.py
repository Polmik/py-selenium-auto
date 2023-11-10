import re

v = """AddRemoveElementsForm.cs
AuthenticationForm.cs
BasicAuthForm.cs
CheckboxesForm.cs
ContextMenuForm.cs
DropdownForm.cs
DynamicContentForm.cs
DynamicControlsForm.cs
FileDownloaderForm.cs
ForgotPasswordForm.cs
HoversForm.cs
InfiniteScrollForm.cs
JQueryMenuForm.cs
JavaScriptAlertsForm.cs
KeyPressesForm.cs
RedirectorForm.cs
StatusCodesForm.cs
TheInternetForm.cs
WelcomeForm.cs"""

c = '''from enum import Enum

from py_selenium_auto_core.locator.locator import Locator
from selenium.webdriver.common.by import By

from py_selenium_auto.elements.label import Label
from py_selenium_auto.elements.link import Link
from tests.integration.forms_test_app.the_internet.forms.the_internet_from import TheInternetForm


class {0}(TheInternetForm):

    def __init__(self):
        super().__init__(
            Locator(By.XPATH, ""),
            "{1}",
        )

    @property
    def _url_part(self) -> str:
        return ""
'''


def to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


vs = [i.replace(".cs", "") for i in v.split()]
converted_vs = [to_snake(i) for i in vs]
print(converted_vs)

for i, j in zip(vs, converted_vs):
    cc = c.format(i, i.replace("Form", ""))
    with open(f"forms/{j}.py", "w") as f:
        f.write(cc)
