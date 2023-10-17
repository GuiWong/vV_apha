

 


;segment .bss:		;TODO: allocate bss in system0x





segment .data:


	vV_error_msg:
	.default: db "Unhandeled Error "
	default_size equ $-.default
	
	vV_error_vectors:
	times 32 dq vV_error_unhandeled



segment .text:



vV_error:

	push rdx
	
	xor rdx , rdx
	
	mov dl , ah
	
	shl dl , 3
	
	call [vV_error_vectors + edx]
	
	
	pop rdx
	
	ret
	
	
vV_error_fatal:

	
	mov al , dl
	
	shr al , 3

	call w_forced_exit
	
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
	
	
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

