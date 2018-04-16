# Simple Argument Description Notation (SADN) 

SADN is a simple, text oriented, notation for describing arguments

## Simple Argument Description Notation (SADN)

- **<\>** = conflicts with
- **\>** = attacks/opposes
- **<** = attacked/opposed by
- **}** = supports
- **{** = supported by
- Statements are identifiers, e.g. 1,2,3, UUIDS, or Double-quoted Strings
- Statements separated by ,
- One expression per line

## Examples

- **1, 2 > 3**- Statements 1 & 2 attack statement 3
- **1, 2 } 3**- Statements 1 & 2 support statement 3
- **1 <> 2**- 1 & 2 conflict with each other (interpret as bi-directional attack)

