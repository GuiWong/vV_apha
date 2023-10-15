
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
	
	
	

convert_to_int:			;convert string from w_number_buffer to int value in rax

					;	Input: rax->digit_number

	mov r9 , rax 	;		number of digits
	
	mov rbx , 10				;our awfull human base
	
	dec r9					; since starting from 0
	
	xor r8 , r8				; count number of digits processed
	
	mov rsi , w_number_buffer		;adress of string to numerize
	
	xor rax , rax
	xor rdx , rdx

	.start:
	
	mov dl , [rsi]				;fetch char ascii
	sub edx , '0'				;convert to value
	add eax , edx				;add to output

	inc r8					;increment counter
	inc rsi				;and pointer		(maybe one is enough)
	
	cmp r8 , r9				;check if finished
	je .end
	
	mul ebx				;move one column to the left
	
	jmp .start				;proceed to next digit
	
	
	.end:
	
	
	ret
	
	
	



	wio_out:				; print top of data stack (int->str)
	
		sub r15 , 4
	
		mov eax, [r15]				;set rax to top of dstack
		
		
		
		call convert_to_string				;get str repr of rax in w_number_buffer
		
		
		mov edx , 11				;string lenght		#TODO: remove leading 0
		mov rsi , w_number_buffer		;strng ptr
		mov rdi , 1				;file descriptor, stdout
		mov rax , 1				; Write sysCall
		syscall
	
		ret
		
		
	wio_get:
	
	
		mov rsi , w_number_buffer		;ptr to string destination	
		mov edx , 10				;string lenght		#TODO: handle multiple lenght numbers
		mov rdi , 0				;file descriptor, stdin
		mov rax , 0				; read sysCall
		
		syscall
		
		call convert_to_int
		
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
		
		
		
		
		
		
		


