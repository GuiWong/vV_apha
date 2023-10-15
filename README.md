This is a personnal project for learning low level programming.

The goal is to implement a programming language using python and assembly.

I'm taking inspiration from Porth (https://gitlab.com/tsoding/porth) ,

but vV is already different in implementation and in planning.



(Current version could be 0.0.1 , first version with a working compiler.)

	Now working on v 0.0.2, I/O update


Planned Updates:




	0.0.2:		I/O Update
	
		-buffered 32b unsigned int input		|	Done/unimplemented yet
		-buffered 32b unsigned int output		|	Done/unimplemeted yet
		-Basic Errors (exit code!=0)			|	TODO: define errors somewhere
		-Rewrite the transpiler to use nasm macros	|	In progress
		
		todo:
		
		-format for u_int I/O (hex, bin, decimal)
		- "char" I/O
		-" PackedChar" I/O
		- Rename labels, update some names



	0.0.3: 	The string Update
	
		-add a 2nd stack for strings
			-new stack pointer: r14 (string stack pointer)
		-8 new string or io related keywords
		
		-string LIFO:	byte 1 hold size (max 255 size string on stack)
				string follows at addr +1, +2 ...
				push / pop using size and string SP to align strings
				
				
				
	0.0.4:		Memory access, Variables
	
	
	
	
Current Implementation:

vV (pronounced in french "Double V", the name of the letter W . 
Could be called "double-u" or "double-v") is a stack based programming language.

For now, it only has:
	- basic operations ( + - mul div < > ! & ^ % )
	- if , else , end , do , while for flow control
	- output of number kinda works
	-all assembly is here for int and string input, just need to add the keywords
	
	
stack is in .bss for now, pointed to by r15

rsp is used as return stack








	
		
		-

