# Simple Argument Description Notation (SADN) 

SADN is a simple, text oriented, notation for declaratively describing arguments in an incremental, line-oriented fashion. SADN is built upon the Simple Argument Description Format (SADFace) which provides a core ontology of argumentative concepts. 

## General Principles

- Identifiers are either SADFace UUIDs or transient local aliases.
- Values are double-quoted Strings.
- Statements are separated by ,
- One expression is allowed per line.

## Commands

Commands come in four basic forms:

1. Simple command, e.g. print, are a bare command without parenthesis or arguments. They perform one clearly defined role.
2. Complex defined list command - takes a comma separated list of arguments enclosed in parenthesis in which the exact number of operands is pre-defined.
3. Complex Undefined list command - takes a comma separated list of arguments enclosed in parenthesis  in which an undefined number of operands are allowed.
4. Complex Labelled command - in which the operands are labelled to provide more information about their status. This enables the specific nature of the operand to be clearly and unambiguously communicated.

Available commands:

- atom(id:$ID, text:$TEXT) – Add a new atom node. $CONTENT is an optional quoted string contain- ing the textual content of the atom. If the atom command is executed with an existing $ID and a new text $TEXT then this will cause the existing atom node’s text value to be updated with the new $TEXT string.
- scheme(id:$ID, name:$TEXT) – Add a new scheme node. $TEXT is an optional quoted string containing the name of the associated argumentation scheme. If no $TEXT is supplied then a generic “support” name will be used. If the scheme command is executed with an exist- ing $ID and a new name $TEXT then the existing scheme node will be updated with the new name.
- support(scheme:$ID, conclusion:$ID, premise:$ID, ...) – Create a new supportive relationship be- tween the existing nodes identified by the conclusion and premise IDs. The support command allows an arbitrary number of premise IDs to be supplied. If no scheme ID is supplied then a new generic “support” node is created .
- attack(source:$ID, target:$ID) – Create a new attack relationship between the supplied nodes iden- tified by the source and target $IDs. Attack is a uni-directional conflict from one argument that is directed towards another argument. A new conflict node of type attack is created as a result.
- disagree($ID, $ID, ...) – Create a new disagreement relationship between the nodes identified by the supplied $IDs. Disagree is a bi-directional conflict between two or more arguments A new conflict node of type disagreement is created as a result.
- argument(scheme:$TEXT, conclusion:$ID | text:$CONTENT, premise:$ID | text:$CONTENT, ...) – Builds a complete argument structure in a single command. If no name $TEXT is supplied then a generic ‘support’ label will be added to the scheme. The remainder of the arguments are a comma separated list of arbitrary length of either $IDs referring to pre-existing nodes or double-quoted $TEXT strings which cause new atoms to be created. The first ID supplied will be interpreted as the concluding node, all other IDs will be interpreted as premises.
- remove(id:$ID, ...) – Remove the element identified by $ID from the model. This also removes any dependent elements within the SADFace model such as edges if the removed element is either the source or target of the edge.The remove operation is idempotent and repeated use on the same $ID will make no further change to the model. If no $ID is supplied the remove has no effect on the model.
- metadata(id:$ID, namespace:$TEXT, $KEY:$TEXT) – Used to add a metadata entry to the identified namespace of the SADFace element identified by $ID. Elements that can support metadata blocks are the model’s global metadata block, individual nodes, and individual resources. If the $KEY already exists then the $TEXT updates itand if the $KEY doesn’t exist then that key is created.
- atoms - Lists the atom nodes in the current SADFace model.
- schemes - Lists the scheme nodes in the current SADFace model.
- conflicts - Lists the conflict nodes, in the current SADFace model which includes both attacks and disagreements.
- edges - Lists the atom nodes in the current SADFace model.
- export(type:$TYPE) – SADFace supports exporting the SADFace model into a range of other text- based forms, for example, Dot and Cytoscape. The export keyword converts the SADFace model into the nominated model and displays it in the REPL.
- save(type:$TYPE, name:$PATHNAME) – Saves the SADFace model to a file on disk. Save supports all of the textual formats valid in the export keyword but adds binary formts that can’t be usefully displayed in the REPL including jpg, png, and svg formats.
- load(name:$PATHNAME) – Loads the SADFace document from the supplied pathname.
- clear – Return the current situation to an empty default SADFace model.
- print – Display the SADFace model as a single compact string.
- prettyprint – Display the SADFace model in a pretty printed JSON form using tabs and newlines. help – Display a list of available commands.

### Notes:
1. Variables are depicted in uppertext and prefixed by the `$' sign.
2. Where there is choice within an operand list, e.g. either supply a or b then this is indicated using the vertical bar `|'.
3. Some arguments are mandatory and the argument is therefore expected and others are optional and the command will complete in the absence of the argument.
3. IDs have two forms, a UUID or a local ID. UUIDs are based on Python UUID4 and are suitable for public facing argument structures where nodes might be referenced in other contexts. Local IDs are generated monotonically during a SADN session, correspond 1:1 with UUIDs, and there is no expectation that a local ID will survive past the current session. All local IDs are generated afresh during a SADN session when a document is loaded in, or when a node is created.
4. If a command consumes an ID then either a UUID or a local ID can be supplied.
5. If a commmand expects an ID and no ID is supplied then a new node will be created with a freshly generated local ID and UUID.

## Efficent Notation

- @ -> atom()
- $ -> scheme()
- ^ -> support()
- % -> disagree()
- \> -> attacks
- < -> attacked by
- & -> argument

## Examples

- **1, 2 > 3**- Statements 1 & 2 attack statement 3
- **1, 2 } 3**- Statements 1 & 2 support statement 3
- **1 <> 2**- 1 & 2 conflict with each other (interpret as bi-directional attack)

