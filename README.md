# Selenium for Python

[![Latest Version](https://img.shields.io/pypi/v/py_selenium_auto.svg)](https://pypi.org/project/py-selenium-auto/)
[![License](https://img.shields.io/pypi/l/py_selenium_auto.svg)](https://pypi.org/project/py-selenium-auto/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/py_selenium_auto.svg)](https://pypi.org/project/py-selenium-auto/)
[![Build Status](https://github.com/Polmik/py-selenium-auto/actions/workflows/tests.yml/badge.svg)](https://github.com/Polmik/py-selenium-auto/actions/workflows/tests.yml)
[![Coverage Status](https://codecov.io/gh/Polmik/py-selenium-auto/branch/main/graph/badge.svg)](https://codecov.io/gh/Polmik/py-selenium-auto)
[![Supported Python implementations](https://img.shields.io/pypi/implementation/py_selenium_auto.svg)](https://pypi.org/project/py-selenium-auto/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Introduction

This package is a library designed to simplify your work with Selenium WebDriver and based on [py-selenium-auto-core](https://github.com/Polmik/py-selenium-auto-core) solution.

### Supported browsers
* Chrome

**Note: Support for popular browsers will be expanded in the future**

### Supported Python Versions

* Python 3.7-3.12

### Installation 

If you have [pip](https://pip.pypa.io/en/stable/) on your system, you can simply install or upgrade the Python bindings:

```bash
pip install -U py-selenium-auto
```

Alternately, you can download the source distribution from [PyPI](https://pypi.org/project/py-selenium-auto/#files), unarchive it, and run:

```bash
python setup.py install
```

### Template

To start the project using this solution, you can look into [py-selenium-auto-template
](https://github.com/Polmik/py-selenium-auto-template).

### Quick start

1. Add the dependency in your project
2. Create conftest.py file and add the following code:
```python
@pytest.fixture(scope="session", autouse=True)
def setup_session(request):
    # TODO: workaround to set calling root path, because pytest runs from the root dir
    work_dir = RootPathHelper.current_root_path(__file__)
    os.chdir(work_dir)
```

It's necessary to set root dir for your test directory. It is assumed that your project structure will look like this:
```
src/
    __init__.py
    some_code/
tests/  # Any name
    __init__.py
    resources/
    some_code/
```
3. Create instance of Browser in your test:
```python
browser = BrowserServices.Instance.browser
```
4. Use Browser's methods directly for general actions, such as navigation, window resize, scrolling and alerts handling:
```python
browser.maximize()
browser.go_to("https://google.com")
browser.wait_for_page_to_load()
```
5. Use ElementFactory class's methods to get an instance of each element:
```python
my_text_box = BrowserServices.Instance.service_provider.element_factory().get_text_box(Locator.by_xpath("XPATH"), "Name")
```
Or you can inherit a class from Form class and use existing ElementFactory:
```python
self.my_text_box = self._element_factory.get_text_box(Locator.by_xpath("XPATH"), "Name")
```
6. Call element's methods to perform action with element:
```python
my_text_box.type("example@email.com")
```
7. Quit browser at the end:
```python
browser.quit()
```

### Configuration
This file is used to configure your browser settings, as well as other settings.By default, your solution will use the file from this project.

Copy the [following file](https://github.com/Polmik/py-selenium-auto/blob/main/py_selenium_auto/resources/settings.json) to your solution in `tests/resources` to configure it yourself

### License
Library's source code is made available under the [Apache 2.0 license](https://github.com/Polmik/py-selenium-auto/blob/main/LICENSE).