#!/usr/bin/python

import argparse
import cmd
import codecs
import datetime
import json
import sys
import textwrap
import uuid

from . import config
from . import validation

sd = {}

def add_argument(con_text=None, prem_text=None, con_id=None, prem_id=None):
    """
    Syntactic sugar to create an argument structure from a set of texts.
    Given a conclusion text & a list of premise texts. Creates an intermediate,
    default "inference" scheme.

    This makes it easier to build a SADFace document without manually creating
    and organising individual nodes.

    Returns an argument dict, e.g.

    {
        "conclusion": atom,
        "scheme": atom,
        "premises": [atom ID(s)]
    }

    e.g.

    {
        "conclusion": {
            "id": "329aee40-b34d-4eaa-9e25-9ef3098b4cfa",
            "type": "atom",
            "text": "You should treasure every moment",
            "sources": [],
            "metadata": {
                "core": {}
            }
        },
        "scheme": {
            "id": "f4ae4161-f18b-49f7-9213-d81c2084cedd",
            "type": "scheme",
            "name": "inference",
            "metadata": {
                "core": {}
            }
        },
        "premises": ["6b4cbe35-4e11-4126-ab25-97c9ac651647", "4cebed0d-3869-4a20-958c-9e164a019573"]
    }

    Returns: a dict
    """
    if((con_text is not None or con_id is not None) and (prem_text is not None or prem_id is not None)):

        if con_text is not None:
            c = add_atom(con_text)
        else:
            c = get_atom(con_id)

        s = add_scheme("inference")
        try:
            add_edge(s["id"], c["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        p_list = []
        if(prem_text is not None):
            for text in prem_text:
                atom = add_atom(text)
                p_list.append(atom["id"])
                try:
                    add_edge(atom["id"], s["id"])
                except Exception as ex:
                    print(ex)
                    raise Exception("Could not create new argument")
        if(prem_id is not None):
            for atom_id in prem_id:
                atom = get_atom(atom_id)
                p_list.append(atom["id"])
                try:
                    add_edge(atom["id"], s["id"])
                except Exception as ex:
                    print(ex)
                    raise Exception("Could not create new argument")

        arg = {"conclusion":c, "scheme":s, "premises":p_list}
        return arg
    return None

def add_conflict(arg_text=None, arg_id=None, conflict_text=None, conflict_id=None):
    """
    Conflicts play an important role in arguments. We depict conflict
    through the use of schemes that represent the conflict relationship. This
    function will instantiate a conflict scheme between two nodes (either
    pre-existing & identifed by node IDs or created from supplied texts, or a
    mixture of the two).

    Returns a conflict dict, e.g.

    {
        "argument": atom,
        "scheme": atom,
        "conflict": atom
    }
    (where the scheme just happens to depict a conflict)

    
    For example:

    {
        "argument": {
            "id": "6399c86d-3c07-4223-ae91-bb989b6dc21e",
            "type": "atom",
            "text": "You are going to die",
            "sources": [],
            "metadata": {
                "core": {}
            }
        },
        "scheme": {
            "id": "7b4b7d23-7386-470e-ad48-56a655812218",
            "type": "scheme",
            "name": "conflict",
            "metadata": {
                "core": {}
            }
        },
        "conflict": {
            "id": "777a21cf-6c60-44cc-9b3f-bfe1f2e342d6",
            "type": "atom",
            "text": "YOLO",
            "sources": [],
            "metadata": {
                "core": {}
            }
        }
    }



    Returns: a dict
    """
    if((arg_text is not None or arg_id is not None) and (conflict_text is not None or conflict_id is not None)):
        
        if arg_text is not None:
            a = add_atom(arg_text)
        else:
            a = get_atom(arg_id)

        s = add_scheme("conflict")

        try:
            add_edge(s["id"], a["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        if conflict_text is not None:
            c = add_atom(conflict_text)
        else:
            c = get_atom(conflict_id)

        try:
            add_edge(c["id"], s["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        arg = {"argument":a, "scheme":s, "conflict":c}
        return arg
    return None

def add_support(con_text=None, prem_text=None, con_id=None, prem_id=None):
    """
    Syntactic sugar to create an argument structure from a set of texts.
    Given a conclusion text & a list of premise texts. Creates an intermediate,
    default "support" scheme.

    This makes it easier to build a SADFace document without manually creating
    and organising individual nodes.

    Returns an argument dict, e.g.

    {
        "conclusion": atom,
        "scheme": atom,
        "premises": [atom(s)]
    }

    Returns: a dict
    """
    if((con_text is not None or con_id is not None) and (prem_text is not None or prem_id is not None)):

        if con_text is not None:
            c = add_atom(con_text)
        else:
            c = get_atom(con_id)

        s = add_scheme("support")
        try:
            add_edge(s["id"], c["id"])
        except Exception as ex:
            print(ex)
            raise Exception("Could not create new argument")

        p_list = []
        if(prem_text is not None):
            for text in prem_text:
                atom = add_atom(text)
                p_list.append(atom["id"])
                try:
                    add_edge(atom["id"], s["id"])
                except Exception as ex:
                    print(ex)
                    raise Exception("Could not create new argument")
        if(prem_id is not None):
            for atom_id in prem_id:
                atom = get_atom(atom_id)
                p_list.append(atom["id"])
                try:
                    add_edge(atom["id"], s["id"])
                except Exception as ex:
                    print(ex)
                    raise Exception("Could not create new argument")

        arg = {"conclusion":c, "scheme":s, "premises":p_list}
        return arg
    return None


def add_edge(source_id, target_id):
    """
    Given a source atom ID & a target atom ID, create an 
    edge linking the two and add it to the sadface doc,
    "sd" & return the dict representing the edge. If
    either of source or target IDs is invalid then an
    exception is raised.

    Returns: a dict 
    """
    if ((get_node(source_id) is not None) and (get_node(target_id) is not None)):
        edge = new_edge(source_id, target_id)
        sd["edges"].append(edge)
        return edge
    raise Exception("Could not create new edge between: "+source_id+" & "+target_id)

def add_atom(text):
    """
    Create a new argument atom using the supplied text

    Returns: the new atom dict
    """
    atomid = contains_atom(text)
    atom = None

    if atomid is not None:
        atom = get_atom(atomid)

    else:
        atom = new_atom(text)
        sd["nodes"].append(atom)
    
    return atom

def add_atom_metadata(atom_id, namespace, key=None, value=None):
    """
    Add metadata, a key:value pair, to the atom dict identified
    by the supplied atom ID and metadata namespace.

    Note that "core" should be reserved for sadface default metadata only

    Additional namespaces can be any string but should normally follow
    the reversed domain name approach to provide some level of uniqueness
    and avoid unnecessary clashes
    """
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_id == node["id"]:
                if node["metadata"].get(namespace) is None:
                    node["metadata"][namespace] = {}
                    node["metadata"][namespace][key] = value
                else:
                    node["metadata"][namespace][key] = value
                    
def add_global_metadata(namespace, key, value):
    """
    Add metadata, a key:value pair to the base sadface doc
    """
    if sd["metadata"].get(namespace) is None:
        sd["metadata"][namespace] = {}
        sd["metadata"][namespace][key] = value
    else:
        sd["metadata"][namespace][key] = value

def add_notes(text):
    """
    Add a metadata entry for the document that contains notes. Notes
    are miscellaneous, unstructured free text.
    """
    sd["metadata"]["core"]["notes"] = text


def add_resource(content):
    """
    Create a new resource dict using the supplied content string
    then add to the resourses list of the sadface doc

    Returns: the new resource dict
    """
    res = new_resource(content)
    sd["resources"].append(res)
    return res

def add_resource_metadata(resource_id, namespace, key=None, value=None):
    """
    Add metadata, a key:value pair to the resource dict identified
    by the supplied atom ID.    
    """
    for res in sd["resources"]:
        if res["id"] == resource_id:
            if res["metadata"].get(namespace) is None:
                res["metadata"][namespace] = {}
                res["metadata"][namespace][key] = value
            else:
                res["metadata"][namespace][key] = value

def add_scheme(name):
    """
    Add a new scheme node dict to the sadface document. The scheme type
    is identified by the supplied name

    Returns: The new scheme dict
    """
    scheme = new_scheme(name)
    sd["nodes"].append(scheme)
    return scheme

def add_scheme_metadata(scheme_id, namespace, key=None, value=None):
    """
    Add metadata, a key:value pair, to the scheme dict identified
    by the supplied scheme ID and metadata namespace.

    Note that "core" should be reserved for sadface default metadata only

    Additional namespaces can be any string but should normally follow
    the reversed domain name approach to provide some level of uniqueness
    and avoid unnecessary clashes
    """
    for node in sd["nodes"]:
        if "scheme" == node["type"]:
            if scheme_id == node["id"]:
                if node["metadata"].get(namespace) is None:
                    node["metadata"][namespace] = {}
                    node["metadata"][namespace][key] = value
                else:
                    node["metadata"][namespace][key] = value


def add_source(atom_id, resource_id, text, offset, length):
    """
    Add a new source dict to the atom identified by the supplied
    atom ID. The new source refers to the an existing resource that
    is identified by the supplied resource ID. The source identifies
    text string in the resource dict that it references as well as
    the offset & length of the text from the beginning of the resource

    Returns: The new source dict
    """
    source = new_source(resource_id, text, offset)
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_id == node["id"]:
                node["sources"].append(source)
                return source

def append_notes(text):
    """
    Append new text to an existing notes entry
    """
    if sd.get("metadata").get("core").get("notes") != None:
        sd["metadata"]["core"]["notes"] += text
    else:
        add_notes(text)


def clear_notes():
    """
    Remove any existing notes
    """
    sd.get("metadata").get("core").pop("notes")


def contains_atom(atom_text):
    """
    Searches the sadface document for an existing atom containing
    the supplied text. If found, returns the id of that atom,
    otherwise None
    """
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_text == node["text"]:
                return node["id"]
    return None

def delete_atom(atom_id):
    """
    Remove the atom from the sadface document identified by the
    supplied atom ID
    """
    atom = get_atom(atom_id)
    sd["nodes"].remove(atom)

    conns = get_connections(atom_id)
    for c in conns:
        delete_edge(c["id"])

def delete_edge(edge_id):
    """
    Remove the edge from the sadface document identified by the
    supplied edge ID

    """
    edge = get_edge(edge_id)
    sd["edges"].remove(edge)

def delete_source(atom_id, resource_id):
    """
    Remove a source from the atom identified by the
    supplied atom ID & resource ID respectively

    """
    source = get_source(atom_id, resource_id)
    if source is not None:
        atom = get_atom(atom_id)
        atom["sources"].remove(source)

def delete_resource(resource_id):
    """
    Remove the resource from the sadface document identified by the
    supplied resource ID

    """
    resource = get_resource(resource_id)
    sd["resources"].remove(resource)

def delete_scheme(scheme_id):
    """
    Remove the scheme from the sadface document identified by the
    supplied scheme ID

    """
    scheme = get_scheme(scheme_id)
    sd["nodes"].remove(scheme)

    conns = get_connections(scheme_id)
    for c in conns:
        delete_edge(c["id"])

def export_cytoscape():
    """
    Cytoscape.js is a useful graph visualisation library for Javascript. However
    it uses some slightly different keynames and includes description of visual
    elements, useful to Cytoscape's visualisation, but having no place in SADFace.

    Both nodes & edges in a Cytoscape graph are collated together into a single
    eleents object so we need to do that to the SADFace nodea & edges. Furthemore,
    each node and edge object must contain a data object. After that conversion is
    a relatively straightforward mapping:

    EDGES
        id -> id
        source_id -> source
        target_id -> target

        e.g. 
        {
            "data": {
                "source": "a1",
                "id": "a1s1",
                "target": "s1"
            }
        }

    NODES - ATOMS    
        id -> id
        type -> type
        text -> content
        + "classes":"atom-label"
        + "typeshape":"roundrectangle"

        e.g.
        {
            "classes": "atom-label",
            "data": {
                "content": "Every person is going to die",
                "type": "atom",
                "id": "a1",
                "typeshape": "roundrectangle"
            }
        }


    NODES - SCHEMES
        id -> id
        type -> type
        name -> content
        + "classes":"scheme-label"
        + "typeshape":"diamond"
        
        e.g.
        {
            "classes": "scheme-label",
            "data": {
                "content": "Default\nSupport",
                "type": "scheme",
                "id": "s1",
                "typeshape": "diamond"
            }
        }

    """
    cy = {}
    cy['elements'] = {}
    cy['elements']['nodes'] = []
    cy['elements']['edges'] = []

    for edge in sd['edges']:
        e = {}
        e['data'] = {}
        e['data']['id'] = edge['id']
        e['data']['source'] = edge['source_id']
        e['data']['target'] = edge['target_id']

        cy['elements']['edges'].append(e)

    for node in sd['nodes']:
        n = {}
        n['data'] = {}
        n['data']['id'] = node['id']
        n['data']['type'] = node['type']
        if n['data']['type'] == "atom":
            n['classes'] = "atom-label"
            n['data']['typeshape'] = "roundrectangle"
            n['data']['content'] = node['text']

        else:
            n['classes'] = "scheme-label"
            n['data']['typeshape'] = "diamond"
            n['data']['content'] = node['name']

        cy['elements']['nodes'].append(n)

    return  json.dumps(cy)

def export_dot(trad=True):
    """
    Exports a subset of SADFace to the DOT graph description language

    Returns: String-encoded DOT document
    """
    if trad:
        colour_scheme = "X11"
        support_colour = "darkolivegreen3"
        conflict_colour = "firebrick2"
        default_colour = "cornsilk4"
    else:
        colour_scheme = "ylgnbu3"
        support_colour = "1"
        conflict_colour = "3"
        default_colour = "2"

    max_length = 25
    edge_str = " -> "
    dot = "digraph SADFace {"
    dot += "node [style=\"filled\"]"
    for node in sd["nodes"]:
        if "text" in node:
            txt = node["text"]
            if len(txt) > max_length:
                txt = "\\n".join(textwrap.wrap(txt, max_length))
            line = '"{}"'.format(node['id']) + " [label=\"" + txt + "\"]" + " [shape=box, style=rounded];\n"
            dot += line
        elif "name" in node:
            if "support" == node.get("name"):
                line = '"{}"'.format(node['id']) + " [label=\"" + node["name"]\
                + "\"]"\
                + " ["\
                + "colorscheme="+colour_scheme+", fillcolor="+support_colour\
                + ", shape=diamond];\n"
            elif "conflict" == node.get("name"):
                line = '"{}"'.format(node['id']) + " [label=\"" + node["name"]\
                + "\"]"\
                + " ["\
                + "colorscheme="+colour_scheme+", fillcolor="+conflict_colour\
                + ", shape=diamond];\n"

            else:
                line = '"{}"'.format(node['id']) + " [label=\"" + node["name"]\
                + "\"]"\
                + " ["\
                + "colorscheme="+colour_scheme+", fillcolor="+default_colour\
                + ", shape=diamond];\n"

            dot += line

    for edge in sd["edges"]:
        source = get_node(edge["source_id"])
        target = get_node(edge["target_id"])
        
        if("atom" == source["type"]):
            dot += '"{}"'.format(source["id"])
        elif "scheme" == source["type"]:
            dot += '"{}"'.format(source["id"])
        
        dot += edge_str

        if("atom" == target["type"]):
            dot += '"{}"'.format(target["id"])
        elif "scheme" == target["type"]:
            dot += '"{}"'.format(target["id"])
        
        dot += ";\n"

    dot += "}"
    
    return dot

def export_json():
    """
    Dump the current sadface document to a JSON string

    Returns: String-encoded JSON
    """
    return json.dumps(sd)

def get_analyst():
    """
    Retrieve the name of the argument analyst in the SADFace doc
    """
    return sd["metadata"]["core"]["analyst_name"]

def get_atom(atom_id):
    """
    Retrieve the atom dict identified by the supplied atom ID

    Returns: An atom dict
    """
    for node in sd["nodes"]:
        if atom_id == node["id"]:
            return node

def get_atom_id(text):
    """
    Retrieve the first atom whose text equals the supplied text

    Returns: The atom's ID or None 
    """
    for node in sd["nodes"]:
        if text == node.get("text"):
            return node["id"]

def get_atom_metadata(atom_id, namespace=None, key=None):
    """
    Retrieve an atom's metadata. Results depend upon the specificity of the request
    which must include atom_id.

    If atom_id only is provided then all metadata assocaited with the atom is returned
    If atom_id + namespace is provided then only the specified namespace is returned
    If atom_id + namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict
    """
    atom = get_atom(atom_id)
    if atom is not None:
        if namespace is None:
            return atom.get("metadata")
        else:
            if key is None:
                return atom.get("metadata").get(namespace)
            else:
                return atom.get("metadata").get(namespace).get(key)


def get_atom_text(atom_id):
    """
    Retrieve the atom dict identified by the supplied atom ID

    Returns: An atom dict
    """
    for node in sd["nodes"]:
        if atom_id == node["id"]:
            return node["text"]

def get_claim():
    """
    Retrieve the claim metadata entry from the document
    """
    return sd["metadata"].get("core").get("claim")

def get_connections(node_id):
    """
    Given a node id, retrieve a list containing all edges that connnect it
    to other nodes
    """
    conn =  []
    for edge in sd["edges"]:
        if node_id == edge["source_id"] or node_id == edge["target_id"]:
            conn.append(edge)
    return conn

def get_created():
    """
    Retrieve the claim metadata entry from the document
    """
    return sd["metadata"].get("core").get("created")

def get_document():
    """
    Retrieve the current SADFace document
    """
    return sd

def get_document_id(doc = None):
    """
    Retrieve the SADFace document's ID
    """
    if doc is None:
        return sd["metadata"].get("core").get("id")
    else:
        return doc["metadata"].get("core").get("id")

def get_description():
    """
    Retrieve the description metadata entry from the document
    """
    return sd["metadata"].get("core").get("description")

def get_edited():
    """
    Retrieve the last edited timestamp from the sadface document
    """
    return sd["metadata"].get("core").get("edited")

def get_edge(edge_id):
    """
    Retrieve the edge dict identified by the supplied edge ID

    Returns: An edge dict
    """
    for edge in sd["edges"]:
        if edge_id == edge["id"]:
            return edge

def get_global_metadata(namespace=None, key=None):
    """
    Retrieve the document's metadata. Results depend upon the specificity of the request
    which must include atom_id.

    If neither namespace nor key are provided then all metadata associated with the document is returned
    If a namespace is provided then only the specified namespace is returned
    If a namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict
    """
    if namespace is None:
        return sd.get("metadata")
    else:
        if key is None:
            return sd.get("metadata").get(namespace)
        else:
            return sd.get("metadata").get(namespace).get(key)



def get_node(node_id):
    """
    Given a node's ID but no indication of node type, return the node if 
    it exists or else indicate that it doesn't to the caller.

    Returns: A node dict or None
    """
    for node in sd["nodes"]:
        if node_id == node["id"]:
            return node

def get_notes():
    """
    Retrieve the notes metadata entry from the document
    """
    return sd["metadata"].get("core").get("notes")

def get_resource(resource_id):
    """
    Retrieve the resource dict identified by the supplied resource ID

    Returns: An resource dict
    """
    for resource in sd["resources"]:
        if resource_id == resource["id"]:
            return resource

def get_resource_metadata(resource_id, namespace=None, key=None):
    """
    Retrieve a resource's metadata. Results depend upon the specificity of the request
    which must include a resource_id.

    If resource_id only is provided then all metadata assocaited with the resource is returned
    If reource_id + namespace is provided then only the specified namespace is returned
    If resource_id + namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict
    """
    resource = get_resource(resource_id)
    if resource is not None:
        if namespace is None:
            return resource.get("metadata")
        else:
            if key is None:
                return resource.get("metadata").get(namespace)
            else:
                return resource.get("metadata").get(namespace).get(key)

def get_scheme(scheme_id):
    """
    Retrieve the scheme dict identified by the supplied scheme ID

    Returns: An scheme dict
    """
    for node in sd["nodes"]:
        if scheme_id == node["id"]:
            return node

def get_scheme_metadata(scheme_id, namespace=None, key=None):
    """
    Retrieve a scheme's metadata. Results depend upon the specificity of the request
    which must include a valid scheme_id.

    If scheme_id only is provided then all metadata assocaited with the scheme is returned
    If scheme_id + namespace is provided then only the specified namespace is returned
    If scheme_id + namespace + a key is provided then the value associated with that key is returned
    Else nothing is returned

    Returns: A metadata dict or None
    """
    scheme = get_scheme(scheme_id)
    if scheme is not None:
        if namespace is None:
            return scheme.get("metadata")
        else:
            if key is None:
                return scheme.get("metadata").get(namespace)
            else:
                return scheme.get("metadata").get(namespace).get(key)

def get_source(atom_id, resource_id):
    """
    Retrieve the source dict identified by the supplied source ID

    Returns: An source dict
    """
    atom = get_atom(atom_id)
    if atom is not None:
        if len(atom["sources"]) > 0:
            for source in atom["sources"]:
                if resource_id == source["resource_id"]:
                    return source
            
def get_title():
    """
    Retrieve the title metadata entry from the document
    """
    return sd["metadata"].get("core").get("title")

def get_version():
    """
    Return a string indicating the version of the loaded SADFace document
    If no version parameter then version is less than <0.1
    Versioning introduced in v0.2 with introduction of version key to
        {"metadata":{ "core": { "version": "0.1"} }, ...}
    """
    version = sd.get("metadata").get("core").get("version")
    if None == version:
        print("no explicit version so 0.1")
        version = "0.1"

    return version


def import_json(json_string):
    """
    Take a string-encoded JSON document and loads it into a Python dict

    Returns: the loaded dict
    """
    return json.loads(json_string)

def initialise():
    """
    Reads the config file from the supplied location then uses the data
    contained therein to personalise a new SADFace document

    Returns: A Python dict representing the new SADFace document
    """
    global sd
    sd = new_sadface()
    return sd#new_sadface()

def list_atoms():
    """
    Return a list of atoms and their associated ID contained in the current 
    document, using the following format

    [ { 'id':'id-value', 'text':'text-value' } ]

    """
    atoms = []
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            tmp = {}
            tmp["id"] = node["id"]
            tmp["text"] = node["text"]
            atoms.append(tmp)
    return atoms

def list_arguments():
    """
    Use to retrieve a list of arguments in the current document. Minimally
    we expect that each argument contains at least one sceheme node, so, by
    extension, a list of scheme nodes is also a list of arguments

    Returns: A list of scheme IDs
    """
    schemes = []
    for node in sd["nodes"]:
        if "scheme" == node["type"]:
            schemes.append(node.get("id"))
    return schemes

def list_resources():
    """
    Returns a comma separated list of resource IDs
    """
    return [ res["id"] for res in sd["resources"] ]

def list_schemes():
    """
    Use to retrieve a list of scheme nodes from the current document.

    Returns: A list of scheme IDs
    """
    schemes = []
    for node in sd["nodes"]:
        if "scheme" == node["type"]:
            schemes.append(node.get("id"))
    return schemes


def load_from_file(filename):
    """
    Load the sadface document stored in the file identifed by the supplied
    filename.
    """
    with open(filename) as sadface_file:
        return json.load(sadface_file)


def new_atom(text):
    """
    Creates a new SADFace atom node (Python dict) using the supplied text

    Returns: A Python dict representing the new SADFace atom
    """
    new_atom = {"id":new_uuid(), "type":"atom", "text":text, "sources":[], "metadata":{"core": {}}}
    return new_atom

def new_edge(source_id, target_id):
    """
    Creates & returns a new edge dict using the supplied source & 
    target IDs

    Returns: A Python dict representing the new edge
    """
    new_edge = {"id":new_uuid(), "source_id":source_id, "target_id":target_id}
    return new_edge

def new_sadface():
    """
    Creates & returns a new SADFace document

    Returns: A Python dict representing the new SADFace document
    """
    if config.location is None:
        new_doc = {"metadata":{ "core":{"version":"0.5", "id":new_uuid(), "analyst_name":"A User", "analyst_email":"user@email.address", "created":now(), "edited":now()}}, "resources":[], "nodes":[], "edges":[]}

    else:
        new_doc = {"metadata":{ "core":{"version":"0.5", "id":new_uuid(), "analyst_name":config.current.get("analyst", "name"), "analyst_email":config.current.get("analyst", "email"), "created":now(), "edited":now()}}, "resources":[], "nodes":[], "edges":[]}
    return new_doc

def new_resource(content):
    """
    Given the supplied content (Python String), create a new resource dict

    The arguments that SADFace describes are either constructed directly in a tool that writes
    them to this format, or else are sourced from elsewhere, e.g. an argumentative text or
    webpage, or else perhaps another medium, such as audio or video. Currently SADFace supports
    textual resources which are stored in the content key. Optionally a 
        "url":"some web location"
    pair can be added to the metadata to indicate a specific web location. Alternatively:
        "doi":"digital object identifier" - resolvable by dx.doi.org
        "magnet-link":"a torrent file"
        "isbn":"for books"
    Metadata may also store additional bibliographic or referencing/citation information
    as defined in bibtex formats.

    Returns: A Python dict representing the new SADFace resource
    """
    new_resource = {"id":new_uuid(), "content":content, "type":"text", "metadata":{ "core": {}}}
    return new_resource

def new_scheme(name):
    """
    Create a new SADFace scheme (Python dict) using the supplied scheme name. The scheme
    name should refer to an existing scheme from a known schemeset

    Returns: A Python dict representing the new SADFace scheme
    """
    new_scheme = {"id":new_uuid(), "type":"scheme", "name":name, "metadata":{ "core": {}}}
    return new_scheme

def new_source(resource_id, text, offset):
    """
    Create a new SADFace source (Python dict) using the supplied resource ID (a source always
    refers to an existing resource object) and identifying a section of text in the resource 
    as well as an offset for locating the text in the original resource.

    Text segment length is calculated from the length of the supplied text.

    As the resource object is enhanced to account for newer "types" of resource, so the
    source object must be enhanced to keep track and enable sources to index sub-parts of
    resources.

    Returns: A Python dict representing the new SADFace source
    """
    length = len(text)
    new_source = {"resource_id":resource_id, "text":text, "offset":offset, "length":length}
    return new_source

def new_uuid():
    """
    Utility method to generate a new universally unique ID. Used througout to uniquely
    identify various items such as atoms, schemes, resources, & edges

    Returns: A string
    """
    return str(uuid.uuid4())

def now():
    """
    Utility method to produce timestamps in ISO format without the microsecond
    portion, e.g. 2017-07-05T17:21:11

    Returns: A String
    """
    return datetime.datetime.now().replace(microsecond=0).isoformat()

def prettyprint(doc=None):
    """
    Retrieve a nicely formatted string encoded version of the SADFace document

    Returns: A String
    """
    string = sd
    if(doc is not None):
        string = doc
    return json.dumps(string, indent=4, sort_keys=True)

def print_doc(doc=None):
    """
    Retrieve a string encoded version of the SADFace document

    Returns: A String
    """
    string = sd
    if(doc is not None):
        string = doc
    return json.dumps(string,sort_keys=True)

def reset():
    """
    Return SADFace to it's initial state

    Basically delete, remove, or nullify any settings that have been applied.
    """
    global sd
    sd = {}
    config.reset()

def save(filename=None, filetype="json"):
    """
    Write the prettyprinted SADFace document to a JSON file on disk
    """
    f = filename
    d = None
    pathname = None

    if filename is None:       
        if config.current is not None:
            f = config.current.get("file","name")
            d = config.current.get("file","dir")
            outname = f+d
        else:
            f = "out"
            d = ""
            pathname = f
    else:
        pathname = f


    if ("dot" == filetype):
        suffix = '.dot'
        if not pathname.endswith(suffix):
            pathname += suffix

        with codecs.open(pathname, 'w', 'utf-8') as outfile:
            outfile.write(export_dot())

    elif("cytoscape" == filetype):
        suffix = '.json'
        if not pathname.endswith(suffix):
            pathname += suffix
        
        with codecs.open(pathname, 'w', 'utf-8') as outfile:
            outfile.write(prettyprint(json.loads(export_cytoscape())))
    else:
        suffix = '.json'
        if not pathname.endswith(suffix):
            pathname += suffix
        
        with open(pathname, 'w') as outfile:
            json.dump(sd, outfile, indent=4, sort_keys=True, ensure_ascii=False)

def set_analyst(analyst):
    """
    sets the name of the argument analyst in the SADFace doc to the supplied name
    """
    sd["metadata"]["core"]["analyst_name"] = analyst
    
def set_atom_text(atom_id, new_text):
    """
    An atoms text key:value pair is the canonical representation of a portion of text 
    that exists in an argument. This should be updatable so that the overall document 
    makes sense. Links to original source texts are maintained via the source list 
    which indexes original text portions of linked resources.

    Returns: The updated atom dict
    """
    atom = get_atom(atom_id)
    if(atom is not None):
        atom["text"] = new_text
        return atom
    else:
        raise Exception("Could not set the text value for atom: "+atom_id)

def set_title(text):
    """
    Set a metadata entry for the document that contains a title. This is a
    useful but non-essential addendum to the base sadface document when
    building systems that make use of sadface.
    """
    sd["metadata"]["core"]["title"] = text

def set_claim(atom_id):
    """
    Enables a given atom to be nominated as the claim for the argument captured
    by this sadface document. A useful way to explicitly set the atom that should
    be considered to be the main claim.
    """
    atom = get_atom(atom_id)
    if(atom is not None): 
        sd["metadata"]["core"]["claim"] = atom_id
    else:
        raise Exception("Can't make atom ("+atom_id+") a claim because it doesn't exist")

def set_created(timestamp):
    """
    Sets the creation timestamp for the SADFace document to the supplied timestamp.
    This can be useful when moving analysed argument data between formats whilst
    maintaining original metadata.
    """
    sd["metadata"]["core"]["created"] = timestamp

def set_description(text):
    """
    Set a metadata entry for the document that contains a description.
    """
    sd["metadata"]["core"]["description"] = text

def set_edited(timestamp):
    """
    Set the last edited timestamp for the SADFace doc to match the supplied
    timestamp. This can be useful when moving analysed argument data between formats 
    whilst maintaining original metadata.
    """
    sd["metadata"]["core"]["edited"] = timestamp

def set_document_id(id):
    """
    Set the SADFace document ID to match the supplied ID. This can be useful when 
    moving analysed argument data between formats whilst maintaining original metadata.
    """
    sd["metadata"]["core"]["id"] = id

def set_scheme_name(scheme_id, scheme_name):
    """
    Given an ID for an existing scheme node, set the name associated with it and return the scheme node.
    
    Returns: Updated scheme dict
    """
    scheme = get_scheme(scheme_id)
    if(scheme is not None):
        scheme["name"] = scheme_name
        return scheme
    else:
        raise Exception("Could not set the name of scheme: "+scheme_id)

def update():
    """
    Updates the last edited timestamp for the SADFace doc to now
    """
    sd["metadata"]["core"]["edited"] = now()

