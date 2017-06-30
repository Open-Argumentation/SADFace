#!/usr/bin/python

import argparse
import cmd
import codecs
import ConfigParser
import datetime
import json
import uuid

config = ConfigParser.ConfigParser()
config_location = "etc/defaults.cfg"
sd = {}

def add_edge(source, target):
    edge = new_edge(source, target)
    sd["edges"].append(edge)
    return edge

def add_resource(content):
    res = new_resource(content)
    sd["resources"].append(res)
    return res

def add_atom(text):
    atom = new_atom(text)
    sd["nodes"].append(atom)
    return atom

def add_scheme(name):
    scheme = new_scheme(name)
    sd["nodes"].append(scheme)
    return scheme

def add_source(atom_id, resource_id, text, offset, length):
    source = new_source(resource_id, text, offset, length)
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_id == node["id"]:
                node["sources"].append(source)
                return source

def add_atom_metadata(atom_id, key, value):
    for node in sd["nodes"]:
        if "atom" == node["type"]:
            if atom_id == node["id"]:
                node["metadata"][key] = value

def add_resource_metadata(resource_id, key, value):
    for res in sd["resources"]:
        if res["id"] == resource_id:
            res["metadata"][key] = value

def add_sadface_metadata(key, value):
    sd["metadata"][key] = value

def export_json():
    return json.dumps(sd)

def import_json(json_string):
    return json.loads(json_string)

def init():
    try:
        config.read(config_location)
    except:
        print "Could not read configs from ", config_location
    return new_sadface()

def new_edge(source, target):
    new_edge = {"id":new_uuid(), "source":source, "target":target}
    return new_edge

def new_sadface():
    new_doc = {"id":new_uuid(), "analyst_name":config.get("analyst", "name"), "analyst_email":config.get("analyst", "email"), "created":now(), "edited":now(), "metadata":{}, "resources":[], "nodes":[], "edges":[]}
    return new_doc

def new_resource(content):
    new_resource = {"id":new_uuid(), "content":content, "type":"text", "metadata":{}}
    return new_resource

def new_atom(text):
    new_atom = {"id":new_uuid(), "type":"atom", "canonical_text":text, "sources":[], "metadata":{}}
    return new_atom

def new_scheme(name):
    new_scheme = {"id":new_uuid(), "type":"scheme", "name":name}
    return new_scheme

def new_source(resource_id, text, offset, length):
    new_source = {"resource_id":resource_id, "text":text, "offset":offset, "length":length}
    return new_source

def new_uuid():
    return str(uuid.uuid4())

def now():
    return datetime.datetime.now().replace(microsecond=0).isoformat()

def prettyprint():
    return json.dumps(sd, indent=4, sort_keys=True)

def save():
    with open('data.json', 'w') as outfile:
        json.dump(sd, outfile, codecs.getwriter('utf-8')(outfile), indent=4, sort_keys=True, ensure_ascii=False)

def update():
    sd["edited"] = now()

def update_analyst(analyst):
    sd["analyst"] = analyst

def update_created(timestamp):
    sd["timestamp"] = timestamp

def update_id(id):
    sd["id"] = id

def update_edited(timestamp):
    sd["edited"] = timestamp


class REPL(cmd.Cmd):
    """
    The SADFace REPL. Type 'help' or 'help <command>' for assistance
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "The SADFace REPL. Type 'help' or 'help <command>' for assistance"
    
    def do_add_resource(self, args):
        add_resource("hello world")
        print prettyprint()

    def do_init(self, args):
        global sd
        sd = init()
        print sd
        
    def do_print(self, args):
        print prettyprint()

    def do_quit(self, args):
        return True

    def help_init(self):
        print "Creates a default SADFace document"

    do_q = do_quit

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is the SADFace Python tool")
    parser.add_argument("-c", "--config", help="Supply a config file for SADFace to use.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Use the SADFace REPL")
    parser.add_argument("-l", "--load", help="Load a JSON document into SADFace")
    args = parser.parse_args()

    if args.config:
        config_location = args.config

    if args.interactive:
        REPL().cmdloop()
    else:
        if args.load:
            sd = import_json(args.load)
        else:
            sd = init()
            add_sadface_metadata("hello","world")
            add_sadface_metadata("some","shit")
            add_resource("hello world")
            add_resource("goodbye cruel world")
            add_resource_metadata("test", "one", "two")

            a = add_atom("an argument atom")
            add_source(a["id"], "1234", "a source text", 150, 57)
            add_scheme("expert_opinion")
        
            add_edge("1", "2")
            add_edge("1", "3")

            print prettyprint()
            save()

