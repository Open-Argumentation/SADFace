#!/usr/bin/python

import argparse
import cmd
import codecs
import ConfigParser
import datetime
import json
import sys
import uuid

config = ConfigParser.ConfigParser()
config_location = "etc/defaults.cfg"
sd = {}

def add_argument(conclusion, premises):
    """
    Syntactic sugar to create an argument structure from a set of texts.
    Given a conclusion text & a list of premise texts, create an intermediate,
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
    c = add_atom(conclusion)
    s = add_scheme("support")
    try:
        add_edge(s["id"], c["id"])
    except Exception as ex:
        print ex
        raise Exception("Could not create new argument")

    p_list = []
    for premise in premises:
        atom = add_atom(premise)
        p_list.append(atom)
        try:
            add_edge(atom["id"], s["id"])
        except Exception as ex:
            print ex
            raise Exception("Could not create new argument")

    arg = {"conclusion":c, "scheme":s, "premises":p_list}
    return arg

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
    atom = new_atom(text)
    sd["nodes"].append(atom)
    return atom

def add_atom_metadata(atom_id, key, value):
    """
    Add metadata, a key:value pair to the atom dict identified
    by the supplied atom ID.
    """
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_id == node["id"]:
                node["metadata"][key] = value

def add_resource(content):
    """
    Create a new resource dict using the supplied content string
    then add to the resourses list of the sadface doc

    Returns: the new resource dict
    """
    res = new_resource(content)
    sd["resources"].append(res)
    return res

def add_resource_metadata(resource_id, key, value):
    """
    Add metadata, a key:value pair to the resource dict identified
    by the supplied atom ID.    
    """
    for res in sd["resources"]:
        if res["id"] == resource_id:
            res["metadata"][key] = value

def add_sadface_metadata(key, value):
    """
    Add metadata, a key:value pair to the base sadface doc
    """
    sd["metadata"][key] = value

def add_scheme(name):
    """
    Add a new scheme node dict to the sadface document. The scheme type
    is identified by the supplied name

    Returns: The new scheme dict
    """
    scheme = new_scheme(name)
    sd["nodes"].append(scheme)
    return scheme

def add_source(atom_id, resource_id, text, offset, length):
    """
    Add a new source dict to the atom identified by the supplied
    atom ID. The new source refers to the an existing resource that
    is identified by the supplied resource ID. The source identifies
    text string in the resource dict that it references as well as
    the offset & length of the text from the beginning of the resource

    Returns: The new source dict
    """
    source = new_source(resource_id, text, offset, length)
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_id == node["id"]:
                node["sources"].append(source)
                return source

def delete_atom(atom_id):
    """
    Remove the atom from the sadface document identified by the
    supplied atom ID
    """
    atom = get_atom(atom_id)
    sd["nodes"].remove(atom)

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
    atom, resource = get_source(atom_id, resource_id)
    atom["sources"].remove(resource)

def delete_resource(resource_id):
    """
    Remove the resource from the sadface document identified by the
    supplied resource ID

    """
    resource = get_resource(resource_id)
    sd["resources"].remove(resource)

def delete_scheme(scheme_id):
    """
    Remove the schemee from the sadface document identified by the
    supplied scheme ID

    """
    scheme = get_scheme(scheme_id)
    sd["nodes"].remove(scheme)

def export_json():
    """
    Dump the current sadface document to a JSON string

    Returns: String-encoded JSON
    """
    return json.dumps(sd)

def get_atom(atom_id):
    """
    Retrieve the atom dict identified by the supplied atom ID

    Returns: An atom dict
    """
    for node in sd["nodes"]:
        if atom_id == node["id"]:
            return node

def get_edge(edge_id):
    """
    Retrieve the edge dict identified by the supplied edge ID

    Returns: An edge dict
    """
    for edge in sd["edges"]:
        if edge_id == edge["id"]:
            return edge

def get_node(node_id):
    """
    Given a node's ID but no indication of node type, return the node if 
    it exists or else indicate that it doesn't to the caller.

    Returns: A node dict or None
    """
    for node in sd["nodes"]:
        if node_id == node["id"]:
            return node

def get_resource(resource_id):
    """
    Retrieve the resource dict identified by the supplied resource ID

    Returns: An resource dict
    """
    for resource in sd["resources"]:
        if resource_id == resource["id"]:
            return resource

def get_scheme(scheme_id):
    """
    Retrieve the scheme dict identified by the supplied scheme ID

    Returns: An scheme dict
    """
    for node in sd["nodes"]:
        if scheme_id == node["id"]:
            return node

def get_source(atom_id, resource_id):
    """
    Retrieve the source dict identified by the supplied source ID

    Returns: An source dict
    """
    atom = get_atom(atom_id)
    for source in atom["sources"]:
        if resource_id == source["resource_id"]:
            return atom, source

def import_json(json_string):
    """
    Take a string-encoded JSON document and loads it into a Python dict

    Returns: the loaded dict
    """
    return json.loads(json_string)

def init():
    """
    Reads the config file from the supplied location then uses the data
    contained therein to personalise a new SADFace document

    Returns: A Python dict representing the new SADFace document
    """
    try:
        config.read(config_location)
    except:
        print "Could not read configs from ", config_location
    return new_sadface()

def new_atom(text):
    """
    Creates a new SADFace atom node (Python dict) using the supplied text

    Returns: A Python dict representing the new SADFace atom
    """
    new_atom = {"id":new_uuid(), "type":"atom", "text":text, "sources":[], "metadata":{}}
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
    new_doc = {"id":new_uuid(), "analyst_name":config.get("analyst", "name"), "analyst_email":config.get("analyst", "email"), "created":now(), "edited":now(), "metadata":{}, "resources":[], "nodes":[], "edges":[]}
    return new_doc

def new_resource(content):
    """
    Given the supplied content (Python String), create a new resource dict

    Returns: A Python dict representing the new SADFace resource
    """
    new_resource = {"id":new_uuid(), "content":content, "type":"text", "metadata":{}}
    return new_resource

def new_scheme(name):
    """
    Create a new SADFace scheme (Python dict) using the supplied scheme name. The scheme
    name should refer to an existing scheme from a known schemeset

    Returns: A Python dict representing the new SADFace scheme
    """
    new_scheme = {"id":new_uuid(), "type":"scheme", "name":name}
    return new_scheme

def new_source(resource_id, text, offset, length):
    """
    Create a new SADFace source (Python dict) using the supplied resource ID (a source always
    refers to an existing resource) and identifying a section of text in the resource as well
    as an offset & segment length for locating the text in the original resource.

    Returns: A Python dict representing the new SADFace source
    """
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
    Print nicely formatted output of the passed in string or
    otherwise the SADFace document encoded as a String

    Returns: A String
    """
    string = sd
    if(doc is not None):
        string = doc
    return json.dumps(string, indent=4, sort_keys=True)

def save(filename=None):
    """
    Write the prettyprinted SADFace document to a JSON file on disk
    """
    if filename is None:
        f = config.get("file","name")
    else:
        f = filename
    with open(f, 'w') as outfile:
        json.dump(sd, outfile, codecs.getwriter('utf-8')(outfile), indent=4, sort_keys=True, ensure_ascii=False)

def update():
    """
    Updates the last edited timestamp for the SADFace doc to now
    """
    sd["edited"] = now()

def update_analyst(analyst):
    """
    Updates the name of the argument analyst in the SADFace doc to the supplied name
    """
    sd["analyst"] = analyst

def update_atom_text(atom_id, new_text):
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
        raise Exception("Could not update the text value for atom: "+atom_id)

def update_created(timestamp):
    """
    Updates the creation timestamp for the SADFace document to the supplied timestamp.
    This can be useful when moving analysed argument data between formats whilst
    maintaining original metadata.
    """
    sd["timestamp"] = timestamp

def update_id(id):
    """
    Update the SADFace document ID to match the supplied ID. This can be useful when 
    moving analysed argument data between formats whilst maintaining original metadata.
    """
    sd["id"] = id

def update_edited(timestamp):
    """
    Update the last edited timestamp for the SADFace doc to match the supplied
    timestamp. This can be useful when moving analysed argument data between formats 
    whilst maintaining original metadata.
    """
    sd["edited"] = timestamp

def update_scheme(scheme_id, scheme_name):
    """
    Given an ID for an existing scheme node, update the name associated with it and return the scheme node.
    
    Returns: Updated scheme dict
    """
    scheme = get_scheme(scheme_id)
    if(scheme is not None):
        scheme["name"] = scheme_name
        return scheme
    else:
        raise Exception("Could not update the name of scheme: "+scheme_id)

class REPL(cmd.Cmd):
    """
    The SADFace REPL. Type 'help' or 'help <command>' for assistance
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "The SADFace REPL. Type 'help' or 'help <command>' for assistance"
        REPL.do_init(self, None)

    def do_arg(self, line):
        """
        Arguments are depicted in a Prolog style, e.g. conclusion:=premise1,premise2

        The line is split on the ':=" to get the conclusion then it is split on the
        comma delimters to retrieve each premise.
        """
        head,tail = line.split(':=')
        conc = head
        prems = []
        for element in tail.split(','):
            prems.append(element)
        arg = add_argument(conc, prems)
        print arg

    def default(self, line):
        print "I do not understand that command. Type 'help' for a list of commands."

    def do_add_resource(self, line):
        add_resource("hello world")
        print prettyprint()

    def do_init(self, line):
        global sd
        sd = init()
        print sd
    
    def do_print(self, line):
        print sd

    def do_prettyprint(self, line):
        print prettyprint()

    def do_save(self, line):
        if('' != line):
            save(line)
        else:
            save()

    def do_quit(self, line):
        """
        Quit the SADRace REPL.
        """
        return True

    def emptyline(self):
        pass

    def help_init(self):
        print "Creates a default SADFace document"

    do_p = do_print
    do_q = do_quit
    do_s = do_save
    do_pp = do_prettyprint


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is the SADFace Python tool")
    parser.add_argument("-c", "--config", help="Supply a config file for SADFace to use.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Use the SADFace REPL")
    parser.add_argument("-l", "--load", help="Load a JSON document into SADFace")
    args = parser.parse_args()

    if args.config:
        config_location = args.config

    if args.load:
        sd = import_json(args.load)
    else:
        if args.interactive:
            REPL().cmdloop()
        else:
            parser.print_help()
            sys.exit(0)

