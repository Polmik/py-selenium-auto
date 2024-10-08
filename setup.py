import setuptools


def _open(filename):
    return open(filename, encoding="utf-8")


# Getting description:
with _open("README.md") as readme_file:
    description = readme_file.read()

# Getting requirements:
with _open("requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()

setuptools.setup(name="py-selenium-auto",
                 version="0.4.7",
                 description="Selenium for Python",
                 long_description=description,
                 long_description_content_type="text/markdown",
                 author="Egor Ryaboshapko",
                 author_email="mrpolmik@hotmail.com",
                 maintainer="Egor Ryaboshapko",
                 maintainer_email="mrpolmik@hotmail.com",
                 url="https://github.com/Polmik/py-selenium-auto",
                 license="Apache",
                 license_files=('LICENSE',),
                 keywords=['testing', 'selenium', 'driver', 'test automation'],
                 include_package_data=True,
                 packages=setuptools.find_packages(include=['py_selenium_auto*']),
                 install_requires=requirements,
                 zip_safe=True,
                 platforms=["any"],
                 classifiers=[
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 3.7",
                     "Programming Language :: Python :: 3.8",
                     "Programming Language :: Python :: 3.9",
                     "Programming Language :: Python :: 3.10",
                     "Programming Language :: Python :: 3.11",
                     "Programming Language :: Python :: 3.12",
                     "Programming Language :: Python :: Implementation :: PyPy",
                     "Framework :: Pytest",
                     "Topic :: Software Development",
                     "Topic :: Software Development :: Libraries",
                     "Topic :: Software Development :: Libraries :: Python Modules",
                 ])
