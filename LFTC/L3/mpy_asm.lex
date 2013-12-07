%{
    #include <stdlib.h>
    #include <string.h>
    #include <string>
    #include "node.h"
	#include "mpy_asm.tab.h"
    #include <math.h>
    int lineno = 0;
    #include <stack>
    std::stack<int> indentation;

    int current_indentation = 0;
    #define token(txt)  return txt;
%}

%option noyywrap
%x indent

%%
\n                 { lineno++; }
^[^ \n]+           { int last = yyleng - 1;
                     while ((last >= 0) && (yytext[last] != ' ')) {
                        unput(yytext[last]);
                        last-- ;
                     }
                     if (current_indentation != 0) {
                        current_indentation = 0;
                        token(DEDENT)
                     }
                     current_indentation = 0;
                  }

"int"                 { token(INT) }
"input"               { token(INPUT) }
"print"               { token(OUTPUT) }
"if"                  { token(IF) }
"else"                { token(ELSE) }
[a-zA-Z][a-zA-Z0-9]*  { yylval.id = (char*)malloc(yyleng);
                        strcpy(yylval.id, yytext);
                        return VAR;
                      }
0|[1-9][0-9]*         { yylval.intValue = atoi(yytext);
                        return NUM_CT;
                      }
"+"                   { token(PLUS) }
"-"                   { token(MINUS) }
"*"                   { token(MUL) }
"/"                   { token(DIV) }
"="                   { token(ASSIGN) }
","                   { token(COMMA) }
":"                   { token(COLON) }
"<"                   { token(LT) }
">"                   { token(GT) }
"=="                  { token(EQ) }
">="                  { token(GTE) }
"<="                  { token(LTE) }
"!="                  { token(NEQ) }
"("                   { token(LPAREN) }
")"                   { token(RPAREN); }
^[ ]*$                { } /* blank lines*/
^[ ]*           {                     if (current_indentation > yyleng) {
                        int prev = indentation.top();
                        indentation.pop();
                        prev = indentation.top();
                        if (prev != yyleng) {
                            BEGIN(indent);
                            int i = prev - yyleng;
                            while (i--) {
                                unput(' ');
                            }
                        }
                        if (indentation.empty()) {
                            printf("Incorrect indentation at line %d \n", yytext, lineno);
                        }
                        current_indentation = yyleng;
                        token(DEDENT)
                    }
                    else if (current_indentation < yyleng) {
                        indentation.push(yyleng);
                        current_indentation = yyleng;
                        token(INDENT)
                    }

                }
<indent>([ ]*)|\n   {
                    int prev = indentation.top();
                    indentation.pop();
                    if (prev != yyleng) {
                        int i = prev - yyleng;
                        while (i-- && i > 0) {
                            unput(' ');
                        }
                    }
                    else {
                        BEGIN(0);
                    }
                    if (indentation.empty()) {
                        printf("Incorrect indentation at line %d \n", yytext, lineno);
                    }
                    token(DEDENT)
                }
[ ]             { } /* ignore space */
.               { printf("Illegal char %s on line %d \n", yytext, lineno); return 0;}




%%
