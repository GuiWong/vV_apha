
import vV.VM_Opcode as OP


class vV_Type:

	UNFOUND = 0
	VALUE = 1
	POINTER = 2		#Base Type, tobe Ored with appropriate type???
	
class Scope:

	GLOBAL = 1
	LOCAL = 2
	

scope_names = ["global","local"]
type_names = ["unfound","value","pointer"]


class vV_Variable:


		
	name = ''
	var_type = vV_Type.UNFOUND
	scope = Scope.GLOBAL
	is_init = False
	init_value = 0
	
	internal_id = 0	#may be usefull for argument ordering double verification




	def __init__(self,name,scope,vV_type,is_init=False,init_value=0):
	
		self.name = name
		self.var_type = vV_type
		self.scope = scope
		self.is_init = is_init
		self.init_value = init_value
		
		
	def __str__(self):
	
		return "Var "+self.name+" \n Scope: "+OP.var_define.keys()[OP.var_define.values().index(self.scope)]+"\n Type: "+OP.var_type.keys()[OP.var_type.values().index(self.var_type)]+"\n With Value: "+str(self.init_value)
		
		
