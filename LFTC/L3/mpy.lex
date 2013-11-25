%{
    #include <stdlib.h>
    #include <string.h>
	#include "mpy.tab.h"
    #include <math.h>
    int lineno = 0;
    #include <stack>
    std::stack<int> indentation;

    int current_indentation = 0;
    #define token(txt) printf("%d %s \n", lineno, #txt); return txt;
%}

%option noyywrap
%x indent

%%
\n                 { lineno++; token(NEWLINE) }
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

"float"               { token(FLOAT) }
"char"                { token(CHAR) }
"or"                  { token(OR) }
"and"                 { token(AND) }
"not"                 { token(NOT) }
"["[1-9][0-9]*"]"     { token(ARRAY) }
"input"               { token(INPUT) }
"print"               { token(OUTPUT) }
"if"                  { token(IF) }
"elif"                { token(ELIF) }
"else"                { token(ELSE) }
"while"               { token(WHILE) }
"return"              { token(RETURN) }
"def"                 { token(DEF) }
"continue"            { token(CONTINUE) }
"break"               { token(BREAK) }
[a-zA-Z][a-zA-Z0-9]*  { printf("%d %s: %s \n", lineno, "VAR", yytext);
                        yylval.id = (char*)malloc(yyleng);
                        strcpy(yylval.id, yytext);
                        return VAR;
                      }
\"[a-zA-Z0-9 ]*\"     { printf("%d %s: %s \n", lineno, "STR_CT", yytext);
                        yylval.strValue = (char*)malloc(yyleng);
                        strcpy(yylval.strValue, yytext);
                        return STR_CT;
                      }
(0|[1-9][0-9]*)"."[0-9]+  { printf("%d %s: %s \n", lineno, "NUM_CT", yytext);
                        yylval.dblValue = atof(yytext);
                        return NUM_CT;
                      }
"+"                   { token(PLUS) }
"-"                   { token(MINUS) }
"*"                   { token(MUL) }
"/"                   { token(DIV) }
"%"                   { token(MOD) }
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
^[ ]*           { printf(" Indent of %d current %d \n", yyleng, current_indentation);
                    if (current_indentation > yyleng) {
                        int prev = indentation.top();
                        indentation.pop();
                        prev = indentation.top();
                        if (prev != yyleng) {
                            BEGIN(indent);
                            int i = prev - yyleng;
                            printf("orig prev %d yyleng %d diff %d ", prev, yyleng, i);
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

                    printf(" Indent of %d current %d \n", yyleng, current_indentation);
                }
<indent>([ ]*)|\n   {
                    int prev = indentation.top();
                    indentation.pop();
                    if (prev != yyleng) {
                        int i = prev - yyleng;
                        printf("prev %d yyleng %d diff %d ", prev, yyleng, i);
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
