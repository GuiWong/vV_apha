




	

	0.0.2.3.1:	
				-Project structure cleanup
				-Support for char, packedchar, binary and hexadecimal in source file
		
	0.0.2.2:
				-Reworked Error management, Still in progress
				-new "block" logic, allowing sub_blocks
				- break keyword, to exit a loop
	
	
	
	
		
I/O Update	0.0.2.0
		
			-Input and Output Buffer Initialized by vV runtime
			-get keyword, with format prefix. push 32bit value on the data stack from input.
				Forced exit in case of bad input/Inputoverflow
				(Will probably call a stored adress, to allow Error Catching)
			 	
			
			Unsigned Int:
			
				dget  :  Decimal  [may swich to hex if reading 'x' or 'h' , to bin with 'b']
				bget  :  Binary   [may swich to hex if reading 'x' or 'h']
				
				xget  :
				hget  :  Hex	  [Won't switch ( allow starting with "b")

			Char:
			
				cget  :  Char	  [Zero check, just push first Byte of input Buffer to data Stack]
				
			PackedChar:
			
				wget  :  4 chars stored as a 32bit unsigned integer. missing chars are zeroed
				
			-out keyword, with same formats as get
			
				( out , dout , xout/hout , cout , wout )
				
			-Buffered out, fill the output buffer without printing
			
				( out_ , dout_ , xout_/hout_ , cout_ , wout_ )
				
				
		
		
	0.0.1 --> 0.0.1.5  (first working version)
			
		Basic assembly runtime
		Python precompiler / Transcompiler
		barebone i/o

	