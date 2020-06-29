#!/usr/bin/python

from . import aml
from . import sadface
from . import config

import argparse
import cmd
import sys
import textwrap
import uuid

class REPL(cmd.Cmd):
    """
    The SADFace REPL. Type 'help' or 'help <command>' for assistance
    """

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "The SADFace REPL. Type 'help' or 'help <command>' for assistance"

    def do_arg(self, line):
        """
        Arguments are depicted in the following fashion e.g. premise1,premise2}conclusion
        premises are a comma separated list of strings where each string depicts a single
        premise. The conclusion is written at the end of the premise list using `}` to
        indicate a defeasible Modus Ponens rule. This uses the Simple Argument Description
        Notation (SADN).

        The line is split initially on the '}" to yield the premises (in the head)
        and the conclusion in the tail. The head is further split on the comma delimiters
        to retrieve each individual premise.
        """
        conid = None
        contxt = None
        if "}" in line:
            head,tail = line.split("}")
            if tail.startswith("id="):
                conid = tail.replace("id=", "")
            else:
                if (len(tail)>0):
                    contxt = tail.strip()
            premtext = []
            premid = []
            for element in head.split(","):
                t = element.strip()
                if t.startswith("id="):
                    premid.append(t.replace("id=", ""))
                else:
                    if (len(t) >0 ):
                        premtext.append(t)
            if ((conid is not None or contxt is not None) and (premtext or premid)):
                arg = sadface.add_argument(con_text=contxt, prem_text=premtext, con_id=conid, prem_id=premid)
                print(arg)
            else:
                print("USAGE: arg premise,premise,...}conclusion")
        else:
            print("USAGE: arg premise,premise,...}conclusion")

    def default(self, line):
        print("I do not understand that command. Type 'help' for a list of commands.")

    def do_add_resource(self, line):
        sadface.add_resource("hello world")
        print(sadface.prettyprint())

    def do_clear(self, line):
        sadface.sd = {}
        sadface.sd = sadface.initialise()

    def do_list_atoms(self, line):
        atoms = sadface.list_atoms()
        for a in atoms:
            print(a["id"]+" | "+a["text"])
    
    def do_print(self, line):
        print(sadface.sd)

    def do_prettyprint(self, line):
        print(sadface.prettyprint())

    def do_save(self, line):
        if('' != line):
            sadface.save(line)
        else:
            sadface.save()

    def do_save_to_dot(self, line):
        if('' != line):
            sadface.save(line, filetype="dot")
        else:
            sadface.save(filetype="dot")

    def do_quit(self, line):
        """
        Quit the SADRace REPL.
        """
        return True

    def emptyline(self):
        pass

    def help_clear(self):
        print("Creates a new, empty SADFace document")

    do_p = do_print
    do_q = do_quit
    do_s = do_save
    do_sd = do_save_to_dot
    do_pp = do_prettyprint


def main():
    parser = argparse.ArgumentParser(description="This is the SADFace Python tool")
    parser.add_argument("-c", "--config", help="Supply a config file for SADFace to use.")
    parser.add_argument("-i", "--interactive", help="Use the SADFace REPL", action="store_true")

    fileinput = parser.add_mutually_exclusive_group()
    fileinput.add_argument("-l", "--load", help="Load a Sadface document from a file")
    fileinput.add_argument("-r", "--raw", help="Load a raw JSON document string into SADFace")
    fileinput.add_argument("--aml", help="Load a legacy AML document from a file")

    parser.add_argument("-s", "--save", help="Save the loaded document to a SADFace formatted JSON file")
    
    export = parser.add_mutually_exclusive_group()
    export.add_argument("--printdoc", 
        help="Print the SADFace document to the screen", action="store_true")
    export.add_argument("--pretty", 
        help="Pretty print the SADFace document", action="store_true")
    export.add_argument("--exportdot", 
        help="Export the SADFace document to dot format", action="store_true")


    args = parser.parse_args()

    if args.config:
        config.set_config_location(args.config)

    if args.raw:
        sadface.sd = sadface.import_json(args.raw)
    elif args.load:
        sadface.sd = sadface.load_from_file(args.load)
    elif args.aml:
        aml.init(args.aml)
    else:
        sadface.sd = sadface.initialise()

    if args.save:
        sadface.save(args.save)

    if args.printdoc:
        print(sadface.print_doc())
    elif args.pretty:
        print(sadface.prettyprint())
    elif args.exportdot:
        print(sadface.export_dot())
    
    if args.interactive:
        REPL().cmdloop()
        
            
