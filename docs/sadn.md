# Simple Argument Description Notation (SADN) 

SADN is a simple, text oriented, notation for declaratively describing arguments in an incremental, line-oriented fashion. SADN is built upon the Simple Argument Description Format (SADFace) which provides a core ontology of argumentative concepts. 

## General Principles

- Identifiers are either SADFace UUIDs or transient local aliases.
- Values are double-quoted Strings.
- Statements are separated by ,
- One expression is allowed per line.

## Commands



## Examples

- **1, 2 > 3**- Statements 1 & 2 attack statement 3
- **1, 2 } 3**- Statements 1 & 2 support statement 3
- **1 <> 2**- 1 & 2 conflict with each other (interpret as bi-directional attack)

