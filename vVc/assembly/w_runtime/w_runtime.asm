%define SYS_EXIT 60

;%include "wio.asm"


%include "vVc/assembly/w_runtime/vV_errors.asm"
%include "vVc/assembly/w_runtime/vV_system0.asm"
%include "vVc/assembly/w_runtime/vV_system1.asm"
%include "vVc/assembly/w_runtime/vV_memaloc.asm"
%include "vVc/assembly/w_runtime/vV_stack_init.asm"


global _start

global w_input_buffer
global w_output_buffer
global w_number_buffer

;extern w_entry_point			;Defined by main program
global w_forced_exit			;Error caused exit


	
segment .data 

	is_main: db -1 			;May Be used for "lib" version of compile
						; or maybe another runtime?
	error: db 0xa," Error (wip) [code] [name]",0xa
	errsize equ $-error

	

segment .text 


	w_forced_exit:				;rax hold exit code
	
		push rax
		
	
		mov edx , errsize				;string lenght
		mov rsi , error			;strng ptr
		mov rdi , 2				;file descriptor, stderr
		mov rax , 1				; Write sysCall
		syscall
		
		
		pop rdi
		;mov rdi, rax
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
	
		mov DWORD [win_count] , 0
		mov DWORD [wout_count] , 0
		
		mov DWORD [endofline] , 0xa
		
		mov DWORD[vV_sys_format_mode] , vV_ascii_int_to_dec
		
		ret
		
		
	
		
_start:				;Entry point of Every Program
	
		

	mov rbp, rsp				;Setup Stack Frame
	
	mov r15 , fake_stack_start			;setup fake data stack
	
	call save_regs				;just in case
	
	
	call setup_memory			;all memory setup at start
	
	
	
	call w_entry_point			;Start the program 
	
	
	call restore_regs
	
;-----------attempt to clean input buffer--------------------------------------
	
	
	
	
	
	;mov edx , [w_output_buffer - 4]		;string lenght
	;	mov rsi , w_output_buffer			;strng ptr
	;	mov rdi , 1				;file descriptor, stdout
	;	mov rax , 1				; Write sysCall
	;	syscall

;------------------------------------------------------------------------------

	mov rax, SYS_EXIT
	mov rdi, 0				;Normal exit procedure (no code returned from main, need to call exit(code) forhat)
	syscall
	
	
	
	
	
