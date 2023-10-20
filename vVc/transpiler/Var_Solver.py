


class Var_Solver:


	bss = ''
	data = ''
	
	def __init__(self,namespace):
	
	
		self.namespace = namespace
		self.bss = '\n	u_global:\n'
		self.data = '\n i_global:\n'
		
		
	def generate_var_decl(self):
	
		for v in self.namespace.global_vars:
		
		
			if self.namespace.global_vars[v].is_init:
			
				self.data += "."+self.namespace.global_vars[v].name + ": dq "+ str(self.namespace.global_vars[v].init_value) +"\n"
				
			else:
			
				self.bss += "."+self.namespace.global_vars[v].name + ": resq 1 \n"
				
	def generate_var_file(self):
	
	
		outpt = ''
		
		outpt += ' segment .data \n'
		outpt += self.data
		outpt += ' segment .bss \n'
		outpt += self.bss
		
		return outpt
		
				
	def solve_var(self,var_name,scope):
	
	
	
		tmp = self.namespace.solve_var(var_name,scope)
		adr = ''
		
		if tmp[0]:
		
			adr = tmp[1]
			
		else:
		
			assert False, "UNSOLVABLE VAR PATH "+str(var_name)+" in "+str(scope)
			
		if tmp[2]:
		
			if self.namespace.global_vars[var_name].is_init:
			
				adr = "[i_global."+adr + "]"
				
			else:
			
				adr = "[u_global."+adr + "]"
				
		return adr
			
		
		
		
	def push_var(self,varname,scope):
	
		txt = ''
		
		adr = self.solve_var(varname,scope)
		
		
		txt += 'mov rax , '+adr+'\n' 
		txt += 'vV_push eax\n' 
		
		return txt
		
		
	def pop_var(self,varname,scope):
	
		txt = ''
		
		adr = self.solve_var(varname,scope)
		
		
		txt += 'vV_pop eax\n' 
		txt += 'mov '+adr+' , rax\n' 
		
		return txt



