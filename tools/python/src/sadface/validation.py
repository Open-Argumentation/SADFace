#!/usr/bin/python

import uuid

import sadface

def verify(incoming=None):
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

    Returns: a list of strings. Each string describes a problem with the supplied input
    """


