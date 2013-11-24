%{
    #include <stdio.h>
	extern int  lineno;
	extern char *yytext; /* last token, defined in lex.l  */
	int yylex(void);
void yyerror(const char *);
    #include <stack>
    extern std::stack<int> indentation;


%}

%union {  
	double dblValue;
	char*  strValue;
	char* id;
}

%token <dblValue> NUM_CT
%token <strValue> STR_CT
%token <id> VAR

%token DEDENT
%token INDENT

%token FLOAT
%token CHAR
%token ARRAY

%token INPUT
%token OUTPUT

%token IF
%token ELIF
%token ELSE
%token WHILE
%token RETURN
%token DEF
%token CONTINUE
%token BREAK
%token OR
%token AND
%token NOT

%token NEWLINE
%token COMMA
%token COLON
%token DOT
%token LPAREN
%token RPAREN
%token ASSIGN
%token PLUS
%token MINUS
%token MUL
%token DIV
%token MOD
%token LT
%token GT
%token EQ
%token GTE
%token LTE
%token NEQ

%start program

%%

program : /*nada*/
         | program stmt
         | program NEWLINE
         ;

stmt : simple_stmt
       | compound_stmt
       ;
simple_stmt : small_stmt NEWLINE
              ;
small_stmt : expr_stmt
            | print_stmt
            | read_stmt
            | flow_stmt
            ;

expr_stmt : type VAR
            | type VAR ASSIGN expr
            | VAR ASSIGN expr
            ;
print_stmt : OUTPUT LPAREN atom RPAREN
             ;
read_stmt : INPUT LPAREN VAR RPAREN
            ;
flow_stmt : break_stmt | continue_stmt | return_stmt
            ;
break_stmt : BREAK
             ;
continue_stmt : CONTINUE
                ;
return_stmt : RETURN atom
              ;

compound_stmt : if_stmt
                | while_stmt
                | funcdef
                ;

funcdef : DEF type VAR LPAREN argslist RPAREN COLON suite
          ;
funccall : VAR LPAREN call_list RPAREN
           ;
argslist : type VAR
           | argslist COMMA type VAR
           ;
call_list : expr
            | call_list COMMA expr
            ;

if_stmt : IF test COLON suite elif else
          ;
elif :
        | ELIF test COLON suite
        | elif ELIF test COLON suite
        ;
else :
        | ELSE COLON suite
        ;

while_stmt : WHILE test COLON suite
             ;

suite : simple_stmt
        | NEWLINE INDENT multiple_stmt DEDENT
        ;

multiple_stmt : stmt
                | multiple_stmt stmt
                ;

test : and_test
       | test OR and_test
       ;
and_test : not_test
           | and_test AND not_test
           ;
not_test : comparison
           | NOT comparison
           ;
comparison : expr comp_op expr
             ;
comp_op : LT
          | GT
          | EQ
          | GTE
          | LTE
          | NEQ
          ;
expr : term
       | expr PLUS term
       | expr MINUS term
       ;
term : factor
       | term MUL factor
       | term DIV factor
       | term MOD factor
       ;
factor : atom
        | funccall
        | PLUS atom
        | PLUS funccall
        | MINUS atom
        | MINUS funccall
        ;

atom : VAR
       | NUM_CT
       | STR_CT
       ;

type : FLOAT
       | CHAR
       | FLOAT ARRAY
       | CHAR ARRAY
       ;

%%

void yyerror(const char* a) {
	printf( "Syntax error on line #%d\n", lineno);
	printf( "Last token was \"%s\"\n", yytext);
	printf("Param: %s \n", a);
}


int main() {
    indentation.push(0);
  printf("MY: yyparse returns %d \n", yyparse());
} 