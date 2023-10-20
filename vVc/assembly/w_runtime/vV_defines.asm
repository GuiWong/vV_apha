


;------------------Variables From Project-------------

	;------------------Should come from io module(need refactoring)


	%define vV_input_buffer_size 255
	%define vV_output_buffer_size 255



;------------------Implementation Relative-------------

%deftok vV_sp 'r15'

%deftok vV_spS 'r14'

%deftok vV_sdir '-'




;------------------Stack Shortcuts--------------------

%define cell(a) (a*4)


%define vV_top [vV_sp vV_sdir %+ cell(1)]
%define vV_2nd [vV_sp vV_sdir %+ cell(2)]

%define vV_stack_v(a) ([vV_sp vV_sdir %+ cell(a)])


;-------------------Out_Format Pointer------------------

%deftok vV_FORMAT_BIN "vV_ascii_int_to_bin"
%deftok vV_FORMAT_DEC "vV_ascii_int_to_dec"
%deftok vV_FORMAT_HEX "vV_ascii_int_to_hex"



;--------------------Op Macros--------------------------

%macro vV_push 1

	mov DWORD[vV_sp] , %1
	add vV_sp , 4

%endmacro

%macro vV_pop 1

	sub vV_sp , 4
	mov %1 , [vV_sp]
	
%endmacro

%macro vV_swap 0

	mov edx , [vV_sp-4]
	mov eax , [vV_sp-8]
	mov [vV_sp-8] , edx 
	mov [vV_sp-4] , eax 
	
%endmacro

%macro vV_dup 1

	mov ecx , %1
	lea rsi , [vV_sp-cell(%1)]
	mov rdi , vV_sp
		
	rep movsd
	
	add vV_sp , cell(%1)
	
%endmacro


%macro vV_dec_sp 1

	sub vV_sp , cell(%1)
	
%endmacro
	
