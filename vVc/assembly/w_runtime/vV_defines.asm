
%deftok vV_sp 'r15'

%deftok vV_spS 'r14'

%define cell(a) (a*4)

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
	
