# SADFace Python Package

## QuickStart

SADFace can currently be used in three ways, as a Python library, to builds SADFace documents from an existing argument tool, as a command line application, and using the inbuilt REPL. SADFace is currently developed and tested under Python 3 so, your mileage may vary under earlier versions (Note that the bulk of development was actually completed under Python 2.7 and very few alterations were needed for the Python 3 migration so you may well be in luck).


### Installation

Install SADFace as follows. If you have cloned the source repository then you can run the following:

~~~~
 $ pip install setup.py
~~~~

NB. In this case it might be worth considering running with the -e argument (see the discussion in the 'Run The Tests' section below), especially if you are intent on hacking on SADFace.


### Library

SADFace can be used as a Python library using a standard import statement, e.g.

~~~~
 import sadface
~~~~

If you are in the Python REPL (or similar) then you can explore the SADFace package API using:

~~~~
 dir(sadface)
~~~~



### Command Line Tool

SADFace can be used as a standard CLI tool. SADFace files can be loaded, manipulated, saved, and exported.
~~~~
 $ python -m sadface -c deploy/etc/simon.cfg
~~~~

The CLI tool will interact with other CLI tools using standard pipes to move data between apps. For example, the following pipeline will, assuming you have the GraphViz dot tool installed, convert the SADFace document into a png:

~~~~
 $ python -m sadface -c deploy/etc/simon.cfg -l deploy/out/death.json --exportdot | dot -Tpng -o death.png
~~~~

Import an Argument Markup Language (AML) file and parse into a SADFace document:

~~~~
$ python -m sadface -c deploy/etc/simon.cfg --aml file.aml --pretty
~~~~

Note that AML support is experimental. It supports extraction of ROOT, AU, CA, LA, REFUTATION, PROP, & TEXT nodes. Support for extraction of scheme information is in the SADFace development plan.


### REPL

SADFace can be used interactively by invoking the REPL, e.g.

~~~~
 $  python -m sadface  -i
~~~~

This will launch SADFace in interactive mode. If you have a config file then this can be passed in using the -c argument, e.g.

~~~~
 $  python -m sadface -c deploy/etc/simon.cfg -i
~~~~

Once you are presented with the REPL UI you can manipulate with your SADFace document interactively, for example, loading, editing, saving, and exporting the SADFace document. The best place to start is to run the REPL then use the built-in help feature, e.g.

~~~~
The SADFace REPL. Type 'help' or 'help <command>' for assistance
> help

~~~~

### Run the tests

Relative to the tools/python folder. If sadface and sadface_tests are either not on the PYTHONPATH or else haven't been installed using pip then you need to handle this so that the Sadface and Sadface Test packages can be found by Python, Either:

~~~~
    $ PYTHONPATH=`pwd`/sadface:`pwd`/tests
~~~~

Or else use setup.py of each package and pip to install them, e.g. go into each source folder (src/sadface and src/sadface_tests) and:

~~~~
    $ pip install -e .
~~~~

This second approach is really useful if you want to hack on the SADFace source code as the -e switch enables you to make changes to either source or tests and these are picked up in your python path. NB. I do recommend working in a virtualenv.

Now run the tests, either by module:

~~~~
    $ python -m unittest -v tests/*_test.py
~~~~

Or through test discovery:
~~~~
    $ python -m unittest discover -s tests/ -p '*_test.py' -v
~~~~
