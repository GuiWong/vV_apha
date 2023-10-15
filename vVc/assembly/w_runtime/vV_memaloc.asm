

;Will Be Needed in version 0.0.3 for vars

segment .bss

	
	
	var_space:
	ALIGNB 4
;---------------------------var reserved Space-----	

	var_int:
		
		resd	512
		
		
	var_sting:
	
		resb 	2048
		

