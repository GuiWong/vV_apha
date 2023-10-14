%define SYS_EXIT 60

;%include "wio.asm"

global _start

global w_input_buffer
global w_output_buffer
global w_number_buffer

;extern w_entry_point			;Defined by main program
global w_forced_exit			;Error caused exit

segment .bss


;----------------Fixed memory Allocation for w systems----------------------------


;------------Input Buffer


	
	win_count: resb 4					;Input Buffer current content
	w_input_buffer: resb 255					;Input Buffer of 256 char
	
	
	
	
;------------Output Buffer



	
	wout_count: resb 4					;Output Buffer current content
	w_output_buffer: resb 255					;Output Buffer of 256 char
	
	
	
	
;------------Number Buffer


	
	
	w_number_buffer: resb 10				;Todo: Handle Bigger Numbers
	endofline: resb 1					;Maybe Not Needed
	
	
	
	
;------------Temporary Stack
	
	
	
	fake_stack: resd 2046					;Can be local, because dsp(r15) is setup on start by runtime
	

	
	
segment .data 

	is_main: db -1 			;May Be used for "lib" version of compile
						; or maybe another runtime?


	

segment .text 


	w_forced_exit:
	
	
		call restore_regs
		
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
	
		mov DWORD [win_count] , 0
		mov DWORD [wout_count] , 0
		
		mov DWORD [endofline] , 0xa
		
		ret
		
		
	
		
_start:				;Entry point of Every Program
	
		

	mov rbp, rsp				;Setup Stack Frame
	
	mov r15 , fake_stack			;setup fake data stack
	
	call save_regs				;just in case
	
	
	call setup_memory			;all memory setup at start
	
	
	
	call w_entry_point			;Start the program 
	



	mov rax, SYS_EXIT
	mov rdi, 0				;Normal exit procedure (no code returned from main, need to call exit(code) forhat)
	syscall
	
	
	
	
	
