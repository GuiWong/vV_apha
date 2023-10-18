
segment .bss

	ALIGNB 4
	vV_sys_start:	resd 16		;not used now

	
	
segment .data


;--Start of Memory----------------------------------------------------------

	ALIGN 8
	
	
;---------------------Error Managment----------


;error vectors	
	
	vV_error_vectors:
	times 32 dq vV_error_unhandeled
	
	
	
segment .text


vV_error:

	push rdx
	
	xor rdx , rdx
	
	mov dl , ah
	
	shl dl , 3
	
	call [vV_error_vectors + edx]
	
	
	pop rdx
	
	ret
	
	
vV_error_fatal:

	
	mov al , dl
	
	shr al , 3

	call vV_forced_exit
	
	
	
	
	
	

	
