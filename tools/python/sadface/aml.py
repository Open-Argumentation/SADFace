import xml.etree.ElementTree as et
from . import sadface

def init(infile):
    sadface.sd = sadface.initialise()
    tree = et.parse(infile)
    root = tree.getroot()
    process_root(root)

def process_root(root):
    c = root.getchildren()
    for child in c:
        if child.tag == "TEXT":
            process_text(child)
            pass
        elif child.tag == "SCHEMESET":
            pass
        elif child.tag == "EDATA":
            pass
        elif child.tag == "AU":
            process_au(child)
        else:
            print("XML malformed")

def process_au(node):
    ch = node.getchildren()
    for c in ch:
        if c.tag == "PROP":
            pass
        elif c.tag == "REFUTATION":
            process_refutation(c, node)
        elif c.tag == "CA":
            process_ca(c, node)
        elif c.tag == "LA":
            process_la(c, node)
        else:
            print("XML malformed")

def process_ca(node, parent):
    """
    The DTD allows only a single premise supporting a given conclusion
    within a single AU node.
    """
    conc = get_node_text(parent)[1]
    prem = []

    ch = node.getchildren()
    for c in ch:
        if c.tag == "AU":
            prem.append(get_node_text(c)[1])
            process_au(c)

    sadface.add_support(con_text=conc, prem_text=prem)

def process_la(node, parent):
    conc = get_node_text(parent)[1]
    prem = []

    ch = node.getchildren()
    for c in ch:
        if c.tag == "AU":
            prem.append(get_node_text(c)[1])
            process_au(c)

    sadface.add_support(con_text=conc, prem_text=prem)

def process_refutation(node, parent):
    """
    The DTD allows only a single refutation relationship between a
    pair of AU nodes.
    """
    conc = get_node_text(parent)[1]
    prem = []

    ch = node.getchildren()
    for c in ch:
        if c.tag == "AU":
            prem.append(get_node_text(c)[1])
            process_au(c)

    sadface.add_conflict(arg_text=conc, conflict_text=prem[0])

def get_node_text(node):
    for child in node:
        if child.tag == "PROP":
            pid = child.attrib['identifier']
            for elem in child.iter(tag="PROPTEXT"):
                return (pid, elem.text)

def process_text(node):
    sadface.add_resource(node.text)

