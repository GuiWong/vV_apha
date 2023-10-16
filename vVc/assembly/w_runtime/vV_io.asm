

%include "vVc/assembly/w_runtime/vV_ascii.asm"


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


segment .text 





	vV_io_flush:
	
	
	
		mov edx , DWORD[wout_count]			;string lenght	
		mov rsi , w_output_buffer			;strng ptr
		
		;dec edx			
		;dec edx
		
		mov BYTE[w_output_buffer + edx] , 0xa
		inc edx
		
		mov rdi , 1					;file descriptor, stdout
		mov rax , 1					; Write sysCall
		syscall
	
		ret






	wio_out_buff:				; print top of data stack (int->str)
	
		sub r15 , 4
	
		mov eax, [r15]				;set rax to top of dstack
		
		
		
		mov edi , w_output_buffer
		add edi ,DWORD[wout_count]
		
		mov r9 , 255
		sub r9d , edi
		
		call vV_ascii_int_to_dec				;get str repr of rax in w_number_buffer
		
		
		;inc eax
		add [wout_count] , eax
		
	
		ret
		
	
		
;vV_io_out_format_default:
;
;	mov r10d , DWORD[vV_sys_format_mode]	
;	ret
	
vV_io_out_buffer_default:

	mov r10d , DWORD[vV_sys_format_mode]	
	call vV_io_out_buffer
	ret
	
vV_io_out_default:

	mov r10d , DWORD[vV_sys_format_mode]	
	call vV_io_out
	ret
	
vV_io_out_buffer:					;print str repr of Top Of Stack element


	call vV_io_out01					
	
	call vV_io_out_buffer_end
	
	ret
		
vV_io_out:					;print str repr of Top Of Stack element


	call vV_io_out01					
	
	call vV_io_out_direct_end
	
	ret
	
	

vV_io_out01:					;print str repr of Top Of Stack element


	vV_pop eax			;get value in eax
	
	mov edi , w_output_buffer	;set dest as O_buff
	add edi ,DWORD[wout_count]	;set offset to freespace
	
push rdi				;Save buffer origin
	
	mov r9 , 255			;set Max buffer available	#TODO: Stop HardCoding VALUES!!!!
	sub r9d , edi			;


	call r10			;call current conversion format function
	
	
	xor rdi , rdi
	
pop rdi						;recover Buffer origin
	
	ret
	
	
vV_io_out_direct_end:



	mov BYTE[edi + eax] , 0xa		;add new_line
		
		inc eax
		
		mov edx , eax				;string lenght		#TODO: remove leading 0
		mov rsi , rdi				;strng ptr
		mov rdi , 1				;file descriptor, stdout
		mov rax , 1				; Write sysCall
		syscall
	
		ret
		
		
vV_io_out_buffer_end:

	add [wout_count] , eax
		
	
		ret
		

		
	


	wio_out:				; print top of data stack (int->str)
	
		sub r15 , 4
	
		mov eax, [r15]				;set rax to top of dstack
		
		
		
		mov edi , w_output_buffer
		add edi ,DWORD[wout_count]
		
	push rdi
		
		mov r9 , 255
		sub r9d , edi
		
		call vV_ascii_int_to_hex;vV_ascii_int_to_dec				;get str repr of rax in w_number_buffer
	
	xor rdi , rdi
	pop rdi	
		
		mov BYTE[edi + eax] , 0xa
		
		inc eax
		
		mov edx , eax				;string lenght		#TODO: remove leading 0
		mov rsi , rdi				;strng ptr
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


push rbx

		mov ebx , eax 	;char count
		xor edi , edi 
		mov esi , w_input_buffer
		

		call vV_ascii_as_dec
		
pop rbx
		
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
		
		
		
		
		
		
		



