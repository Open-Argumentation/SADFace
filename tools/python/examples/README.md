# Using SADFace as a Python library

## basic_1.py
This file shows the basic steps involved in creating a SADFace document using a custom configuration file then doing the following to it:

* manipulating the title, notes, and description metadata, 
* adding an argument,
* adding a supporting argument
* adding a conflicting argument
* exporting a dot file for rendering using the Dot/GraphViz tool


### GraphViz/Dot Rendering

You can convert the exported dot file to a PDF using a comman like the following:

      $ dot out.dot -Tpdf -o out.pdf

Notice that you can alter the colouring used in the call to export_dot() by setting the trad=False flag. This suppresses the traditional red=conflict, green=support colouring & uses a Brewer colourscheme instead.
