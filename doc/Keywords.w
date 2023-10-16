


1.0: basic Operations


	+	-	*	/		%

	<	>	!	|	&	^	
	
	
2.0: Boolean checks	
	
	<? >? =?					#Need lessandequal itou more

3.0: flow control


	if 	el	,
	
	do	while

4.0: Stack manipulation

 	(push) ' '	 xdup   	swp		drp		
 
 
 
 
5.0 To implement:
 
 
 DONE	get	[read input, send int data tostack]
 	
 DONE	(out) .  [top of stack to output as str repr]
 	
 	
 ------------------------------------------------------
 
6.0[next version]STRING STACK
 	
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
      
      
      
      
      
