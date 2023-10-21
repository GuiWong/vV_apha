

import precompiler.VarUpdate.vV_Variable as vV_Var

class Var_Solver:


	bss = ''
	data = ''
	
	def __init__(self,namespace):
	
	
		self.namespace = namespace
		self.bss = '\n	u_global:\n'
		self.data = '\n i_global:\n'
		
		
	def generate_var_decl(self):
	
		for v in self.namespace.global_vars:
		
			size = self.namespace.global_vars[v].calc_size()/8
			
			
		
			if self.namespace.global_vars[v].is_init:
			
				self.data += "."+self.namespace.global_vars[v].name + ": dq "+ str(self.namespace.global_vars[v].init_value) +"\n"
				
			else:
			
			
				self.bss += "."+self.namespace.global_vars[v].name + ": resb "+str(size)+" \n"
				
	def generate_var_file(self):
	
	
		outpt = ''
		
		outpt += ' segment .data \n'
		outpt += self.data
		outpt += ' segment .bss \n'
		outpt += self.bss
		
		return outpt
		
				
	def solve_var(self,var_name,scope):
	
	
		print "Solving var "+str(var_name)
		print "in scope: "+str(scope)
	
		tmp = self.namespace.solve_var(var_name,scope)	#This should check type
		
		print tmp
		adr = ''
		setup=''
		
		#args = var_name[1:]
		
		#print args
		
		
		assert tmp[0] , "UNSOLVABLE VAR PATH "+str(var_name[0])+" in "+str(scope)
		
		
		if isinstance(tmp[3],vV_Var.vV_Int_Type):
		
		
			if tmp[2]:
			
				if self.namespace.global_vars[var_name[0]].is_init:
			
					adr = "[i_global."+tmp[1] + "]"
				
				else:
			
					adr = "[u_global."+tmp[1] + "]"
					
			else:
			
			
				adr = tmp[1]
				
				
		elif isinstance(tmp[3],vV_Var.vV_Array_Type):
		
			if isinstance(tmp[3].content,vV_Var.vV_Int_Type):
			
				
				argu = []
				d = len(var_name)
				offset = 0
			
				if d > 1:
					
					argu = var_name[1]
					print argu
		
				if tmp[2]:
			
					i=1
					
					setup += "	xor eax , eax	\n"
					for d in argu:
					
						v=0
						#if d=="pop":
						
						#	print "should pop value"
							
						#else:
						
						#	v = d
							
						siz = 0
						if i< len(tmp[3].size):
						
							siz = tmp[3].size[i]
							
						else:
						
							siz = tmp[3].content.calc_size()/8
						
						print d
						if d=="pop":
						
							setup += "	vV_pop edi		\n"
							setup += "	add eax , edi			\n"
							
						else:
							setup += "	add eax , "+str(d)+"			\n"
						setup += "	mov ecx , "+str(siz)+"\n"
						setup += "	mul ecx		\n"
						#setup += " 	add edi , eax				\n"
						#offset += d
						i+=1
						
					setup += "	mov esi , eax		\n"
					setup += "	mov edi , u_global."+tmp[1]+"\n"
						
					adr = "[edi + esi]"
					
				else:
				
					assert False, "Locals Array unimplemented"
					
					
			else:
			
				assert False, "Unimplemented type for array"
				
				
				
				
		else:
		
			assert False, "Unknown or unimplemented  Type"
			
			
		return [adr , setup]
		
		
		'''
		
		if tmp[0]:
		
			
			print "Solving Var: " + var_name[0]
			print tmp[3]
			
			print "args: "+str(var_name[1:])
		
			adr = tmp[1]
			
		else:
		
			assert False, "UNSOLVABLE VAR PATH "+str(var_name)+" in "+str(scope)
			
		if tmp[2]:
		
			if self.namespace.global_vars[var_name[0]].is_init:
			
				adr = "[i_global."+adr + "]"
				
			else:
			
				adr = "[u_global."+adr + "]"
				
		return adr
			
		'''
		
		
	def push_var(self,varname,scope):
	
		txt = ''
		
		adr = self.solve_var(varname,scope)
		
		txt+=adr[1]
		
		txt += 'mov rax , '+adr[0]+'\n' 
		txt += 'vV_push eax\n' 
		
		return txt
		
		
	def pop_var(self,varname,scope):
	
		txt = ''
		
		adr = self.solve_var(varname,scope)
		txt+=adr[1]
		
		
		txt += 'vV_pop eax\n' 
		txt += 'mov '+adr[0]+' , rax\n' 
		
		return txt



