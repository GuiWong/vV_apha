


1.0: basic Operations


	+	-	*	/		%

	<	>	!	|	&	^	
	
	
2.0: Boolean checks	
	
	<? >? =?					

3.0: flow control


	if 	el	,
	
	do	while
	
	break

4.0: Stack manipulation

 	(push) ' '	 dup   	swp		drp		
 			2dup
 			  |
 			9dup
 
 
5.0 I/O Update (0.0.2.x)
 
 
 DONE	get	[read input, send int data tostack]
 
 	Auto FORMAT (0x,0b, 0d)
 	
 DONE	(out) .  [top of stack to output as str repr]



	Format: 	-d:Deciamal		-c: char
			-x/-h: hex		-w: packed char
 			-b: bin
 	
 	
 Syntax??????
 
 
 		get	\
 	 /	(dget)	|
 	 |	(sget)	|	Done
 Implicit|	(xget)	|
 	  \	(bget)	/
 		
 		getc	\	Done
 		getw	/
 
 
   28	 	out	\		out_	\
 		dout	|		dout_	|
 		sout	|done		sout_	|
 		xout	|		xout_	|
 		bout	/		bout_	|	Done
 						|
 		cout	\ done		cout_	|
 		wout	/		wout_	/
 		
 		
 		
 	All format are Recognised by compiler ( 32  <=> ' ' <=> 0x20 ) 
 
 	
 ------------------------------------------------------
 
 6.0 Function Update (0.0.3)
 
 
 	def name	\
 			|
 			|	Define a function name
 			|
 	endef		/
 
 7.0 Var Update (0.0.4)
 
 
 	scope <type> name
 	scope <type> value name
 	scope value name
 	
 	
 	scope can be:
 			global
 			local
 			
 	
 	name   =>  push value (must be int/32bit data)	
 	name=  =>  set var value to top of Data stack
 	(name1)name2=	=>	set value of name2 to value of name 1
 	
 8.0 Func with args (0.0.4.5)
 
 	
 	def (<type> varname)funcname
 	
 	(x)funcname	-->varname is a "local" reference to var x
 
9.0[next version]STRING STACK
 	
 	new instr for str:
 
 
($push) 'text'	   Direct str insertion ( from "sourcecode" [is just a hidden var, const])

($out)	$.	Direct String output(pop) from string stack
	
	$get		read input from user in inpt buffer
	  $getl
	  $get0
	  
	  
	$ipush	   push input buffer on strstack
	
      [  ipush  ]push buffer content size to data stack
      
      
      
      indirect output:
      
	
	$_	pop top of str stack to output buffer
	 $_l
	 $_0
      
      
      Input size managment:
      
      	idrop		flush surplus frop input_buffer (arg is max keeped)
      	$idrop 	flush ALL 	"       "      
      	
      	
     [		]	flush surplus frop input_buffer  TO output_buffer(arg is max keeped)
     [ 	]	flush ALL 	"       "          "    "
      	
      	flush		flush output_buffer to output
      
      
      
      
      
