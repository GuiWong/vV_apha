
segment .bss

	ALIGNB 4
	vV_sys_start:	resd 16		;not used now

	vV_sys_format_mode: resd 1
	
	vV_error_buffer:
	resb 64
	vV_end_err_buff:
	vV_error_buffer_size equ vV_end_err_buff-vV_error_buffer
