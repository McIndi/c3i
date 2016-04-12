# C3I

__What is c3I?__

C3I stands for Command and Control Center with Information. C3I Was designed
to address some of the shortcomings which arise from the dogma surrounding
the IT industry.

C3I is a secure, configurable and teachable cross-platform daemon. It is
compatible with Windows and Linux and runs on Python 2.7 and 3.5.

Out-of-the-box C3I does nothing, but by writing simple plugins, you can
extend it's functionality to do just about anything.

__What is a plugin?__

A C3I Plugin is simply a Python module which registers itself using a
setuptools `entry_point` and points to a callable which accepts a `dict`
containing the C3I configuration and returns a WSGI application. This
application will be served over `https` at a URI of the plugins name.

For instace if the plugin is called `foo` and C3I is configured to listen on
port `8080`, then the plugin will be accessable from `https://hostname:8080/foo`

__What do you use it for?__

The short answer is `anything`, but we designed it to be used to control
our configuration and infrastructure as well as handle our Continuous
Integration and Delivery. By issuing a request to a C3I instance we can now

* Deploy new servers to our develoopment, QA and production environment
* See if any of our source code changed
* Kick off our Continuous Integration and Delivery Pipeline (Although this one
is also called automatically by a git hook)
* Add a user to a group of systems
* Get a look at the performance of our systems

# Installation

Installation is simple:

For bleeding-edge features:

```bash
$ git clone https://github.com/ilovetux/c3i
$ cd c3i
$ python setup.py install
```

For the latest stable version

```bash
$ pip install c3i
```

# Usage

After installation, you will have a command `c3i` which can be used to
install, remove, start and stop the daemon, but there will be no plugins and
thus no functionality yet. To install a plugin simply `pip` install it or 
`python setup.py install` it, and c3i will pick it up on the next restart of
the service.

To disable a plugin simply add the plugins name to a key called
`exclude_plugins` in `config.json` for instance:

```bash
$ cat ~/.c3i/config.json
{
...
    "exclude_plugins": ["foo_plugin"]
...
}
```

# Creating a plugin

A plugin is a Python module which registers a callable which accepts the
configuration and returns a WSGI application. A simple plugin might look like
this:

```bash
foo
├── foo
│   └── __init__.py
├── test
│   ├── __init__.py
│   └── test_foo.py
├── README.md
├── setup.py
└── tox.ini
```

and in `setup.py`:

```python
from setuptools import setup

setup(
    name="foo",
    author="your name",
    author_email="your@email.com",
    install_requires=["c3i"],
    description="A c3i plugin for foo",
    url="https://your.domain.com/foo",
    packages=["foo"],
    entry_points={
        'c3i_plugin': [
            'foo=foo:plugin'
        ]
    }
)
```

and in `foo/__init__.py`

```python
import bottle

def plugin(config):
    app = bottle.Bottle(__name__)

    @app.route("/")
    def do_foo():
        return {"foo": "bar", "baz": "foobar"}

    return app
```

# Recomendations for plugin design

This section is subject to change, but for a quick list of considerations
please take a look:

* C3I is served over `https`, but provides no RBM type functionality, this
was decided upon to simplify and to remove dogma, but if your plugin could
be misused, please add the RBM pieces yourself. If you want to do something
quickly, consider using `bottle` with the `bottle-cork` package as it supports
most simple use cases.
* It is recomended to consume and return JSON documents, this standardizes and
simplifies interacting with the plugins. If you wish to provide a gui or a CLI
command you should make them speak JSON to your plugin. This way someone else
can simply re-implement your clients if they don't like yours.
* On the first run of your plugin, you should add a section in `config.json`
containing the default configuration for your plugin.
* Keep in mind that a common use case for C3I is to have an installation on
each of the systems in an environment to act as an agent and to have an
installation on one server to communicate to all the agents. If you want to
design multiple pieces of functionality like gathering metrics and controling
the servers, you should have an agent plugin and a master plugin. They should
be able to run from different machines or from the same machine.

Have some more tips and tricks, please open an
[issue](https://github.com/mcindi/c3i/issues) 

# List of official plugins

C3I is pretty young and we haven't released any official plugins yet, but we
will soon. Stay tuned.

# List of recomended third party plugins

C3I is pretty young and we haven't come across any plugins from anyone
else yet, if you made one or know of one you would like to be included here
please submit an [issue](https://github.com/mcindi/c3i/issues).
