#!/usr/bin/python

import uuid

from . import sadface


def check_edges_block(doc):
    """
    The edges block is a list of edges within the SADFace document and is a required
    part of a well formed SADFace document
    """
    problems = []

    if doc.get("edges") == None:
        problems.append("No 'edges' block")
    else:
        if type(doc.get("edges")) is not list:
            problems.append("Edges block is not a list")
        for edge in doc.get("edges"):
            if type(edge) is not dict:
                problems.append("Edges block has a member that is not a dict/object")

            if "id" not in edge:
                problems.append("Edge has no 'id' key")
            else:
                edge_id = edge.get("id")
                try:
                    uuid.UUID(edge_id, version=4)
                except:
                    problems.append("'edge_id' is not an instance of UUID4") 
                    
            if "source_id" not in edge:
                problems.append("Edge has no 'source_id' key")
            else:
                source_id = edge.get("source_id")
                try:
                    uuid.UUID(source_id, version=4)
                except:
                    problems.append("'source_id' is not an instance of UUID4")

            if "target_id" not in edge:
                problems.append("Edge has no 'target_id' key")
            else:
                target_id = edge.get("target_id")
                try:
                    uuid.UUID(target_id, version=4)
                except:
                    problems.append("'target_id' is not an instance of UUID4")

            for key in edge.keys():
                if key not in ["id", "source_id", "target_id"]:
                    problems.append("Edge contains the invalid key: "+key)
                    
    return problems

def check_global_metadata_block(doc):
    """
    The global metadata block is a collection of objects, each of which contains information
    about the current document. A core collection is a required part of the global metadata
    block and is reserved for SADFace metadata only. Additional metadata can be stored in
    user defined metadata blocks that are named uniquely and store key:value pairs.

    Global metadata is a required part of a well formed SADFace document

    """
    problems = []

    if doc.get("metadata") == None:
        problems.append("No 'metadata' block")
    else:
        if type(doc.get("metadata")) is not dict:
            problems.append("Metadata block is not a dict/object")
        else:
            if doc.get("metadata").get("core") is None:
                problems.append("No 'core' block in metadata")
            else:
                core = doc.get("metadata").get("core")
                if type(core) is not dict:
                    problems.append("Metadata core block is not a dict/object")
                
                if "analyst_email" not in core:
                    problems.append("'analyst_email' key is not in the core metadata block")
                else:
                    analyst_email = core.get("analyst_email")
                    if type(analyst_email) is not str:
                        problems.append("'analyst_email' in core metadata is not a string")

                if "analyst_name" not in core:
                    problems.append("'analyst_name' key is not in the core metadata block")
                else:
                    analyst_name = core.get("analyst_name")
                    if type(analyst_name) is not str:
                        problems.append("'analyst_name' in core metadata is not a string")

                if "created" not in core:
                    problems.append("'created' key is not in the core metadata block")
                else:
                    created = core.get("created")
                    if type(created) is not str:
                        problems.append("'created' in core metadata is not a string")
                
                if "edited" not in core:
                    problems.append("'edited' key is not in the core metadata block")
                else:
                    edited = core.get("edited")
                    if type(edited) is not str:
                        problems.append("'edited' in core metadata is not a string")

                if "id" not in core:
                    problems.append("'id' key is not in the core metadata block")
                else:
                    core_id = core.get("id")
                    if type(core_id) is not str:
                        problems.append("'id' in core metadata is not a string")

                if "version" not in core:
                    problems.append("'version' key is not in the core metadata block")
                else:
                    version = core.get("version")
                    if type(version) is not str:
                        problems.append("'version' in core metadata is not a string")

                for key in core.keys():
                    if key not in ["analyst_email", "analyst_name", "created", "edited", "id", "version"]:
                        problems.append("Edge contains the invalid key: "+key)
            
            for block in doc.get("metadata"):
                obj = doc.get("metadata").get(block)
                if type(obj) is not dict:
                    problems.append("Metadata contains a block that is not a dict/object:"+str(block))

    return problems

def check_node_type_atom(atom):
    """
    Atoms are a specific type of node in a SADFace graph. They have an associated set of data that
    is required for an Atom to be considered well formed.
    """
    problems = []

    if "text" not in atom:
        problems.append("No 'text' key in Atom Node")
    else:
        text = atom.get("text")
        if type(text) is not str:
            problems.append("'text' in Atom Node is not a string")

    if "sources" not in atom:
        problems.append("No 'text' key in Atom Node")
    else:
        text = atom.get("text")
        if type(text) is not str:
            problems.append("'text' in Atom Node is not a string")
    
    return problems

def check_node_type_scheme(scheme):
    """
    Schemes are a specific type of node in a SADFace graph. They have an associated set of data that
    is required for a Scheme to be considered well formed.

    """
    problems = []

    if "name" not in atom:
        problems.append("No 'name' key in Scheme Node")
    else:
        name = atom.get("name")
        if type(name) is not str:
            problems.append("'name' in Atom Node is not a string")
    
    return problems

def check_nodes_block(doc):
    """
    Nodes hold data within a SADFace graph and are connected by Edges. Nodes have a common associated 
    set of data that is required for them to be considered well formed. Several additional sub-types 
    of Node exist and may require additional data associated with them.

    """
    problems = []
    
    if doc.get("nodes") == None:
        problems.append("No 'nodes' block")
    else:
        if type(doc.get("nodes")) is not list:
            problems.append("Nodes block is not a list")
        else:
            for node in doc.get("nodes"):
                if "id" not in node:
                    problems.append("Node doesn't contain an 'id' key")
                else:
                    node_id = node.get("id")
                    if type(node_id) is not str:
                        problems.append("Node 'id' key is not a string")
                    try:
                        uuid.UUID(node_id, version=4)
                    except:
                        problems.append("'node_id' is not an instance of UUID4"+str(node_id))

                if "type" not in node:
                    problems.append("Node doesn't contain a 'type' key")
                else:
                    type_key = node.get("type")
                    if type(type_key) is not str:
                        problems.append("Node 'type' key is not a string")
                    if type_key not in ["atom", "scheme"]:
                        problems.append("Node 'type' not of supported SADFace node type")

                    if type(type_key) == "atom":
                        problems += check_node_type_atom(node)
                    elif type(type_key) == "scheme":
                        problems += check_node_type_scheme(node)
                        

                for block in node.get("metadata"):
                    obj = doc.get("metadata").get(block)
                    if type(obj) is not dict:
                        problems.append("Metadata contains a block that is not a dict/object:"+str(obj))
                    else:
                        if doc.get("metadata").get("core") is None:
                            problems.append("No 'core' block in metadata")

        for block in doc.get("nodes"):
            if type(block) is not dict:
                problems.append("Nodes contains a block that is not a dict/object:"+str(block))
            

    return problems
 

def check_resources_block(doc):
    """
    The resources block is a list of, possibly external, resources that the SADFace graph refers to.
    The block is required but may be an empty list.
    """
    problems = []
    
    if doc.get("resources") == None:
        problems.append("No 'resources' block")
    else:
        if type(doc.get("resources")) is not list:
            problems.append("Resources block is not a list")

        for block in doc.get("resources"):
            if type(block) is not dict:
                problems.append("Resources contains a block that is not a dict/object:"+str(block))

    return problems



def verify(incoming=None, as_string=False):
    """
    Verifies that the supplied SADFace document is well formed.

    If no input is supplied then this function will verify the current internal sadface document.
    Otherwise a document can be supplied in two forms, as a JSON encoded string or as a Python dict.
    In either case the function checks the input type and acts accordingly to normalise the input to
    a Python dict. This dict is then checked to ensure that:

        1. All necessary keys are present
        2. All supplied keys are permitted, i.e. within the boundaries permitted
            by the namespacing/metadata infrastructure
        3. No additional keys are present
        4. All values, where appropriate, are within defined parameters

    Returns: a pair (status, problems) such that:
        status is True if their are no problems and False otherwise
        problems is either a list of strings where each string describes a problem with the supplied input or a single string in which the members of the list have been joined (useful for convenient output to the user)
    """
    doc = {}
    problems = []

    if incoming is not None:
        if type(incoming) is str:
            doc = sadface.import_json(incoming)
        elif type(incoming) is dict:
            doc = incoming
        else:
            problems.append("Supplied document is neither a JSON encoded string nor a Python dict")
            return problems
    else:
        doc = sadface.sd


    problems += check_global_metadata_block(doc)
    problems += check_edges_block(doc)
    problems += check_nodes_block(doc)
    problems += check_resources_block(doc)
    

    if len(problems) > 0 and as_string == False:
        return True, problems
    elif len(problems) == 0 and as_string == False:
        return False, problems
    elif len(problems) > 0 and as_string == True:
        return True, ", ".join(problems)
    else:
        return False, ", ".join(problems)
    

