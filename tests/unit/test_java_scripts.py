import pytest

from py_selenium_auto.browsers.java_script import JavaScript
from collections import defaultdict


class TestJavaScripts:

    @pytest.mark.parametrize(
        "js_script",
        [js for js in JavaScript]
    )
    def test_should_get_java_script(self, js_script):
        assert len(js_script.script_from_file) > 0, f"Failed to get javascript {js_script}"

    def test_should_be_unique_java_scripts(self):
        values = [js.value for js in JavaScript]
        js_scripts = [js for js in JavaScript]
        counter = defaultdict(list)

        for value, js_script in zip(values, js_scripts):
            if values.count(value) > 1:
                counter[value].append(js_script)

        assert len(counter.keys()) == 0, \
            f"some duplicates where found among JavaScripts:\n{counter}"
