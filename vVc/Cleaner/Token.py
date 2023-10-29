


class T_Type:


	BAD = 0
	OPCODE = 1
	
	VARDEF = 8
	FUNCDEF = 16
	VAR_OP = 32
	FUNC_CALL = 64

class Token:

	t_type = T_Type.BAD
	
