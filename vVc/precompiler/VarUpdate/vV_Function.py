

import vV_Variable



#WILL NEED TO CHANGE VAR TYPE


class vV_Function:



	name = ''
	referenced_vars = {}
	local_vars = {}
	code = []
	effective_namespace=''
	
	def __init__(self,name,args):			#args must be in ORDER!
	
		self.name = name
		self.referenced_vars = args
		self.local_vars = {}
		self.code = {}
		self.effective_namespace=''
		
	def set_effective_namespace(self,txt):
	
		self.effective_namespace=txt
		
	def add_local_var(self,var):
	
		self.local_vars[var.name] = var		#Will need to check type later
		
		return 0
		
	def store_code(self,codearray):	#probably not needed
	
		self.code = codearray.copy()
		
	def solve_var(self,name):
	
		if name in self.local_vars.keys():
		
			return [True, '[rbp - '+str( ( self.local_vars.keys().index(name) + 1 ) * 8 ) + "]"	,self.local_vars[name].var_type ]#Only for direct values
			
			
		elif name in self.referenced_vars.keys():
		
		
			return [True, '[rbp + '+str( ( self.referenced_vars.keys().index(name) + 2 ) * 8 ) + ']' , self.referenced_vars[name].var_type ]	#Only for direct values
		
		
		else:
		
			return [False]
			
	def get_var_obj(self,name):
	
		
		if name in self.local_vars.keys():
		
			return [True,self.local_vars[name] ]
			
			
		elif name in self.referenced_vars.keys():
		
		
			return [True,  self.referenced_vars[name] ]	#Only for direct values
		
		
		else:
		
			return [False]
			
			
			
	def get_arg_type(self,n):
	
		return self.referenced_vars.values()[-1-n].var_type
			
			
	def generate_call(self):
	
		lines = []
		
		for a in self.referenced_vars:
		
			pass
			
			
			
	def generate_head(self):
	
	
		txt = ''
		
		txt += self.effective_namespace+self.name + ":		\n"
		txt += "	push rbp	\n"
		txt += "	mov rbp , rsp	\n"
		
		
		r_c = len(self.referenced_vars)
		l_c = len(self.local_vars)
		
		txt +="\n;------Setup Phase\n"
		
		if  r_c > 0:
		
			pass
			#assert False, "unimplemented yet"
			
		if l_c > 0:
		
			
		
			txt+= "	sub rsp , "+str( (l_c + 1 )* 8	)+"	;Space for local vars	\n"
			
			
		txt +="\n;------Init Phase\n"
			
		for i in range(0,l_c):
		
			if self.local_vars.values()[i].is_init:
			
				txt += 'mov DWORD[rbp  - ' +str(  ( i + 1 ) * 8 )  +" ] , " + str(self.local_vars.values()[i].init_value)+"		; space for lvar "+str(i)+" ("+self.local_vars.values()[i].name+")	\n"
				
		txt +='\n.tailcall:		;Body Section	\n'
		
		
		return txt
		
	def generate_foot(self):
	
		txt = ''
		
		r_c = len(self.referenced_vars)
		l_c = len(self.local_vars)
		

		
		txt +="\n;------Cleanup Phase\n"
		
		if  r_c > 0:
		
			pass
			#assert False, "unimplemented yet"
			
		if l_c > 0:
		
			
		
			pass	#Not needed

		txt +="\n;------frame restore Phase\n"
		
		txt += "	mov rsp , rbp	\n"
		txt += "	pop rbp	\n"
		txt += "	ret	\n"
		
		return txt
			

