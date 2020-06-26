import sadface as sf

"""
A minimal script to create the bare minimum SADFace document. This includes each of an edges, nodes, resources, and metadata block. The resulting SADFace description is then run through a validation procedure before being pretty printed to the terminal.
"""

sf.initialise()
result, problems = sf.validation.verify(sf.get_document(), as_string=True)

if result:
    print(problems)
else:
    print(sf.prettyprint())

