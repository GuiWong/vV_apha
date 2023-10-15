
segment .bss

	ALIGNB 4
	
	
	;------------Input Buffer


	
	win_count: resb 4					;Input Buffer current content
	w_input_buffer: resb 255					;Input Buffer of 256 char
	
	
	
	
;------------Output Buffer



	
	wout_count: resb 4					;Output Buffer current content
	w_output_buffer: resb 255					;Output Buffer of 256 char
	
	
	
	
;------------Number Buffer


	
	
	w_number_buffer: resb 10				;Todo: Handle Bigger Numbers
	endofline: resb 1					;Maybe Not Needed
	



