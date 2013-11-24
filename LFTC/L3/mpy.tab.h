
/* A Bison parser, made by GNU Bison 2.4.1.  */

/* Skeleton interface for Bison's Yacc-like parsers in C
   
      Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     NUM_CT = 258,
     STR_CT = 259,
     VAR = 260,
     DEDENT = 261,
     INDENT = 262,
     FLOAT = 263,
     CHAR = 264,
     ARRAY = 265,
     INPUT = 266,
     OUTPUT = 267,
     IF = 268,
     ELIF = 269,
     ELSE = 270,
     WHILE = 271,
     RETURN = 272,
     DEF = 273,
     CONTINUE = 274,
     BREAK = 275,
     OR = 276,
     AND = 277,
     NOT = 278,
     NEWLINE = 279,
     COMMA = 280,
     COLON = 281,
     DOT = 282,
     LPAREN = 283,
     RPAREN = 284,
     ASSIGN = 285,
     PLUS = 286,
     MINUS = 287,
     MUL = 288,
     DIV = 289,
     MOD = 290,
     LT = 291,
     GT = 292,
     EQ = 293,
     GTE = 294,
     LTE = 295,
     NEQ = 296
   };
#endif



#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 1676 of yacc.c  */
#line 13 "mpy.y"
  
	double dblValue;
	char*  strValue;
	char* id;



/* Line 1676 of yacc.c  */
#line 101 "mpy.tab.h"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE yylval;


