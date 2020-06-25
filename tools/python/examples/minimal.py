import sadface as sf

"""
A minimal script to create the bare minimum SADFace document. This includes an edges, nodes, resources, and metadata block. First a default configuration file (default.cfg) is generated and stored in a folder /etc relative to the current working directory. Core metadata for the new SADFace document is then completed according to that default configuration file. The resulting SADFace description is then run through a validation procedure before being pretty printed to the terminal.
"""

sf.init()
result, problems = sf.validation.verify(sf.get_document(), as_string=True)

if result:
    print(problems)
else:
    print(sf.prettyprint())

