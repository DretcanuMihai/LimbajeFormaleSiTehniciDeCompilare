%{

%}

%locations
%token AND
%token BOOL
%token CIN
%token CONST
%token COUT
%token DOUBLE
%token EQ
%token GTGT
%token ID
%token IF
%token INCLUDE
%token INT
%token IOSTREAM
%token LTLT
%token MAIN
%token NAMESPACE
%token NE
%token OR
%token RETURN
%token STD
%token STRUCT
%token USING
%token WHILE

%%

program	:	INCLUDE	'<' IOSTREAM '>'
			USING NAMESPACE STD ';'
			lista_definire_tipuri
			INT MAIN '(' ')' '{'
				program_principal
				RETURN CONST ';'
			'}'
		;
		
lista_definire_tipuri	:	%empty 
						| 	definire_tip ';'
							lista_definire_tipuri
						;

definire_tip	: 	tip_definit '{' 
					lista_declarari_in_struct
					'}'
				;

tip_definit	:	STRUCT ID
			;
			
lista_declarari_in_struct	:	%empty
							|	declarare_in_struct ';' 
								lista_declarari_in_struct
							;
							
declarare_in_struct	:	tip_primitiv ID
					;
						
tip_primitiv	:	BOOL 
				| 	DOUBLE 
				| 	INT
				;

program_principal	: 	lista_declarari
						lista_instructiuni
					;
				
lista_declarari	:	%empty
				|	declarare ';'
					lista_declarari
				;

declarare	:	tip ID
			;

tip	:	tip_definit 
	| 	tip_primitiv
	;

lista_instructiuni	:	%empty
					|	instructiune ';' 
						lista_instructiuni
					;

instructiune	:	afisare 
				| 	atribuire 
				| 	citire 
				| 	conditionala_if 
				| 	ciclare_while
				;

afisare	:	COUT LTLT evaluabil_atomic
		;

atribuire	:	ID '=' evaluabil
			;

evaluabil	:	evaluabil_atomic 
			| 	operator_unar evaluabil_atomic 
			| 	evaluabil_atomic operator_binar evaluabil_atomic
			;

evaluabil_atomic	:	CONST 
					| 	ID
					;

operator_unar	:	'+' | '-' | '!'
				;

operator_binar	:	'+' | '-' | '*' | '/' | '%' | AND | OR | '<' | '>' | NE | EQ
				;
				
citire	:	CIN GTGT ID
		;
	
conditionala_if	:	IF '(' ID ')' '{' 
					lista_instructiuni 
					'}'
				;
ciclare_while	:	WHILE '(' ID ')' '{'
					lista_instructiuni 
					'}'
				;

%%
