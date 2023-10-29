

segment .text 





vV_io_flush_no_nline:
	
	
	
	mov edx , DWORD[vV_output_buffer_content]			;string lenght	
	
	mov DWORD[vV_output_buffer_content] , 0
	
	mov rsi , vV_output_buffer			;strng ptr
		
	mov rdi , 1					;file descriptor, stdout
	mov rax , 1					; Write sysCall
	syscall
	
	
	
	ret
	

