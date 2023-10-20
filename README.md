This is a personnal project for learning low level programming.

The goal is to implement a programming language using python and assembly.

I'm taking inspiration from Porth (https://gitlab.com/tsoding/porth) ,

but vV is already different in implementation and in planning.



	Update 0.0.4: 
			Global and Local Variables, reworked functions
			


Planned Updates:




	0.0.?: 	The string Update
	
		-add a 2nd stack for strings
			-new stack pointer: r14 (string stack pointer)
		-8 new string or io related keywords
		
		-string LIFO:	byte 1 hold size (max 255 size string on stack)
				string follows at addr +1, +2 ...
				push / pop using size and string SP to align strings
				
				
				
	0.0.?:		Memory access, Variables
	
	
	
	
Current Implementation:

vV (pronounced in french "Double V", the name of the letter W . 
Could be called "double-u" or "double-v") is a stack based programming language.

For now, it only has:
	- basic operations ( + - mul div < > ! & ^ % )
	- if , else , end , do , while , break for flow control
	- numeric and ascii input/output
	- basic Error Managment

	
	
stack is in .bss for now, pointed to by r15

rsp is used as return stack






	
		
		-

