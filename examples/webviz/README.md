# Embedding SADFace Documents into Web Pages

We can use SADFace to create visualling pleasing visualisations of arguments for embedding into arbitrary web-pages. The easiest way is to just convert the SADFace document into dot format then to render this into a PNG, JPG, or other graphcis format.

However, Scalable Vector Graphics (SVG) are a good, future proof way to embed visual data into web-pages that are scalable, so work nicely across different devices, and are text based, so can be indexed by web-search engines.

In the following examples we assume that you've got a SADFace document to work with, either from an existing dataset, created using a SADFace tool (see the tools folder of this repo) or else using an argument analysis tool like [MonkeyPuzzle](http://arg.napier.ac.uk/monkeypuzzle/) that exports to SADFace.

## Exporting to Dot

If you have the SADFace command-line tools installed then you can use them to take a json file as input and export to an output dot file, for example (assuming a SADFace file called in.json and a personal config file called simon.cfg):

        $ python src/repl.py -c etc/simon.cfg -l in.json --exportdot

This should give you a dot file as output which you can pass through the dot program to visualise

## Converting Dot to other image formates

Now you can use the dot tool to convert your dot file into an image file (assuming our dot file is out.dot):

        $ dot out.dot -Tpng -o out.png

More detailed information can be found in the GraphViz/Dot documentation

## Embedding Dot in a web page

We can use the [viz.js JavaScript library](http://viz-js.com/), which is a version of GraphViz/dot for the web. This effectively enables you to dynamically render a source dot file into an SVG image dynamically on a web-page. The file, index.html, contains a simple example of embedding an argument into a web page. The dot source of the argument is stored in args.js and web workers are used to generate the SVG in the background when the page is loaded. This requires the two additional JavaScript files, viz.js and full.render.js to be included. The version of viz.js that is used by this example is v2.1.2 but any recent version should work well.
