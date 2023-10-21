
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
		
		
		
	def solve_var(self,varname,scope = None):
	
		ret_val = ''
		
		
		if scope in self.functions:
		
			loc = self.functions[scope].solve_var(varname[0])
			
			if loc[0]:			#May need to check for ptr type
			
				return [True,loc[1],False,loc[2]]
				
		if varname[0] in self.global_vars:
		
				
			return [True,  self.global_vars[varname[0]].name,True,self.global_vars[varname[0]].var_type]
			
		else:
		
			return [False]
		
			
		
		
		
		
		
		
