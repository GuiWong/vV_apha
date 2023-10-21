
import vV_Variable

import vV.VM_Opcode as OP

class Type_Checker:

	
	def __init__(self):
	
		pass
		
		
	def result_type(self,context,vartype,op_w_arg):
	
	
		if context == None:
		
			if isinstance(vartype, vV_Variable.vV_Int_Type):
			
				print " var is of type int : " + str(vartype)
				
				
				
				
				
				
				
			elif isinstance(vartype, vV_Variable.vV_Array_Type):
			
				print " var is of type array : " + str(vartype)
				
			else:
			
				assert False , "unrecognised type : "+str(vartype)
		
		else:
		
		
			assert False, "unimplemented yet"




