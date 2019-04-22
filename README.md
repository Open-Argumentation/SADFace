# SADFace

The Simple Argument Description Format (SADFace) is a JSON-based document format for describing analysed argument structure and associated meta-data. The aim of this work is to build argument tools for the web. That is simple, flexible, extensible tools that fit into existing web-workflows and tool-chains. A developer should be able to adopt SADFace and start describing arguments or using those descriptions, really easily. Parsing a SADFace document into a Javascript application should not require any special tools, it is just JSON. The structure of the format has been designed to align with a straightforward model of argument structure, defined in such a way as to align with most of the intuitions that an everyday understanding of argument will include, whilst still supporting more advanced features.

## Underlying Model

Arguments are made up from statements (or strings if you're a programmer) that capture a "claim". We call these statements "Argument Atoms", or just "atoms". A simple argument is a collection of such atoms that are linked together. For a simple argument we generally say that one of the atoms is a conclusion, and the other atoms are premises. The exact way that premises support a conclusion is defined by argumentation schemes. An argumentation scheme captures a stereotypical pattern of argumentative reasoning, so different arguments can be categorised into different types. A rough rule of thumb is to say that every individual argument is an instance of an argumentation scheme.

The underlying model of SADFace is the Mathematical Graph, a collection of nodes connected together by edges. More spectifically, SADFace uses a directed graph. In this case the edges have a direction, they claim a relationship that works in a particular direction between any pair of nodes that are connected by a given edge. A SADFace document contains a set of nodes and a set of edges. Edges are quite simple, they have an ID so that the instance of the edge can be uniquely identified from all other edges, and they also have a source and a target. The source and target in an edge are both IDs of nodes, i.e. the ID of the node that this edge goes from, the source ID, and the ID of the node that this edge goes to, the target ID. Nodes are slightly more complicated, currently there are two types of node, atom nodes and scheme nodes. Atoms and schemes are linked together using the aforementioned edges. There are also some restrictions upon which types of node can be lined directly to each other:

1. Atoms cannot be linked directly to each other. They must be linked via a Scheme node. This is in line with the underlying model of the Argument Interchange Format (AIF) which restricts Information or i-nodes, the equivalent of our Atoms, from being linked directly to each other. This is an important restriction as it means that for every link between a pair of atoms, for the link to be valid, it must define a known argumentative relationship.




## Example SADFace Document

This is what a simple SADFace document looks like:

~~~~
{
    "edges": [
        {
            "id": "3df54ae1-fa41-4ac7-85d5-4badee39215b",
            "source_id": "70447169-9264-41dc-b8e9-50523f8368c1",
            "target_id": "ae3f0c7f-9f69-4cab-9db3-3b9c46f56e09"
        },
        {
            "id": "64430e6e-1300-4623-9b89-3c014587f7ae",
            "source_id": "f129934f-53d2-49f6-8feb-9afaff9aabcf",
            "target_id": "70447169-9264-41dc-b8e9-50523f8368c1"
        },
        {
            "id": "1aae6f5e-f1a7-4873-aa64-a606a0e481cd",
            "source_id": "6cd219cc-3203-4602-88bd-d3639f86fb37",
            "target_id": "70447169-9264-41dc-b8e9-50523f8368c1"
        },
        {
            "id": "bfe3db02-f93f-4d91-bd78-beccee980175",
            "source_id": "45199aa0-1556-4b94-8940-3ba30aa08e38",
            "target_id": "f129934f-53d2-49f6-8feb-9afaff9aabcf"
        },
        {
            "id": "3c2f9db7-3b78-4bc0-b990-3d0eacdca90e",
            "source_id": "51775eb3-70c0-4d8e-95a5-b34ffba8a280",
            "target_id": "45199aa0-1556-4b94-8940-3ba30aa08e38"
        }
    ],
    "metadata": {
        "core": {
            "analyst_email": "siwells@gmail.com",
            "analyst_name": "Simon Wells",
            "created": "2019-04-22T23:52:30",
            "description": "An example SADFace document showing an argument analysis of the Hangback cycle safety campaign from the STCD corpora.",
            "edited": "2019-04-22T23:52:30",
            "id": "42e56df7-4074-40d8-8ea1-4fca5321dd31",
            "notes": "This is incomplete because the analysis in Pangbourne & Wells (2018) has much more argumenative content.",
            "title": "Hangback Example",
            "version": "0.2"
        }
    },
    "nodes": [
        {
            "id": "ae3f0c7f-9f69-4cab-9db3-3b9c46f56e09",
            "metadata": {},
            "sources": [],
            "text": "The 'Hang Back' campaign video should not have been published, and should be withdrawn.",
            "type": "atom"
        },
        {
            "id": "70447169-9264-41dc-b8e9-50523f8368c1",
            "metadata": {},
            "name": "support",
            "type": "scheme"
        },
        {
            "id": "f129934f-53d2-49f6-8feb-9afaff9aabcf",
            "metadata": {},
            "sources": [],
            "text": "The 'Hang Back' campaign was the wrong campaign to run",
            "type": "atom"
        },
        {
            "id": "6cd219cc-3203-4602-88bd-d3639f86fb37",
            "metadata": {},
            "sources": [],
            "text": "The 'Hang Back' advert does not clearly express the intended message",
            "type": "atom"
        },
        {
            "id": "45199aa0-1556-4b94-8940-3ba30aa08e38",
            "metadata": {},
            "name": "conflict",
            "type": "scheme"
        },
        {
            "id": "51775eb3-70c0-4d8e-95a5-b34ffba8a280",
            "metadata": {},
            "sources": [],
            "text": "Road users have a responsibility to make our roads safer by being more vigilant.",
            "type": "atom"
        }
    ],
    "resources": []
}
~~~~

This is what the argument contained in that document looks like when exported to the Dot format:

![alt text](https://raw.githubusercontent.com/siwells/SADFace/master/examples/hangback/data.png "Extract from the Hang Back analysis")

