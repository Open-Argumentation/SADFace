import json

import sadface as sf


sf.config.init("etc/test.cfg")
sf.initialise()

sf.set_title("very important")
sf.add_notes("some nonsense about stuff...")
sf.append_notes("yet more notes n stuff")
sf.set_description("a cohesive description of this argument document")

con1 = "You should treasure every moment"
prem1 = ["if you are going to die then you should treasure every moment", "You are going to die"]
arg1 = sf.add_argument(con_text=con1, prem_text=prem1, con_id=None, prem_id=None)

t1 = sf.get_atom_id("You are going to die")

prem2 = ["Every person is going to die", "You are a person"]
arg2 = sf.add_support(con_text=None, prem_text=prem2, con_id=t1, prem_id=None)

prem3 = "YOLO"
arg3 = sf.add_conflict(arg_id=t1, conflict_text=prem3)
print(sf.prettyprint())


dot = sf.export_dot()#trad=False)    # Uncomment to use the brewer colourscheme
with open('out.dot', 'w') as file:
    file.write(dot)
    
