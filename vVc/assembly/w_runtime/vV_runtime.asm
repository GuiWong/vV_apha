%define SYS_EXIT 60


;%include "vVc/assembly/w_runtime/vV_errors.asm"
;%include "vVc/assembly/w_runtime/vV_system00.asm"
;%include "vVc/assembly/w_runtime/vV_system10.asm"
;%include "vVc/assembly/w_runtime/vV_system90.asm"


global _start



;extern vV_entry_point			;Defined by main program



	
segment .data 


	

segment .text 


	vV_forced_exit:				;rax hold exit code
							;Removed default error printing
							;This will now happens in errors module

		mov rdi, rax
		mov rax, SYS_EXIT
		syscall
		
		


	save_regs:			;In case called from other process
	
		pop rax
	
		push rbx
		push r12
		push r13
		push r14
		push r15
		
		push rax
		
		ret
		
	restore_regs:
	
		pop rax
	
		pop r15
		pop r14
		pop r13
		pop r12
		pop rbx
		
		push rax
		
		ret
		
	setup_memory:
	
		mov DWORD [vV_input_buffer_content] , 0
		mov DWORD [vV_output_buffer_content] , 0
		
		;mov DWORD [endofline] , 0xa
		
		mov DWORD[vV_sys_format_mode] , vV_ascii_int_to_dec
		
		
		mov ecx , 1073741823
		sub QWORD[vV_local_offset] , rcx
		
		
		ret
		
		
	
		
_start:				;Entry point of Every Program
	
		

	mov rbp, rsp				;Setup Stack Frame
	
	mov QWORD[vV_local_offset] , rbp
	mov QWORD[vV_initial_frame] , rbp
	
	mov r15 , fake_stack_start			;setup fake data stack
	
	call save_regs				;just in case
	
	
	call setup_memory			;all memory setup at start
	
	
	
	call vV_entry_point			;Start the program 
vV_initial_return:
	
	call restore_regs
	

;------------------------------------------------------------------------------

	mov rax, SYS_EXIT
	mov rdi, 0		;Normal exit procedure (no code returned from main)
	syscall
	
	
	
	
	
