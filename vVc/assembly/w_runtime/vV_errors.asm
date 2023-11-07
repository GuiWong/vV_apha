


segment .bss


	ALIGNB 4
		
	vV_error_buffer:
	resb 64
	vV_end_err_buff:
	vV_error_buffer_size equ vV_end_err_buff-vV_error_buffer




segment .data

;Error String	

	
	vV_error_msg:
	.default: db "Unhandeled Error "
	default_size equ $-.default
	.invalid_index: db "Invalid Index Error : "
	inv_indx_size equ $-.invalid_index



segment .text


vV_error_invalid_index:


	push rsi
	push rdi	;Save reg used by syscall
	push r9	;and by conversion func
	push rbx	;Save Arg
	
	mov edx , inv_indx_size				;string lenght
	mov rsi , vV_error_msg.invalid_index			;strng ptr
	mov rdi , 2				;file descriptor, stderr
	mov rax , 1				; Write sysCall
	syscall	
	
	
	pop rax
	
	mov edi , vV_error_buffer
	mov r9d , vV_error_buffer_size
	call vV_ascii_int_to_dec	

	mov BYTE[vV_error_buffer + eax] , 0xa
	
	inc eax
	
	mov edx , eax				;string lenght
	mov rsi , vV_error_buffer			;strng ptr
	mov rdi , 2				;file descriptor, stderr
	mov rax , 1				; Write sysCall
	syscall
	
	pop r9
	pop rdi
	pop rsi
	
	
	mov rax , rdi 
	vV_push eax
	call vV_io_out_default
	call vV_io_flush
	
	call vV_climb_call_stack
	call vV_error_fatal
	
	ret
	
	
	

	
vV_error_unhandeled:


	push rsi
	push rdi	;Save reg used by syscall
	push r9	;and by conversion func
	
	
;push rax	;Save flags ( and value)

	push rbx	;Save Arg
push rdx		;Save error code
	
	
	mov edx , default_size				;string lenght
	mov rsi , vV_error_msg.default			;strng ptr
	mov rdi , 2				;file descriptor, stderr
	mov rax , 1				; Write sysCall
	syscall	
	
	
pop rax	;error code


	shr al , 3
	
	
	mov edi , vV_error_buffer
	mov r9d , vV_error_buffer_size
	

	call vV_ascii_int_to_dec	
	
		
	
	mov BYTE[vV_error_buffer + eax] , ' '
	
	
	
	
	lea rdi , [vV_error_buffer + eax + 1]
	sub r9d , edi
	
	pop rax
	
	call vV_ascii_int_to_dec
	
	lea r9 , [edi + eax]
	
	mov BYTE[r9] , 0xa
	
	inc r9
	
	sub r9 , vV_error_buffer
	
	mov edx , r9d				;string lenght
	mov rsi , vV_error_buffer			;strng ptr
	mov rdi , 2				;file descriptor, stderr
	mov rax , 1				; Write sysCall
	syscall
	
	pop r9
	pop rdi
	pop rsi
	
	
	
	
	ret
	
	
	
vV_climb_call_stack:

	mov rcx , rbp
	
	push rcx
	
	
	..@loop_call:
	
	;xor rax , rax
	mov rax , [rcx+8]
	
	cmp rax , vV_initial_return
	
	je ..@exit
	
	vV_push eax	
	call vV_io_out_default
	
	pop rcx 
	mov rcx , [rcx]
	push rcx
	
	jmp ..@loop_call
	..@exit:
	
	vV_push eax	
	call vV_io_out_default
	
	pop rcx 
	
	ret
	
	
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

