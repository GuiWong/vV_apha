

import vV_Variable



class vV_Function:



	name = ''
	referenced_vars = []
	local_vars = []
	code = []
	
	
	def __init__(self,name,args):			#args must be in ORDER!
	
		self.name = name
		self.referenced_vars = args
		self.local_vars = {}
		self.code = {}
		
	def add_local_var(self,var):
	
		self.local_vars[var.name] = var		#Will need to check type later
		
		return 0
		
	def store_code(self,codearray):	#probably not needed
	
		self.code = codearray.copy()
		
	def solve_var(self,name):
	
		if name in self.local_vars.keys():
		
			return [self.local_vars[name].var_type , 'ebp - '+str( ( self.local_vars.keys().index(name) + 1 ) * 8 )	]#Only for direct values
			
			
		elif name in self.referenced_vars.keys():
		
		
			return [self.referenced_vars[name].var_type , 'ebp + '+str( ( self.referenced_vars.keys().index(name) + 2 ) * 8 ) ]	#Only for direct values
			

