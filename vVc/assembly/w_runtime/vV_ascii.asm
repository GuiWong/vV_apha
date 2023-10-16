

segment .text 




vV_ascii_as_hex2:						;Jumped to from parse_num OR called
								;use edi as counter/offset in string !Set if direct call
								;use esi as source string
								;concatenate result in eax
								;parse digit in cl
								
								;use r8 for base
								;use r9 for max_value
								
							
	;mov r8 , 16	
	
	.start_loop:
	
		mov cl , [esi + edi]
	
		
		cmp cl , 48
		
			jb vV_ascii_unvalid
			
		cmp cl , 58
		
			jb .pass_int
			
			cmp cl , 'f'
			
				ja vV_ascii_unvalid
			
			cmp cl , 'a'
			
				jb vV_ascii_unvalid
				
			sub cl , 39
				
			
		.pass_int:	
			
		sub cl , '0'
		
		
		
		xor edx , edx
		
		clc
		
		mul r8d
		
		jc vV_ascii_overflow
		
		add eax , ecx
		
		.pass02:
		
		inc edi
		
		cmp edi , ebx
		
		jb .start_loop

		
		ret	
		
		
;
;				ebx		esi
;	ascii_to_format( buffer_size , buffer_adress ) 
;		
;
;	set:	rcx,rdx (rax) to 0
;		r8,r9
;		
;	call: specialized dexodefunction
		
vV_ascii_as_hex:
	
	dec ebx
	mov r8 , 16	
	xor rax , rax 		;(just in case not switching from dec mode)			
	xor rcx , rcx
	xor rdx , rdx
	jmp vV_ascii_as_hex2

vV_ascii_as_dec:

	dec ebx
	mov r8 , 10			
	mov r9 , 58
	xor rcx , rcx
	xor rdx , rdx
	jmp vV_ascii_as_decbin

vV_ascii_as_bin:

	dec ebx
	mov r8 , 2			
	mov r9 , 50
	xor rcx , rcx
	xor rdx , rdx
	
	jmp vV_ascii_as_decbin
	
vV_ascii_unvalid:
	
		mov rax , 24;	#TODO: Defined Errors code/ data in file
		xor rdx , rdx
		mov dl , cl
		
		call w_forced_exit
		
vV_ascii_overflow:
	
		mov rax , 25;	#TODO: Defined Errors code/ data in file
		;xor rdx , rdx
		;mov dl , cl
		
		call w_forced_exit
		
		
vV_ascii_change_to_hex:
		
		cmp eax , 0
			
			jne vV_ascii_unvalid
			
		mov r8 , 16
		xor rcx , rcx
		xor rax ,rax
				
		inc edi
		jmp vV_ascii_as_hex2		
		
	


vV_ascii_as_decbin:						;ebx: number of char to read

	

								;use edi as counter/offset in string
								;concatenate result in eax
								;parse digit in cl
								
								;use r8 for base
								;use r9 for max_value					
								;itou
	;xor edi, edi			;should be set by caller
	xor rax , rax
	
	xor rcx , rcx
	
	xor rdx , rdx
	
	
	.start_loop:
	
		mov cl , [esi + edi]
		
		
		cmp cl , 'b'										
			jne .pass01
		
		.format_change:
			
			cmp eax , 0
			
				jne vV_ascii_unvalid
				
			mov r8 , 2
			
			mov r9 , 50
	
			jmp .pass02
		
		
	
		.pass01:
		
		cmp cl , 'h'											
			je vV_ascii_change_to_hex
		cmp cl , 'x'											
			je vV_ascii_change_to_hex
			
			
		cmp cl , r9b
		
			jae vV_ascii_unvalid
		
		cmp cl , 48
		
			jb vV_ascii_unvalid
			
		
			
		sub cl , 48
		
		xor rdx , rdx
		clc
		
		mul r8d
		
		jc vV_ascii_overflow
		
		add eax , ecx
		
		.pass02:
		
		inc edi
		
		cmp edi , ebx
		
		jb .start_loop
		
		
		ret			; result should be in eax
		

	
;------------------------------------------------------------------------------------------
;------------------------------------------------------------------------------------------



vV_ascii_int_to_hex:					;value in eax
						;dest in rdi



	xor ecx , ecx	
	
	mov esi , 16

	
	.loop01:
	
		xor rdx , rdx
		
		div esi
		
		
		cmp dl , 10
		
		jb .dec
		
			add dl , 7
		
		.dec:
		
			add dl , '0'
		
		
		push rdx
		
		inc ecx
		
		cmp eax , esi
		
		jae .loop01
	
	
	cmp al , 10
		
		jb .dec2
		
			add al , 7
		
		.dec2:
		
			add al , '0'	
	mov [rdi] , al
	
	jmp vV_ascii_pop_digits
		
	
	
	
vV_ascii_int_to_dec:					;value in eax
						;dest in rdi
						;max_dest_size in r9d



	xor ecx , ecx	
	
	mov esi , 10
	


	
	.loop01:
	
		xor rdx , rdx
		
		div esi
		
		
		add dl , '0'
		push rdx
		
		inc ecx
		
		cmp eax , 10
		
		jae .loop01
	
	add al , '0'	
	mov [rdi] , al
		
	
		
vV_ascii_pop_digits:			; Need nb of digits currently on stack(ecx)
						;dest in rdi
		mov r8d , 1
		inc ecx
		
		cmp ecx , r9d
		
		jb .loopstart
		
	
			mov rax , 26;	#TODO: Defined Errors code/ data in file
			xor rdx , rdx
			mov edx , ecx
			mov ecx , r9d
		
			call w_forced_exit
		
						
		.loopstart:
		
			pop rdx
			mov BYTE[edi + r8d] , dl
			inc r8d
			
			cmp r8d , ecx
		
		jb .loopstart
	
	
		mov eax , ecx
		
		ret	
	
	
vV_ascii_int_to_bin:					;value in eax, 
							


	xor ecx , ecx
	
	
	.loop01:
	
		
		shr eax , 1
		
		jc .one
		
			mov dl , '0'
			push rdx
			
		jmp .next
		.one:
			
			mov dl , '1'
			push rdx
		
		.next:
		
		inc ecx
		
		cmp eax , 1
		
		jae .loop01
	
	;add al , '1'	
	;mov [rdi] , al
	
	jmp vV_ascii_pop_digits
	
	
;Will need a special version for String stack







