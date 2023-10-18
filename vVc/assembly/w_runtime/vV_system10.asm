
segment .bss

	ALIGNB 4
	
	
	;------------Input Buffer


	
	vV_input_buffer_content: resb 4			;Input Buffer current content
	vV_input_buffer: resb vV_input_buffer_size		;Input Buffer of 256 char
	
	
	
	
;------------Output Buffer



	
	vV_output_buffer_content: resb 4			;Output Buffer current content
	vV_output_buffer: resb vV_output_buffer_size		;Output Buffer of 256 char
	
	
	
	
;------------Number Buffer


	
	
	;w_number_buffer: resb 10				;Todo: Handle Bigger Numbers
	;endofline: resb 1					;Maybe Not Needed
	


segment .data
	ALIGN 4
	vV_sys_format_mode: dd vV_ascii_int_to_dec
