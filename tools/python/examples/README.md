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
    "analyst_email": "siwells@gmail.com", 
    "analyst_name": "Simon Wells", 
    "created": "2019-03-12T18:46:14", 
    "edges": [
        {
            "id": "17828bd5-e8cb-4766-8b01-8f166cba391e", 
            "source_id": "e13a77bc-475c-4af4-aac6-c34eee733d0d", 
            "target_id": "e50b9246-246d-4f6d-8ba4-fd3c4f4416d7"
        }, 
        {
            "id": "b75db6dd-971c-4225-8499-04edde5a4521", 
            "source_id": "a3686491-08ca-426d-b792-c6d201605690", 
            "target_id": "e13a77bc-475c-4af4-aac6-c34eee733d0d"
        }, 
        {
            "id": "251fb6ff-1b9b-4513-8cb3-c316019cb9a6", 
            "source_id": "6d42bc33-423d-455b-ae67-c252c800fbf9", 
            "target_id": "e13a77bc-475c-4af4-aac6-c34eee733d0d"
        }, 
        {
            "id": "10feab16-4bf1-441c-98bc-8fbe2fe453aa", 
            "source_id": "0fd46018-7cab-4a2c-ab1c-4f17d4c7d072", 
            "target_id": "6d42bc33-423d-455b-ae67-c252c800fbf9"
        }, 
        {
            "id": "b4a1e683-63f7-4206-8eb7-5003afeae1fa", 
            "source_id": "e5ae3db2-8fbb-4c0f-a708-eccdc665cbbc", 
            "target_id": "0fd46018-7cab-4a2c-ab1c-4f17d4c7d072"
        }, 
        {
            "id": "86f4469d-ead7-4091-a946-00c3c5309a70", 
            "source_id": "5221139d-2ee2-458a-8547-569ff36262eb", 
            "target_id": "0fd46018-7cab-4a2c-ab1c-4f17d4c7d072"
        }, 
        {
            "id": "a2e21223-603c-4372-b558-4b0e73629abd", 
            "source_id": "70bf08b6-5f56-4ee9-8405-fc92d21cb1a9", 
            "target_id": "6d42bc33-423d-455b-ae67-c252c800fbf9"
        }, 
        {
            "id": "4c62e434-35a0-447b-81d2-17749dc57a93", 
            "source_id": "6d57fbec-4198-4f3f-8470-40a1a649bcc8", 
            "target_id": "70bf08b6-5f56-4ee9-8405-fc92d21cb1a9"
        }
    ], 
    "edited": "2019-03-12T18:46:14", 
    "id": "45a8601c-c42f-492a-9b56-a97bb4af6879", 
    "metadata": {
        "core": {
            "description": "a cohesive description of this argument document", 
            "notes": "some nonsense about stuff...yet more notes n stuff", 
            "title": "very important"
        }
    }, 
    "nodes": [
        {
            "id": "e50b9246-246d-4f6d-8ba4-fd3c4f4416d7", 
            "metadata": {}, 
            "sources": [], 
            "text": "You should treasure every moment", 
            "type": "atom"
        }, 
        {
            "id": "e13a77bc-475c-4af4-aac6-c34eee733d0d", 
            "metadata": {}, 
            "name": "inference", 
            "type": "scheme"
        }, 
        {
            "id": "a3686491-08ca-426d-b792-c6d201605690", 
            "metadata": {}, 
            "sources": [], 
            "text": "if you are going to die then you should treasure every moment", 
            "type": "atom"
        }, 
        {
            "id": "6d42bc33-423d-455b-ae67-c252c800fbf9", 
            "metadata": {}, 
            "sources": [], 
            "text": "You are going to die", 
            "type": "atom"
        }, 
        {
            "id": "0fd46018-7cab-4a2c-ab1c-4f17d4c7d072", 
            "metadata": {}, 
            "name": "support", 
            "type": "scheme"
        }, 
        {
            "id": "e5ae3db2-8fbb-4c0f-a708-eccdc665cbbc", 
            "metadata": {}, 
            "sources": [], 
            "text": "Every person is going to die", 
            "type": "atom"
        }, 
        {
            "id": "5221139d-2ee2-458a-8547-569ff36262eb", 
            "metadata": {}, 
            "sources": [], 
            "text": "You are a person", 
            "type": "atom"
        }, 
        {
            "id": "70bf08b6-5f56-4ee9-8405-fc92d21cb1a9", 
            "metadata": {}, 
            "name": "conflict", 
            "type": "scheme"
        }, 
        {
            "id": "6d57fbec-4198-4f3f-8470-40a1a649bcc8", 
            "metadata": {}, 
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
