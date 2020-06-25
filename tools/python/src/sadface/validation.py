#!/usr/bin/python

import uuid

import sadface


def check_edges_block(doc):
    """

    """
    problems = []

    if doc.get("edges") == None:
        problems.append("No 'edges' block")
    else:
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

def check_metadata_block(doc):
    """

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


def check_nodes_block(doc):
    """

    """
    problems = []
    
    if doc.get("nodes") == None:
        problems.append("No 'nodes' block")

    return problems
 

def check_resources_block(doc):
    """

    """
    problems = []
    
    if doc.get("resources") == None:
        problems.append("No 'resources' block")

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
            doc = import_json(incoming)
        elif type(incoming) is dict:
            doc = incoming
        else:
            problems.append("Supplied document is neither a JSON encoded string nor a Python dict")
            return problems
    else:
        doc = sadface.sd


    problems += check_metadata_block(doc)
    problems += check_edges_block(doc)
    problems += check_nodes_block(doc)
    problems += check_resources_block(doc)
    

    if len(problems) > 0 and as_string == False:
        return True, problems
    elif len(problems) == 0 and as_string == False:
        return None, problems
    elif len(problems) > 0 and as_string == True:
        return True, ", ".join(problems)
    else:
        return False, problems
    

