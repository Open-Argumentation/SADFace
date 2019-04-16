#!/usr/bin/python

import requests as rq
import json

import config

url = ""
ds = ""

def init():
    """
    Set up a datastore if one doesn't already exist
    """
    db_name = config.current.get("db", "name")
    db_type = config.current.get("db", "type")
    db_ip   = config.current.get("db", "ip")
    db_port = config.current.get("db", "port")
    db_protocol = config.current.get("db", "protocol")
    
    if ("couchdb" == db_type):
        global url, ds
        url = db_protocol + "://" + db_ip + ":" + db_port + "/" + db_name
        ds = url + "/"
        r = rq.put(url)
    else:
        print("No supported datastore provided")
        exit(1)


def create(doc, docid):
    """
    Add the supplied document, identified by docid into the datastore
    """
    r = rq.put(ds + docid, data=doc)


def retrieve(docid, raw=False):
    """
    Get the JSON document, identified by docid, from the datastore
    """
    r = rq.get(ds + docid)
    doc = json.loads(r.text)
    if raw:
        return doc
    else:
        doc.pop("_id")
        doc.pop("_rev")
        return doc

def update(doc, docid):
    """
    Update the document, identified by docid, in the datastore
    """
    old = retrieve(docid, raw=True)
    rev = old.get("_rev")
    new = json.loads(doc)
    new["_id"] = docid
    new["_rev"] = rev
    r = rq.put(ds + docid, data=json.dumps(new))

def delete(docid):
    """
    Delete the document, identified by docid, from the datastore
    """
    doc = retrieve(docid, raw=True)
    rev = doc.get("_rev")
    r = rq.delete(ds + docid + "?rev="+rev)

   
