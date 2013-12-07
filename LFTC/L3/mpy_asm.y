%{
    #include <stdio.h>
    #include "node.h"
	extern int  lineno;
	extern char *yytext; /* last token, defined in lex.l  */
	int yylex(void);
    void yyerror(const char *);
    #include <stack>
    #include <vector>

    extern std::stack<int> indentation;
    class Node;
    using namespace std;

    NProgram* progr;
    vector<NVar> var_decl;
%}

%union {  
	int intValue;
	char* id;
	Node *node;
    NProgram *program;
    NExpression *expr;
    NStatement *stmt;
}

%token <intValue> NUM_CT
%token <id> VAR

%token DEDENT INDENT INT INPUT OUTPUT IF ELSE COMMA COLON
%token DOT LPAREN RPAREN ASSIGN PLUS MINUS MUL DIV LT GT EQ GTE
%token LTE NEQ


%type <program> program multiple_stmt
%type <stmt> stmt
%type <expr> expr term atom

%start program

%%

program: multiple_stmt { progr = $1 }

multiple_stmt : stmt  { $$ = new NProgram(); $$->statements.push_back($<stmt>1); }
                | multiple_stmt stmt   { $1->statements.push_back($<stmt>2); }
                ;

stmt : INT VAR             { $$ = new NStatement();
                            var_decl.push_back(NVar(std::string($2))); }
       | VAR ASSIGN expr    { $$ = new NAssignment(NVar(std::string($1)), *$3); }
       | OUTPUT LPAREN VAR RPAREN  {$$ = new NOutput(NVar(std::string($3)));}
       | INPUT LPAREN VAR RPAREN     {$$ = new NInput(NVar(std::string($3)));}
       ;

expr : term
       | expr PLUS term     { $$ = new NBinaryOperator(*$1, 0, *$3); }
       | expr MINUS term    { $$ = new NBinaryOperator(*$1, 1, *$3); }
       ;
term : atom
       | term MUL atom    {$$ = new NBinaryOperator(*$1, 2, *$3); }
       | term DIV atom    {$$ = new NBinaryOperator(*$1, 3, *$3); }
       ;

atom : VAR              { $$ = new NVar(std::string($1)) }
       | NUM_CT         { $$ = new NInteger($1) }
       ;

%%

void yyerror(const char* a) {
	printf( "Syntax error on line #%d\n", lineno);
	printf( "Last token was \"%s\"\n", yytext);
	printf("Param: %s \n", a);
}


int main() {
    indentation.push(0);
    //printf("MY: yyparse returns %d %s \n", yyparse(), progr);
    yyparse();
    progr->var_list = var_decl;
    progr->codeGen();
}