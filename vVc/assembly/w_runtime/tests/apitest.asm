%define SYS_EXIT 60
%include "vVc/assembly/w_runtime/vV_defines.asm"
%include "vVc/assembly/w_runtime/vV_io.asm"
%include "vVc/assembly/w_runtime/w_runtime.asm"


global w_entry_point


;extern w_input_buffer
;extern w_output_buffer
;extern w_number_buffer

;extern wio_out
;extern wio_get
;extern wio_get_str_raw
;extern wio_get_str_null
;extern wio_get_str_nline
;extern wio_move_in_to_out



segment .text 




w_entry_point:


	mov rbp, rsp			;Setup Stack Frame
	
	
	;call wio_get
	
	;call wio_get
	
	;mov DWORD [Wsp] , 63
	;mov DWORD [Wsp+4] , 126
	;add r15 , 8
	
	vV_push 63
	vV_push 126
	
	call wio_get
	
	call wio_get
	
	call wio_out
	call wio_out
	
	vV_swap
	
	
	
	vV_pop eax 
	
	mul DWORD[vV_sp-4]
	
	jc .Overflow
	
	sub vV_sp , 4 
	
	vV_push eax
	
	jmp .endOverflow
	.Overflow:
	
	mov rax , 3	;Overflow Error
	
	call w_forced_exit
	
	.endOverflow:
	
	
	;mov ecx , 2
	;lea rsi , [r15-8]
	;mov rdi , r15
		
	;rep movsd
	
	;add r15 , 8
	
	vV_dup 3
	
	
	
	
	mov eax , [r15-4]
	
	vV_pop eax
	vV_pop edx
	;cmp DWORD[r15-8] , eax
	
	cmp edx , eax
	
	jnz .else
	
			;mov DWORD[r15-8] , -1
			vV_push -1
	
	jmp .endofif
	.else:
	
			;mov DWORD[r15-8] , 0
			vV_push 0
	
	.endofif:
	;sub r15 , 4
	
	
	
	vV_push 63
	
	vV_pop eax
	

	
	call wio_out
	
	
	
	call wio_out
	call wio_out
	call wio_out
	
	mov eax , 255
	
	




	mov rsp , rbp
	
	ret
