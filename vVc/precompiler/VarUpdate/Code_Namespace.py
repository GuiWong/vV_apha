
import vV_Function
import vV_Variable



class NameSpace_Error:


	SYMBOL_REDEFINE = 1



#Errors: catched by compilerto get adress?
#ret_value indicate Errors?



class NameSpace_Manager:


	global_vars = {}
	functions = {}
	
	
	def __init__(self):
	
		self.global_vars = {}
		self.functions = {}
	
	
	def define_function(self,name,args = {}):
	
		if name in self.functions.keys(): 
		
			return NameSPace_Error.SYMBOL_REDEFINE
		
		
		self.functions[name] = vV_Function.vV_Function(name,args)
		
		return 0
		
	def define_global(self,var_obj):
	
		#assert name not in self.global_vars.keys() ,"Raise redefs erreor, need proper_error_managment"
		
		if var_obj.name in self.global_vars.keys():
		
			return NameSPace_Error.SYMBOL_REDEFINE
		
		self.global_vars[var_obj.name] = var_obj  #vV_Variable.vV_Variable()
		
		return 0
