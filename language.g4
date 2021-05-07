grammar language;

entry_point:            (structure_declaration | function_declaration)* ;

structure_declaration:  'struct' IDENTIFIER '{' (function_declaration | attribute_declaration)* '}' ;
attribute_declaration:  IDENTIFIER type_annotation ';' ;
type_annotation:        ':' kind ;
kind:                   ref_type | normal_type ;
ref_type:               '&' normal_type ;
normal_type:            IDENTIFIER ; 

function_declaration:   'func' IDENTIFIER '(' parameters? ')' type_annotation block ;
parameters:             parameter (',' parameter)* ;
parameter:              IDENTIFIER type_annotation ;
block:                  '{' statement* '}' ;

statement:              (expression ';') | (non_expression ';'?) ;

expression:             make_ref
                        | deref
                        | expression '*' expression
                        | expression '+' expression
                        | expression '-' expression
                        | structure_instantiation
                        | array
                        | function_call
                        | method_call
                        | classmethod_call
                        | factor ;
make_ref:               '&' IDENTIFIER ;
deref:                  '*' IDENTIFIER ;
factor:                 NUMBER | IDENTIFIER | STRING | true | false | get_attribute ;
get_attribute:          IDENTIFIER '.' IDENTIFIER ('.' IDENTIFIER)* ;
function_call:          IDENTIFIER '(' arguments? ')' ;
method_call:            get_attribute '(' arguments? ')' ;
classmethod_call:       normal_type '::' IDENTIFIER '(' arguments? ')' ;
arguments:              expression (',' expression)* ;
field_arguments:        IDENTIFIER ':' expression (',' IDENTIFIER ':' expression)* ;
structure_instantiation:IDENTIFIER '{' field_arguments? '}' ;
array:                  '[' arguments ']' ;

non_expression:         variable_declaration | block | assignement | deref_assignement | condition | set_attribute | return_statement ;
variable_declaration:   'let' IDENTIFIER type_annotation? '=' expression ;
assignement:            IDENTIFIER '=' expression ;
deref_assignement:      '*' IDENTIFIER '=' expression ;
condition:              'if' expression block else_block? ;
else_block:             ('else' condition) | ('else' block) ;
set_attribute:          get_attribute '=' expression ;
return_statement:       'return' expression ;

IDENTIFIER :    [A-Za-z] ([A-Za-z] | '_')* ;
NUMBER:         [0-9]+ ;
true:           'true' ;
false:          'false' ;
STRING:         '"'.*?'"' ;
COMMENTS:       '//'.*?[\n] -> skip ;
WS : [ \t\r\n]+ -> skip ;