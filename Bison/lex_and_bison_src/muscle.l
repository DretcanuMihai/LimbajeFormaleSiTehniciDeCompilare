%{
#define MAX_ATOM_SIZE 251
#define MAX_FIP_SIZE 300
#define MAX_TS_SIZE 300

#include "muscle.tab.h"
#include <stdio.h>
#include <string.h>

int wasSuccessful=1;
int lastWasSeparator=1;

typedef struct {
	int value;
	int code;
}nodeFIP;

int sizeFIP=0;
nodeFIP FIP[MAX_FIP_SIZE];

typedef struct{
	char value[MAX_ATOM_SIZE];
}nodeTS;

int sizeTS=0;
nodeTS TS[MAX_TS_SIZE];

void setLastWasSeparator(int value){
	lastWasSeparator=value;
}

void printFIP(){
	printf("FIP:\n");
	int i;
	for(i=0;i<sizeFIP;i++){
		printf("%d\n", FIP[i].value);
		if(FIP[i].value<2){
			printf("%d\n", FIP[i].code);				
		}
	}
}
void printTS(){
	printf("TS:\n");
	int i;
	for(i=0;i<sizeTS;i++){
		printf("%d:%s\n", i,TS[i].value);
	}
}
void printError(){
	if(wasSuccessful){
		printf("lexical error at line %d\n",yylineno);
		wasSuccessful=0;
	}
}
int getTSCode(char* atom){
	int i;
	for(int i=0;i<sizeTS;i++){
		if(strcmp(atom,TS[i].value)==0){
			return i;
		}
	}
	strcpy(TS[sizeTS].value,atom);
	sizeTS++;
	return sizeTS-1;
}
void addToFIP(int value,char* atom, int isSeparator){
	if((!lastWasSeparator) && (!isSeparator)){
		printError();
	}
	if(value==0 && strlen(atom)>250){
		printError();
	}
	
	FIP[sizeFIP].value=value;
	if(value<2){
		int code = getTSCode(atom);
		FIP[sizeFIP].code=code;
	}
	sizeFIP++;
	
	lastWasSeparator=isSeparator;
}	
%}

%option noyywrap
%option yylineno

ID [a-zA-Z_][a-zA-Z_0-9]*([.][a-zA-Z_][a-zA-Z_0-9]*)?

BOOL_CONST "true"|"false"

BINARY_DIGIT [0-1]
OCTA_DIGIT {BINARY_DIGIT}|[2-7]
DECA_DIGIT {OCTA_DIGIT}|[8-9]
HEXA_DIGIT {DECA_DIGIT}|[a-fA-F]

HEXA_FLOAT_I {HEXA_DIGIT}+
HEXA_FLOAT_IV {HEXA_FLOAT_I}[.]
HEXA_FLOAT_IVF {HEXA_FLOAT_IV}{HEXA_DIGIT}+
HEXA_FLOAT_V [.]
HEXA_FLOAT_VF {HEXA_FLOAT_V}{HEXA_DIGIT}+
HEXA_FLOAT_CONST ("0x")({HEXA_FLOAT_I}|{HEXA_FLOAT_IV}|{HEXA_FLOAT_IVF}|{HEXA_FLOAT_VF})([pP][-+]?{DECA_DIGIT}+)

DECA_FLOAT_I {DECA_DIGIT}+
DECA_FLOAT_IV {DECA_FLOAT_I}[.]
DECA_FLOAT_IVF {DECA_FLOAT_IV}{DECA_DIGIT}+
DECA_FLOAT_V [.]
DECA_FLOAT_VF {DECA_FLOAT_V}{DECA_DIGIT}+
DECA_FLOAT_EXP [eE][-+]?{DECA_DIGIT}+
DECA_FLOAT_CONST (({DECA_FLOAT_IV}|{DECA_FLOAT_IVF}|{DECA_FLOAT_VF}){DECA_FLOAT_EXP}?)|({DECA_FLOAT_I}{DECA_FLOAT_EXP})

FLOAT_CONST ({DECA_FLOAT_CONST}|{HEXA_FLOAT_CONST})[fFlL]?

BINARY_INT_CONST ("0b"){BINARY_DIGIT}+
OCTA_INT_CONST ("0"){OCTA_DIGIT}*
DECA_INT_CONST [1-9]({DECA_DIGIT})*
HEXA_INT_CONST ("0x"){HEXA_DIGIT}+
INTEGER_CONST ({BINARY_INT_CONST}|{OCTA_INT_CONST}|{DECA_INT_CONST}|{HEXA_INT_CONST})([uU]|[uU][lL]|[uU][lL][lL]|[lL]|[lL][uU]|[lL][lL]|[lL][lL][uU])?

TEXT_CONST (["](\\n)["])|(["][:a-zA-Z ]+["])

CONST {BOOL_CONST}|{FLOAT_CONST}|{INTEGER_CONST}|{TEXT_CONST}

%%

"#include" {addToFIP(2,yytext,0); return INCLUDE;}
"iostream" {addToFIP(3,yytext,0);return IOSTREAM;}
"using" {addToFIP(4,yytext,0);return USING;}
"namespace" {addToFIP(5,yytext,0);return NAMESPACE;}
"std" {addToFIP(6,yytext,0);return STD;}
"int" {addToFIP(7,yytext,0);return INT;}
"main" {addToFIP(8,yytext,0);return MAIN;}
"return" {addToFIP(9,yytext,0);return RETURN;}
"while" {addToFIP(10,yytext,0);return WHILE;}
"struct" {addToFIP(11,yytext,0);return STRUCT;}
"bool" {addToFIP(12,yytext,0);return BOOL;}
"double" {addToFIP(13,yytext,0);return DOUBLE;}
"cout" {addToFIP(14,yytext,0);return COUT;}
"cin" {addToFIP(15,yytext,0);return CIN;}
"if" {addToFIP(16,yytext,0);return IF;}

"<<" {addToFIP(17,yytext,1);return LTLT;}
">>" {addToFIP(18,yytext,1);return GTGT;}
"!=" {addToFIP(19,yytext,1);return NE;}
"==" {addToFIP(20,yytext,1);return EQ;}
"&&" {addToFIP(21,yytext,1);return AND;}
"||" {addToFIP(22,yytext,1);return OR;}
"+" {addToFIP(23,yytext,1);return '+';}
"-" {addToFIP(24,yytext,1);return '-';}
"*" {addToFIP(25,yytext,1);return '*';}
"/" {addToFIP(26,yytext,1);return '/';}
"%" {addToFIP(27,yytext,1);return '%';}
"<" {addToFIP(28,yytext,1);return '<';}
">" {addToFIP(29,yytext,1);return '>';}
"=" {addToFIP(30,yytext,1);return '=';}
"!" {addToFIP(31,yytext,1);return '!';}

"(" {addToFIP(32,yytext,1);return '(';}
")" {addToFIP(33,yytext,1);return ')';}
"{" {addToFIP(34,yytext,1);return '{';}
"}" {addToFIP(35,yytext,1);return '}';}
";" {addToFIP(36,yytext,1);return ';';}

{CONST} {addToFIP(1,yytext,0);return CONST;}
{ID} {addToFIP(0,yytext,0);return ID;}

[ \t\n\r] {lastWasSeparator=1;}

. {printError(); return 0;}

%%

yyerror()
{
	if(wasSuccessful){
		printf("syntax error at line %d\n", yylineno);
		wasSuccessful=0;
	}
}
int main(int argc, char** argv) {

	yyparse();
	
	if(wasSuccessful){
		printFIP();
		printTS();
	}
	
	return 0;
}