
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
	




vV_o_hex:					;value in eax
						;dest in rdi



	xor ecx , ecx	
	
	mov esi , 16

	
	.loop01:
	
		xor rdx , rdx
		
		div esi
		
		
		cmp dl , 10
		
		jb .dec
		
			add dl , 7
		
		.dec:
		
			add dl , '0'
		
		
		push rdx
		
		inc ecx
		
		cmp eax , esi
		
		jae .loop01
	
	
	cmp al , 10
		
		jb .dec2
		
			add al , 7
		
		.dec2:
		
			add al , '0'	
	mov [rdi] , al
	
	jmp vV_o_pop_digits
		
	
	
	
vV_o_decimal:					;value in eax
						;dest in rdi
						;max_dest_size in r9d



	xor ecx , ecx	
	
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
	mov [rdi] , al
		
	
		
	vV_o_pop_digits:			; Need nb of digits currently on stack(ecx)
						;dest in rdi
		mov r8d , 1
		inc ecx
		
		cmp ecx , r9d
		
		jb .loopstart
		
	
			mov rax , 26;	#TODO: Defined Errors code/ data in file
			xor rdx , rdx
			mov edx , ecx
			mov ecx , r9d
		
			call w_forced_exit
		
						
		.loopstart:
		
			pop rdx
			mov BYTE[edi + r8d] , dl
			inc r8d
			
			cmp r8d , ecx
		
		jb .loopstart
	
	
		mov eax , ecx
		
		ret	
	
	
vV_o_binary:					;value in eax, 
						;base in esi


	xor ecx , ecx
	
	
	.loop01:
	
		
		shr eax , 1
		
		jc .one
		
			mov dl , '0'
			push rdx
			
		jmp .next
		.one:
			
			mov dl , '1'
			push rdx
		
		.next:
		
		inc ecx
		
		cmp eax , 1
		
		jae .loop01
	
	add al , '1'	
	mov [rdi] , al
	
	jmp vV_o_pop_digits




	wio_out:				; print top of data stack (int->str)
	
		sub r15 , 4
	
		mov eax, [r15]				;set rax to top of dstack
		
		
		
		mov edi , w_output_buffer
		mov r9 , 255
		
		call vV_o_hex;vV_o_binary;vV_o_decimal				;get str repr of rax in w_number_buffer
		
		
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
		
		
		
		
		
		
		



