

;%include "vVc/assembly/w_runtime/vV_ascii.asm"


;Group all read/wrie syscalls

;global convert_to_string
;global convert_to_int

;extern vV_input_buffer
;extern vV_output_buffer
;extern w_number_buffer

global wio_out
global wio_get
global wio_get_str_raw
global wio_get_str_null
global wio_get_str_nline
global wio_move_in_to_out


segment .text 



vV_io_flush_no_nline:							;Temporary
	
	
	
	mov edx , DWORD[vV_output_buffer_content]			;string lenght	
	
	mov DWORD[vV_output_buffer_content] , 0
	
	mov rsi , vV_output_buffer			;strng ptr
		
	mov rdi , 1					;file descriptor, stdout
	mov rax , 1					; Write sysCall
	syscall
	
	
	
	ret

vV_io_flush:
	
	
	
	mov edx , DWORD[vV_output_buffer_content]			;string lenght	
	
	mov DWORD[vV_output_buffer_content] , 0
	
	mov rsi , vV_output_buffer			;strng ptr
		
	mov BYTE[vV_output_buffer + edx] , 0xa
	inc edx
		
	mov rdi , 1					;file descriptor, stdout
	mov rax , 1					; Write sysCall
	syscall
	
	
	
	ret
	
		
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
	
vV_io_out_buffer_default:

	mov r10d , DWORD[vV_sys_format_mode]	
	call vV_io_out_buffer
	ret
	
vV_io_out_default:

	mov r10d , DWORD[vV_sys_format_mode]	
	call vV_io_out
	ret

;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
	
vV_io_out_buffer:				;print str repr of Top Of Stack element
						
						
	call vV_io_out01			
	call vV_io_out_buffer_end
	ret

;-------------------------------------------------------------------------------
		
vV_io_out:					;print str repr of Top Of Stack element


	call vV_io_out01					
	call vV_io_out_direct_end
	ret

;-------------------------------------------------------------------------------	
;-------------------------------------------------------------------------------	

vV_io_out01:					;print str repr of Top Of Stack element


	vV_pop eax				;get value in eax
	
	mov edi , vV_output_buffer		;set dest as O_buff
	add edi ,DWORD[vV_output_buffer_content]		;set offset to start of freespace
	
push rdi					;Save buffer origin
	
	mov r9 , 255				;set Max buffer available	
	sub r9d , edi				;#TODO: Stop HardCoding VALUES!!!!
		call r10			;call current conversion format function
	xor rdi , rdi
	
pop rdi						;recover Buffer origin
	
	ret

;-------------------------------------------------------------------------------	
	
vV_io_out_direct_end:



	mov BYTE[edi + eax] , 0xa		;add new_line
		
		inc eax
		
		mov edx , eax				;string lenght		
		mov rsi , rdi				;strng ptr
		mov rdi , 1				;file descriptor, stdout
		mov rax , 1				; Write sysCall
		syscall
	
		ret

;-------------------------------------------------------------------------------		
		
vV_io_out_buffer_end:

	add [vV_output_buffer_content] , eax

	ret

;-------------------------------------------------------------------------------

vV_io_out_char:

	
	call vV_io_read_char
	call vV_io_out_direct_end
	
	ret
	
vV_io_out_packed_char:

	
	call vV_io_read_packed_char
	
	call vV_io_out_direct_end
	
	ret
	
vV_io_out_char_buffer:

	call vV_io_read_char
	
	call vV_io_out_buffer_end
	
	ret
	
vV_io_out_packed_char_buffer:

	call vV_io_read_packed_char
	
	call vV_io_out_buffer_end
	
	ret
	
vV_io_read_char:

	vV_pop eax
	
	mov rdi , vV_output_buffer
	add edi , [vV_output_buffer_content]
	
	mov [edi] , al
	
	mov edi , vV_output_buffer
	mov eax , 1
	
	ret	
	
vV_io_read_packed_char:

	vV_pop eax
	
	mov rdi , vV_output_buffer
	add edi , [vV_output_buffer_content]
	
	mov [edi] , eax
	
	mov edi , vV_output_buffer
	mov eax , 4	
	
	ret
		
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------
	
vV_io_read:

								
		mov rsi , vV_input_buffer		;ptr to string destination	
		mov edx , vV_input_buffer_size				;string lenght	
		mov rdi , 0				;file descriptor, stdin
		mov rax , 0				; read sysCall
		
		syscall
	
;-------------Buffer_Overflow_Execption  



		cmp eax , 255				;Check if Buffer Is Full
		
			jb .no_overflow
			
		cmp BYTE[vV_input_buffer + vV_input_buffer_size-1] , 0xa	;Check if Buffer end with "\n"
		
			je .no_overflow
		
		
			push rax
			push rbx
		
			mov ah , vV_ERR_IO_I_OVERFLOW
			or ax , 0
			xor rbx , rbx
			mov rbx , rsi
		
			call vV_error
		
			pop rbx
			pop rax
		
			;ret
		
		.no_overflow:
		
			ret
		
		
	
	
vV_io_get_default:

	mov r10d , vV_ascii_as_dec			;TODO: default settings
	call vV_io_get
	ret
	
	
vV_io_get:						;convert inputed value to 
							;32bit int, push it on
							;the stack
	call vV_io_read
		
;----------------------------------------------	

	push rbx				;Save rbx (conversion uses it) 

		mov ebx , eax 			;send char count by ebx
		xor edi , edi 			;zero out counter
		mov esi , vV_input_buffer	;Set source to I_buffer
		

		call r10
		
	pop rbx
	
		vV_push eax
		
		ret


;-------------------------------------------------------------------------------
;-------------------------------------------------------------------------------


vV_io_get_char:


	call vV_io_read
	
	xor edx , edx
	
	mov dl , [vV_input_buffer]
	
	vV_push edx
	
	ret
	
vV_io_get_packed_char:

	mov DWORD [vV_input_buffer] , 0

	call vV_io_read
	
	xor edx , edx
	
	mov edx, [vV_input_buffer]
	
	vV_push edx
	
	ret
	
		
		



