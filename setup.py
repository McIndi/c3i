from setuptools import setup
import platform

if "Windows" in platform.system():
    requires = ["pywin32", "pyreadline"]
elif "Linux" in platform.system():
    requires = []
requires += ["cherrypy", "bottle"]

setup(
    name="c3i",
    version="0.6.0"
    author="iLoveTux",
    author_email="me@ilovetux.com",
    install_requires=requires,
    description="A simple, teachable, cross-platform daemon.",
    url="https://github.com/mcindi/c3i",
    packages=["c3i", "c3i.plugins"],
    entry_points={
        'console_scripts': [
            'c3i-start=c3i.c3i:main',
            'c3id=c3i.__main__:main'   
        ],
        'c3i_plugin': [
            'config=c3i.plugins.config:plugin',
            'github=c3i.plugins.github:plugin',
        ]
    }
)

