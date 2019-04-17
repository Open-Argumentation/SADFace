# SADFace Python Package

## QuickStart

SADFace can currently be used in three ways, as a Python library, to builds SADFace documents from an existing argument tool, as a command line application, and using the inbuilt REPL.

### Library

SADFace can be used as a Python library using a standard import statement, e.g.

~~~~
 import sadface
~~~~



### Command Line Tool

SADFace can be used as a standard CLI tool. SADFace files can be loaded, manipulated, saved, and exported.
~~~~
 $ python src/sadface.py -c deploy/etc/simon.cfg
~~~~

The CLI tool will interact with other CLI tools using standard pipes to move data between apps. For example, the following pipeline will, assuming you have the GraphViz dot tool installed, convert the SADFace document into a png:

~~~~
 $ python src/repl.py -c deploy/etc/simon.cfg -l deploy/out/death.json --exportdot | dot -Tpng -o death.png
~~~~

Import an Argument Markup Language (AML) file and parse into a SADFace document:

~~~~
$ python src/repl.py -c deploy/etc/simon.cfg --aml file.aml --pretty
~~~~

Note that AML support is experimental. It supports extraction of ROOT, AU, CA, LA, REFUTATION, PROP, & TEXT nodes. Support for extraction of scheme information is in the SADFace development plan.


### REPL

SADFace can be used interactively by invoking the REPL, e.g.

~~~~
 $ python src/repl.py -i
~~~~

This will launch SADFace in interactive mode. If you have a config file then this can be passed in using the -c argument, e.g.

~~~~
 $ python src/sadface.py -c deploy/etc/simon.cfg -i
~~~~

Once you are presented with the REPL UI you can manipulate with your SADFace document interactively, for example, loading, editing, saving, and exporting the SADFace document. The best place to start is to run the REPL then use the built-in help feature, e.g.

~~~~
The SADFace REPL. Type 'help' or 'help <command>' for assistance
> help

~~~~

### Run the tests

Add application src to the PYTHONPATH:

~~~~
    $ PYTHONPATH=`pwd`/src
~~~~

Run the tests:

~~~~
    $ python test/sadface_test.py
~~~~
