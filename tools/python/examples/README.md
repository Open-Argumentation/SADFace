# Using SADFace as a Python library

## basic_1.py
This file shows the basic steps involved in creating a SADFace document using a custom configuration file then doing the following to it:

* manipulating the title, notes, and description metadata, 
* adding an argument,
* adding a supporting argument
* adding a conflicting argument
* exporting a dot file for rendering using the Dot/GraphViz tool


This is what our SADFace JSON looks like:

~~~~
{
    "edges": [
        {
            "id": "ddb34a0f-6025-42d6-a893-2b04b28c78cc",
            "source_id": "81783b6f-10d1-41a3-9c0a-d815d59937e0",
            "target_id": "e04261af-d3fe-4c3f-be12-49b3b1aea783"
        },
        {
            "id": "7347e24c-5fd0-4049-b1c4-ef3436325e20",
            "source_id": "29bf3c6d-2a95-4983-8807-ae592798ff5e",
            "target_id": "81783b6f-10d1-41a3-9c0a-d815d59937e0"
        },
        {
            "id": "b4fa1944-a3ab-4962-b550-99bbe693c700",
            "source_id": "8c5dcb9e-cee3-4ddb-88a1-4b69f2aaa6c3",
            "target_id": "81783b6f-10d1-41a3-9c0a-d815d59937e0"
        },
        {
            "id": "6ca261ba-1ab5-4875-a5ce-1604727a37dd",
            "source_id": "9af8e365-6355-4cad-9df0-20e8316d320c",
            "target_id": "8c5dcb9e-cee3-4ddb-88a1-4b69f2aaa6c3"
        },
        {
            "id": "db667294-12d3-449e-8549-d50bcddd8f68",
            "source_id": "7de43d91-f616-4a1b-a057-bab66ec461e5",
            "target_id": "9af8e365-6355-4cad-9df0-20e8316d320c"
        },
        {
            "id": "43e0f7be-af22-4a19-919e-055d7045790e",
            "source_id": "1c2f78a5-1c01-45da-8ee1-055cb0922b30",
            "target_id": "9af8e365-6355-4cad-9df0-20e8316d320c"
        },
        {
            "id": "eaadf348-ad7b-44db-8ba2-ffa41d9c6204",
            "source_id": "27583f07-7d1b-4f08-8176-c8f2ed1f1ca0",
            "target_id": "8c5dcb9e-cee3-4ddb-88a1-4b69f2aaa6c3"
        },
        {
            "id": "5df0db48-9db1-4e1e-9aeb-7699f2ffacca",
            "source_id": "347c7451-b617-4418-b4e3-eb9308726ec2",
            "target_id": "27583f07-7d1b-4f08-8176-c8f2ed1f1ca0"
        }
    ],
    "metadata": {
        "core": {
            "analyst_email": "you-killed-my-father@prepare-to-die.com",
            "analyst_name": "Inigo Montoya",
            "created": "2020-06-25T09:40:20",
            "description": "a cohesive description of this argument document",
            "edited": "2020-06-25T09:40:20",
            "id": "a59e4cba-b501-40f6-a04b-f03d536a3bd1",
            "notes": "some nonsense about stuff...yet more notes n stuff",
            "title": "very important",
            "version": "0.2"
        }
    },
    "nodes": [
        {
            "id": "e04261af-d3fe-4c3f-be12-49b3b1aea783",
            "metadata": {
                "core": {}
            },
            "sources": [],
            "text": "You should treasure every moment",
            "type": "atom"
        },
        {
            "id": "81783b6f-10d1-41a3-9c0a-d815d59937e0",
            "metadata": {
                "core": {}
            },
            "name": "inference",
            "type": "scheme"
        },
        {
            "id": "29bf3c6d-2a95-4983-8807-ae592798ff5e",
            "metadata": {
                "core": {}
            },
            "sources": [],
            "text": "if you are going to die then you should treasure every moment",
            "type": "atom"
        },
        {
            "id": "8c5dcb9e-cee3-4ddb-88a1-4b69f2aaa6c3",
            "metadata": {
                "core": {}
            },
            "sources": [],
            "text": "You are going to die",
            "type": "atom"
        },
        {
            "id": "9af8e365-6355-4cad-9df0-20e8316d320c",
            "metadata": {
                "core": {}
            },
            "name": "support",
            "type": "scheme"
        },
        {
            "id": "7de43d91-f616-4a1b-a057-bab66ec461e5",
            "metadata": {
                "core": {}
            },
            "sources": [],
            "text": "Every person is going to die",
            "type": "atom"
        },
        {
            "id": "1c2f78a5-1c01-45da-8ee1-055cb0922b30",
            "metadata": {
                "core": {}
            },
            "sources": [],
            "text": "You are a person",
            "type": "atom"
        },
        {
            "id": "27583f07-7d1b-4f08-8176-c8f2ed1f1ca0",
            "metadata": {
                "core": {}
            },
            "name": "conflict",
            "type": "scheme"
        },
        {
            "id": "347c7451-b617-4418-b4e3-eb9308726ec2",
            "metadata": {
                "core": {}
            },
            "sources": [],
            "text": "YOLO",
            "type": "atom"
        }
    ],
    "resources": []
}
~~~~

This is what the converted Dot file looks like:

~~~~
digraph SADFace {node [style="filled"]"98065126-12f9-4085-b29a-541ecb2010de" [label="You should treasure every
moment"] [shape=box, style=rounded];
"52811614-50b0-471e-b7bf-b9db5334e619" [label="inference"] [colorscheme=X11, fillcolor=cornsilk4, shape=diamond];
"daca4f24-4a99-49be-b3e3-e30321613fe6" [label="if you are going to die
then you should treasure
every moment"] [shape=box, style=rounded];
"6cec2482-2fa9-412d-8828-fd39dead9afb" [label="You are going to die"] [shape=box, style=rounded];
"f48ab0d2-f5c5-4ce9-b7ff-34f08f8a00a0" [label="support"] [colorscheme=X11, fillcolor=darkolivegreen3, shape=diamond];
"fb4c91f2-7cc3-45e0-a2bb-80a4da168555" [label="Every person is going to
die"] [shape=box, style=rounded];
"36ac8cd6-3bad-4b2f-b2e1-a9f412a7fb6d" [label="You are a person"] [shape=box, style=rounded];
"96c9b268-3a62-42f2-a4a1-061e424522bc" [label="conflict"] [colorscheme=X11, fillcolor=firebrick2, shape=diamond];
"62471cc3-855b-440b-9825-3f2a0d0bd86b" [label="YOLO"] [shape=box, style=rounded];
"52811614-50b0-471e-b7bf-b9db5334e619" -> "98065126-12f9-4085-b29a-541ecb2010de";
"daca4f24-4a99-49be-b3e3-e30321613fe6" -> "52811614-50b0-471e-b7bf-b9db5334e619";
"6cec2482-2fa9-412d-8828-fd39dead9afb" -> "52811614-50b0-471e-b7bf-b9db5334e619";
"f48ab0d2-f5c5-4ce9-b7ff-34f08f8a00a0" -> "6cec2482-2fa9-412d-8828-fd39dead9afb";
"fb4c91f2-7cc3-45e0-a2bb-80a4da168555" -> "f48ab0d2-f5c5-4ce9-b7ff-34f08f8a00a0";
"36ac8cd6-3bad-4b2f-b2e1-a9f412a7fb6d" -> "f48ab0d2-f5c5-4ce9-b7ff-34f08f8a00a0";
"96c9b268-3a62-42f2-a4a1-061e424522bc" -> "6cec2482-2fa9-412d-8828-fd39dead9afb";
"62471cc3-855b-440b-9825-3f2a0d0bd86b" -> "96c9b268-3a62-42f2-a4a1-061e424522bc";
}
~~~~

Finally, our file rendered to PNG.

![alt text](https://raw.githubusercontent.com/siwells/SADFace/master/tools/python/examples/out.png "Argument constructed in basic_1.py")

### GraphViz/Dot Rendering

You can convert the exported dot file to a PDF using a command like the following (assuming you have Dot/GraphViz installed):

      $ dot out.dot -Tpdf -o out.pdf

Notice that you can alter the colouring used in the call to export_dot() by setting the trad=False flag. This suppresses the traditional red=conflict, green=support colouring & uses a Brewer colourscheme instead.
