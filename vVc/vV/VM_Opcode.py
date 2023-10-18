

NOP = 1

#-------------------------------------------------------------------------------
#------------------------------- Section ---------------------------------------#-------------------------------------------------------------------------------
#-------------------------- Stack Manipulation ---------------------------------
#-------------------------------------------------------------------------------

PUSH = 5
SWAP = 6
DROP = 7 	# 
#OUT  = 8	#  Will Need a w runtime for compiled version

DUP = 22
 #|
 #|
 #|
 # DUPx -> 22 + x , max 31


#-------------------------------------------------------------------------------
#------------------------------- Section ---------------------------------------#-------------------------------------------------------------------------------
#------------------------------ Arithmetics ------------------------------------
#-------------------------------------------------------------------------------


class Affixed_op:

	def __init__(self,allowed_raw,intacc= False):
	
		#self.affix = afx
		self.allowed = allowed_raw
		self.int_accept = intacc
	




ADD = 32
SUB = 33
MUL = 34
DIV = 35
NEG = 36
MOD = 37
#
#
#
#-------------------------binary ops
LSH = 40
RSH = 41
dummy_equal = 42
NOT = 43
AND = 44
OR = 45
XOR = 46
#
#


#------------------------Boolean ops (binary ops + 8)
LESS = 48
MORE = 49
EQUAL = 50

#NOT NEEDED IF
#false:=0 true:=-1
#can use binary ops

#NOT = 51
#AND = 52
#OR = 53
#XOR = 54



#-------------------------------------------------------------------------------
#------------------------------- Section ---------------------------------------#-------------------------------------------------------------------------------
#----------------------------- Flow Control ------------------------------------
#-------------------------------------------------------------------------------

END_BLOCK = 64		#Virtual for Ifs, maybe not used
IF = 65		#Map to jmp if, 1 instruction
ELSE = 66		#Map to jmp(end) , 
ELIF = 67
ELIF2 = 68		# End:	#is just a dest for last jump, no opcode should be added

#REPEAT = 73;
DO = 74		#transparent, just adress for while [But start Block]
WHILE = 75		#sameopcode as an if, but jumps backwards

BREAK = 76





#-----------------------------------------------------------------------------------
#------------------------------ Section --------------------------------------------
#----------------------------------------------------------------------------------
#------------------------------  I/O  ---------------------------------------------


OUT  = 96
BUFF_OUT = 97
FLUSH = 98
GET = 99







DEF = 192
ENDEF = 193
CALL = 194
RET = 195


SQUOTES = 250
DQUOTES = 251

TAB = 252
N_LINE = 253
COMMENT = 254
SPACE = 255

'''
class Opcode:

	op=0
	arg=0
	def __init__(self,op,arg):
	
		self.op=op
		self.arg=arg
		

	
class Opcode_descriptor:

	op=0
	text = ''
	prefix = ''
	suffix = ''
	name = ''
	
'''

define = {

	'def' : DEF,
	'endef' : ENDEF
	
	}


quotes = {

	"'" : SQUOTES,
	'"' : DQUOTES
	
	}
	
separator = {

	' ' : SPACE,
	'\n': N_LINE,
	'	' : TAB,
	';' : COMMENT
	}	
	
	
block_op ={		#WARNING: Need virual ops

	IF : "if",
	ELSE : "el" ,
	#ELIF : "elif",
	
	END_BLOCK : ",",
	
	DO : 'do',
	WHILE:'while',
	
	BREAK : 'break'
	#REPEAT:'repeat'

}

class Block_Type:

	NONE = 0
	IF = 1
	ELSE = 2
	ELIF = 3
	END = 4
	DO = 5
	WHILE = 6
	#REPEAT=6
	
	BREAK = 8
	
block_type= {

	IF : Block_Type.IF,
	ELSE : Block_Type.ELSE,
	END_BLOCK : Block_Type.END,
	DO : Block_Type.DO,
	WHILE : Block_Type.WHILE,
	BREAK : Block_Type.BREAK,
	#ELIF : Block_Type.ELIF

}


suffixes_op= {


	IF : '?',
	NOP : NOP
	
	
}

class Format:

	NONE = 0
	DEC = 1
	#SIG = 2
	HEX = 3
	BIN = 4
	
	CHR = 8
	PCHR = 9
	
format_prefixed = {

	GET : 'get',
	OUT : 'out',
	BUFF_OUT : 'out_'
	
	
	}

format_prefixes = {

	'd': Format.DEC,
	'x': Format.HEX,
	'h': Format.HEX,
	'b': Format.BIN,
	'c': Format.CHR,
	'w': Format.PCHR
	

}

prefixes_op = {

	NOP : NOP

}


int_prefixed = {

	DUP : 'dup'

}



prefix_allow_TEMP = [LSH,RSH,dummy_equal,NOT,AND,OR,XOR]


virtual_op = {

	dummy_equal : '=',
	IF : "if",
	ELSE : "el" ,
	#ELIF : "elif",
	
	END_BLOCK : ",",
	DO : 'do',
	WHILE:'while',
	BREAK : 'break'
	
	
	
	}



direct_op = {
	
	DUP : "dup",
	SWAP: "swp",
	DROP: "drp",
	ADD: "+",
	SUB: "-",
	MUL: "*",
	DIV: "/",
	MOD:'%',
	#NEG: "!",
	
	LSH: "<",
	RSH: ">" ,
	
	LESS:'<?',		#produce a "boolean on the stack"
	MORE:'>?',
	EQUAL:'=?',
	
	
	
	NOT : "!",
	AND : "&",
	OR : "|",
	XOR : "^",		#meh...
		#ENdblock is a virtual opcode
				#for ifs statements (not for while
				
	GET : "get",
	
	OUT: "out",
	BUFF_OUT:"out_",
	
	FLUSH : "flush",
	
	
	
	ENDEF : "endef"
}


#TODO: Have a full string to OP dict? maybe? YES
#	so first: get virtual Opcode for char
#	then: check if in table?


def get_dir_opcode_by_string(arg):

	return direct_op.keys()[direct_op.values().index(arg)]
	
def get_virual_opcode_by_string(arg):

	if arg in virtual_op.values():
	
		return virtual_op.keys()[virtual_op.values().index(arg)]
	else:
		return direct_op.keys()[direct_op.values().index(arg)]



