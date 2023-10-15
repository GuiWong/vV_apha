
;Group all read/wrie syscalls

;global convert_to_string
;global convert_to_int

;extern w_input_buffer
;extern w_output_buffer
;extern w_number_buffer

global wio_out
global wio_get
global wio_get_str_raw
global wio_get_str_null
global wio_get_str_nline
global wio_move_in_to_out


segment .bss 
	ALIGN 32
	test: resb 4


	
segment .data 


	divisorTable:
   	dd 1000000000
   	dd 100000000
   	dd 10000000
   	dd 1000000
	dd 100000
  	dd 10000
	dd 1000
	dd 100
	dd 10
	dd 1


segment .text 


vV_i_parse_num:		;eax: number of char to read


								;use esi as counter/offset in string
								;concatenate result in eax
								;parse digit in cl
								
								;use r8 for base
								;use r9 for max_value
	mov edi , eax					
	dec edi
	xor esi, esi
	xor rax , rax
	xor rcx , rcx
	
	mov r8 , 10
	mov r9 , 58
	
	.start_loop:
	
		mov cl , [w_input_buffer + esi]
		
		
	;	cmp cl , 0xa					;Check for newline?
	;							;may use character count only
	;		je .end
	;
	
		;Check for format here, direct jump to 
	
			
		cmp cl , r9b
		
			jae .unvalid
		
		cmp cl , 48
		
			jb .unvalid
			
		sub cl , 48
		
		clc
		
		mul r8d
		
		jc .overflow
		
		add eax , ecx
		
		inc esi
		
		cmp esi , edi
		
		jb .start_loop
		
		;jmp .start_loop
		
	;.end:
		
		ret			; result should be in eax
		
	.unvalid:
	
		mov rax , 24;	#TODO: Defined Errors code/ data in file
		xor rdx , rdx
		mov dl , cl
		
		call w_forced_exit
		
	.overflow:
	
		mov rax , 25;	#TODO: Defined Errors code/ data in file
		;xor rdx , rdx
		;mov dl , cl
		
		call w_forced_exit
	
	
	
	
vV_o_decimal:					;value in eax



	xor ecx , ecx
	mov r8d , 1
	
	;xor edx , edx
	
	mov esi , 10
	
	.loop01:
	
		xor rdx , rdx
		
		div esi
		
		
		add dl , '0'
		push rdx
		
		inc ecx
		
		cmp eax , 10
		
		jae .loop01
	
	add al , '0'	
	mov [w_output_buffer] , al
		
	inc ecx
		
	.loop02:
	
		pop rdx
		mov BYTE[w_output_buffer + r8d] , dl
		inc r8d
			
		cmp r8d , ecx
		
		jb .loop02
	
	
	mov eax , ecx
		
	ret	
	



convert_to_string:				; arg: rax  result: w_number_buffer

	mov r8 , 0			;set couner to 0
	mov r9 , 10			;set max to 10
	
	.loop:
	
	xor rdx , rdx					;ero out rdx
	
	div dword [divisorTable + r8 * 4]		;div rax by consecutive power of 10
	
	add rax , '0'					;convert result to ascii
	
	mov [w_number_buffer + r8] , al		;
	
	mov rax, rdx
	
	inc r8
	
	cmp r8, r9
	
	jne .loop
	
	ret 
	
	
	
	
	



	wio_out:				; print top of data stack (int->str)
	
		sub r15 , 4
	
		mov eax, [r15]				;set rax to top of dstack
		
		
		
		call vV_o_decimal				;get str repr of rax in w_number_buffer
		
		
		mov BYTE[w_output_buffer + eax] , 0xa
		
		inc eax
		
		mov edx , eax				;string lenght		#TODO: remove leading 0
		mov rsi , w_output_buffer		;strng ptr
		mov rdi , 1				;file descriptor, stdout
		mov rax , 1				; Write sysCall
		syscall
	
		ret
		
		
	wio_get:
	
	
		mov rsi , w_input_buffer		;ptr to string destination	
		mov edx , 255				;string lenght		#TODO: handle multiple lenght numbers
		mov rdi , 0				;file descriptor, stdin
		mov rax , 0				; read sysCall
		
		syscall
		
		
;-------------Buffer_Overflow_Execption  (experiment) [Working for now]



		cmp eax , 255
		
		jb .no_overflow
		
		
		cmp BYTE[w_input_buffer +254] , 0xa
		
		je .no_overflow
		
			mov rax , 12		;placeholder value for now, 
						;TODO: Make ERRORS constants
		
			call w_forced_exit 	;NOTE: should handle ret adress? #TODO
		
		.no_overflow:
		
;----------------------------------------------


		call vV_i_parse_num
		
		mov [r15] , eax
		
		add r15 , 4
		
		ret
		
	wio_get_str_raw:		;removes the new_line
	
		mov r10 , .end
		
		
		
		
		jmp wio_get_str
		
		.end:
		
		dec DWORD [w_input_buffer-4]
		
	
		
		ret
	
	wio_get_str_null:		;null terminated
	
		mov r10 , .end
		
		
		jmp wio_get_str
		
		.end:
		
		mov rsi , w_input_buffer
		
		add esi ,[w_input_buffer -4]
		
		dec rsi
		
		mov BYTE [rsi] , 0
		
		
		
		ret
	
	wio_get_str_nline:		;keep the new line
	
		mov r10 , .end
		
		
		jmp wio_get_str
		
		.end:
		
		ret
		
		
	wio_get_str:				;arg: eax: size to read	r10: return adrr
							; ?? may use rsi for dest info???
							; then shouldn't increment rsi in get_str
							; maybe make a get_string_direct later???
							; or do adr calc before?
							; maybe 2 entry point/ 1 exit point?
	
	
		mov rsi , w_input_buffer			;ptr to string destination	
		add esi , [w_input_buffer - 4]
		mov edx , eax				;string lenght		#TODO: handle multiple lenght numbers
		;sub edx , [w_input_buffer - 4]
		mov rdi , 0				;file descriptor, stdin
		mov rax , 0				; read sysCall
		
		syscall
		
		
		
		
		
		;dec eax
		
		add [w_input_buffer-4] , eax
		
		
		jmp r10
		
		
	wio_move_in_to_out:
	
	
		mov ecx , [w_input_buffer-4]
		add ecx , 4
		mov esi , w_input_buffer-4
		mov edi , w_output_buffer-4
		
		rep movsb
		
		mov DWORD [w_input_buffer-4] , 0
		
		
		
		ret
	
	
		
		
	wio_flush:
	
	
		
		mov edx , [w_output_buffer - 4]		;string lenght
		mov rsi , w_output_buffer			;strng ptr
		mov rdi , 1				;file descriptor, stdout
		mov rax , 1				; Write sysCall
		syscall
	
		ret
		
		
		
		
		
		
		



