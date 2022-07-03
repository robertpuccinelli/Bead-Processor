import setuptools

setuptools.setup(
    name="beadprocessor",
    version="0.0.1",
    author="Robert R. Puccinelli",
    author_email="robert.puccinelli@outlook.com",
    description="Automated magnetic bead proccessor project and utilities.",
    url="https://github.com/robert.puccinelli/bead_processor.git",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*",
                                               "tests.*", "tests"]),
    install_requires=[
        'pymotors@git+https://github.com/czbiohub/PyMotors#egg=pymotors',
        'pyconfighandler@git+https://github.com/czbiohub/PyConfigHandler#egg=pyconfighandler',
        'pybuttons@git+https://github.com/czbiohub/PyButtons#egg=pybuttons',
        'RPi.GPIO',
    ],
    test_suite="tests",
    classifiers=[
        "Puccinelli :: Bioengineering",
    ],
)