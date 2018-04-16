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
    "analyst_email": "siwells@gmail.com", 
    "analyst_name": "Simon Wells", 
    "created": "2017-07-11T16:32:36", 
    "edges": [
        {
            "id": "d7bcef81-0d74-4ae5-96f9-bfb07031f1fa", 
            "source_id": "49a786ce-9066-4230-8e18-42086882a160", 
            "target_id": "9bfb7cdc-116f-47f5-b85d-ff7c5d329f45"
        }, 
        {
            "id": "f57ecb48-dfd5-4789-b3c5-46f770f4113d", 
            "source_id": "30c9c0ac-ddef-44e7-897d-52ffee97b837", 
            "target_id": "49a786ce-9066-4230-8e18-42086882a160"
        }, 
        {
            "id": "c48c3d75-a8b3-439a-9a2f-b987eaae2c9a", 
            "source_id": "02b4009b-1a12-4d53-ab3a-efabe6c44694", 
            "target_id": "49a786ce-9066-4230-8e18-42086882a160"
        }, 
        {
            "id": "86e797aa-ecb0-4fcd-8838-263ceedb099e", 
            "source_id": "5760a93a-55e7-447c-a245-7f8d7e7e4434", 
            "target_id": "02b4009b-1a12-4d53-ab3a-efabe6c44694"
        }, 
        {
            "id": "b2531a60-6559-4560-b57b-320f1f3b8386", 
            "source_id": "fbaa9b79-0965-45a1-9fd4-60701c2102cf", 
            "target_id": "5760a93a-55e7-447c-a245-7f8d7e7e4434"
        }
    ], 
    "edited": "2017-07-11T16:32:36", 
    "id": "94a975db-25ae-4d25-93cc-1c07c932e2f8", 
    "metadata": {}, 
    "nodes": [
        {
            "id": "9bfb7cdc-116f-47f5-b85d-ff7c5d329f45", 
            "metadata": {}, 
            "sources": [], 
            "text": "The 'Hang Back' campaign video should not have been published, and should be withdrawn.", 
            "type": "atom"
        }, 
        {
            "id": "49a786ce-9066-4230-8e18-42086882a160",
            "metadata": {},
            "name": "support", 
            "type": "scheme"
        }, 
        {
            "id": "30c9c0ac-ddef-44e7-897d-52ffee97b837", 
            "metadata": {}, 
            "sources": [], 
            "text": "The 'Hang Back' advert does not clearly express the intended message", 
            "type": "atom"
        }, 
        {
            "id": "02b4009b-1a12-4d53-ab3a-efabe6c44694", 
            "metadata": {}, 
            "sources": [], 
            "text": "The 'Hang Back' campaign was the wrong campaign to run", 
            "type": "atom"
        }, 
        {
            "id": "5760a93a-55e7-447c-a245-7f8d7e7e4434",
            "metadata": {},
            "name": "conflict", 
            "type": "scheme"
        }, 
        {
            "id": "fbaa9b79-0965-45a1-9fd4-60701c2102cf", 
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

