import sadface as sf

"""
A minimal script to demonstrate loading and verifying a SADFace document.
"""

sfdoc = sf.load_from_file("minimal.json")
sf.set_doc(sfdoc)

result, problems = sf.validation.verify(sf.get_document())
if result:
    print(", ".join(problems))
else:
    print(sf.prettyprint())




