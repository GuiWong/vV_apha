

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
		# End:	#is just a dest for last jump, no opcode should be added

#REPEAT = 73;
DO = 74		#transparent, just adress for while [But start Block]
WHILE = 75		#sameopcode as an if, but jumps backwards





#-----------------------------------------------------------------------------------
#------------------------------ Section --------------------------------------------
#----------------------------------------------------------------------------------
#------------------------------  I/O  ---------------------------------------------


OUT  = 96
GET = 97




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
	
separator = {

	' ' : SPACE,
	'\n': N_LINE,
	'	' : TAB,
	';' : COMMENT
	}	
	
	
block_op ={

	IF : "if",
	ELSE : "el" ,
	
	END_BLOCK : ",",
	
	DO : 'do',
	WHILE:'while'
	#REPEAT:'repeat'

}

class Block_Type:

	NONE = 0
	IF = 1
	ELSE = 2
	END = 3
	DO = 4
	WHILE = 5
	#REPEAT=6
	
block_type= {

	IF : Block_Type.IF,
	ELSE : Block_Type.ELSE,
	END_BLOCK : Block_Type.END,
	DO : Block_Type.DO,
	WHILE : Block_Type.WHILE

}


suffixes_op= {


	IF : '?',
	DUP :':',
	NOP : NOP
	
	
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
	
	END_BLOCK : ",",
	DO : 'do',
	WHILE:'while'
	
	
	}



direct_op = {
	
	DUP : "dup",
	SWAP: "swp",
	DROP: "drp",
	OUT: ".",
	ADD: "+",
	SUB: "-",
	MUL: "*",
	DIV: "/",
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



