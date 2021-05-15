grammar language;

entry_point:            ((builtin_function ';') | builtin_structure | structure_declaration | function_declaration | trait_declaration)* ;

structure_declaration:  'struct' IDENTIFIER implements? '{' (function_declaration | attribute_declaration)* '}' ;
attribute_declaration:  IDENTIFIER type_annotation ';' ;
type_annotation:        ':' kind ;
kind:                   ref_type | normal_type ;
ref_type:               '&' normal_type ;
normal_type:            IDENTIFIER ;

trait_declaration:      'trait' IDENTIFIER '{' (function_prototype ';')* '}' ;
function_prototype:     'func' IDENTIFIER '(' parameters? ')' type_annotation ;

builtin_function:       'builtin' function_prototype ;
builtin_structure:      'builtin' 'struct' IDENTIFIER '[' NUMBER ']' implements? '{' (builtin_function ';')* '}' ;
implements:             'deriving' normal_type ('+' normal_type)* ;

generics:               '<' generic (',' generic)* '>' ;
generic:                IDENTIFIER implements? ;

function_declaration:   'func' IDENTIFIER generics? '(' parameters? ')' type_annotation block ;
parameters:             parameter (',' parameter)* ;
parameter:              IDENTIFIER type_annotation ;
block:                  '{' statement* '}' ;

statement:              (expression ';') | (non_expression ';'?) ;

expression:             lvalue_ref
                        | rvalue_ref
                        | deref
                        | expression EQ expression
                        | expression NEQ expression
                        | expression ADD expression
                        | expression SUB expression
                        | expression MUL expression
                        | structure_instantiation
                        | function_call
                        | expression '.' IDENTIFIER LPAREN arguments? ')'
                        | expression '.' IDENTIFIER
                        | classmethod_call
                        | factor ;
reference:              lvalue_ref | rvalue_ref ;
rvalue_ref:             '&' expression ;
lvalue_ref:             '&' IDENTIFIER ;
deref:                  '*' expression ;
factor:                 NUMBER | IDENTIFIER | STRING | true | false | ('(' expression ')') ;
get_attribute:          expression '.' IDENTIFIER ;
function_call:          IDENTIFIER '(' arguments? ')' ;
method_call:            expression '.' IDENTIFIER '(' arguments? ')' ;
classmethod_call:       normal_type '::' IDENTIFIER '(' arguments? ')' ;
arguments:              expression (',' expression)* ;
field_arguments:        IDENTIFIER ':' expression (',' IDENTIFIER ':' expression)* ;
structure_instantiation:IDENTIFIER '{' field_arguments? '}' ;
array:                  '[' arguments ']' ;
binary_expression:      binary_and | binary_or | binary_eq | binary_neq | binary_mul | binary_add | binary_sub ;
binary_and:             expression 'or' binary_and ;
binary_or:              expression 'and' binary_or ;
binary_eq:              expression '==' binary_eq ;
binary_neq:             expression '!=' binary_neq ;
binary_mul:             expression '*' binary_mul ;
binary_add:             expression '+' binary_add ;
binary_sub:             expression '-' binary_sub ;

non_expression:         variable_declaration
                        | block
                        | assignement
                        | deref_assignement
                        | condition
                        | set_attribute
                        | return_statement
                        | while_statement;
variable_declaration:   'let' IDENTIFIER type_annotation? '=' expression ;
assignement:            IDENTIFIER '=' expression ;
deref_assignement:      '*' IDENTIFIER '=' expression ;
condition:              'if' expression block else_block? ;
else_block:             ('else' condition) | ('else' block) ;
set_attribute:          get_attribute '=' expression ;
return_statement:       'return' expression ;
while_statement:        'while' expression block ;

IDENTIFIER :    [A-Za-z] ([A-Za-z] | '_')* ;
NUMBER:         [0-9]+ ;
true:           'true' ;
false:          'false' ;
STRING:         '"'.*?'"' ;
EQ:             '==' ;
NEQ:            '!=' ;
ADD:            '+' ;
SUB:            '-' ;
MUL:            '*' ;
LPAREN:         '(' ;
COMMENTS:       '//'.*?[\n] -> skip ;
WS : [ \t\r\n]+ -> skip ;