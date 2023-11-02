
segment .bss

	ALIGNB 4
	vV_sys_start:	resd 16		;not used now

	
	
segment .data


;--Start of Memory----------------------------------------------------------

	ALIGN 8
	
;--System adresses offsets----------------

	vV_local_offset:
	dq 0
	
	
;---------------------Error Managment----------


;error vectors	
	
	vV_error_vectors:
	times 17 dq vV_error_unhandeled
	dq vV_error_invalid_index
	times 14 dq vV_error_unhandeled

	
	
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
	
vV_bound_error:

	mov ebx , edi
	mov ah , vV_ERR_MEMORY_OUT_OF_BOUND
	call vV_error	
	
	mov al , vV_ERR_MEMORY_OUT_OF_BOUND
	call vV_forced_exit
	
	
	
	
	
	

	
