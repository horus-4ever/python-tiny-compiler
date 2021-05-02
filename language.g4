grammar language;

entry_point:            (structure_declaration | function_declaration)* ;

structure_declaration:  'struct' IDENTIFIER '{' struct_member* '}' ;
struct_member:          attribute_declaration | function_declaration ;
attribute_declaration:  IDENTIFIER type_annotation ';' ;
type_annotation:        ':' kind ;
kind:                   ref_type | normal_type ;
ref_type:               '&' normal_type ;
normal_type:            IDENTIFIER ; 

function_declaration:   'func' IDENTIFIER '(' parameters? ')' type_annotation block ;
parameters:             parameter (',' parameter)* ;
parameter:              IDENTIFIER type_annotation ;
block:                  '{' statement* '}' ;

statement:              (expression | non_expression) ';' ;

expression:             '&'IDENTIFIER
                        | expression '*' expression
                        | expression '+' expression
                        | expression '-' expression
                        | structure_instantiation
                        | array
                        | function_call
                        | method_call
                        | classmethod_call
                        | factor ;
factor:                 NUMBER | IDENTIFIER | string | get_attribute ;
get_attribute:          IDENTIFIER '.' IDENTIFIER ('.' IDENTIFIER)* ;
function_call:          IDENTIFIER '(' arguments? ')' ;
method_call:            get_attribute '(' arguments? ')' ;
classmethod_call:       kind '::' IDENTIFIER '(' arguments? ')' ;
arguments:              expression (',' expression)* ;
structure_instantiation:IDENTIFIER '{' arguments? '}' ;
array:                  '[' arguments ']' ;

non_expression:         variable_declaration | assignement | set_attribute | return_statement ;
variable_declaration:   'let' IDENTIFIER type_annotation? '=' expression ;
assignement:            IDENTIFIER '=' expression ;
set_attribute:          get_attribute '=' expression ;
return_statement:       'return' expression ;

IDENTIFIER :    [A-Za-z] ([A-Za-z] | '_')* ;
NUMBER:         [0-9]+ ;
string:         '"'.*?'"' ;
COMMENTS:       '//'.*?[\n] -> skip ;
WS : [ \t\r\n]+ -> skip ;