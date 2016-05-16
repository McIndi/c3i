import os
import sys
import util
import json
import readline
import argparse
import platform


setup_template = """
from setuptools import setup

setup(
    name="{name}",
    version="0.1.0",
    author="AUTHOR",
    author_email="AUTHOR@EMAIL.COM",
    install_requires=["bottle"],
    description="SHORT DESCRIPTION.",
    url="https://github.com/AUTHOR/{name}",
    packages=["{name}"],
    entry_points={{
        'c3i_plugin': [
            '{name}={name}:plugin',
        ]
    }}
)
"""

init_template = """
import bottle

def plugin(config):
    app = bottle.Bottle(__name__)

    @app.route("/")
    def return_config():
        return ""

    return app
"""

test_init_template = """
import unittest

class Test{name}(unittest.TestCase):
    # Add tests here
    pass
"""


if not os.path.exists(util.c3i_home()):
    util.first_run()

with open(util.c3i_config(), "r") as fin:
    config = json.load(fin)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    return parser.parse_args(argv)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    args = parse_args(argv)

    os.mkdir(args.name)
    os.mkdir(os.path.join(args.name, args.name))
    with open(os.path.join(args.name, "setup.py"), "w") as fout:
        fout.write(setup_template.format(name=args.name))
    with open(os.path.join(args.name, args.name, "__init__.py"), "w") as fout:
        fout.write(init_template)
    os.mkdir(os.path.join(args.name, "test"))
    with open(os.path.join(args.name, "test", "__init__.py"), "w") as fout:
        fout.write(test_init_template.format(name=args.name))
    print "Plugin template created for {}".format(args.name)


if __name__ == "__main__":
    main()
