
import precompiler.VarUpdate.vV_Variable as vV_Var



class Var_Op_Solver:


	def __init__(self,namespace):
	
		self.solver = Recursive_Var_Solver(namespace)
		
		
	def solve_push(self,data,scope):
	
	
		ns_data = self.solver.name_space.solve_var(data,scope)
		print ns_data[3]
	
		solved = self.solver.solve_var_name(data,scope)
		
		txt = solved[0]
		var_type = solved[1]
		
		print 'solving push:'
		print var_type
		

			
		txt += '	mov ecx , [edi+eax]	\n'
		
		while isinstance(var_type,vV_Var.vV_Ref_Type):
			
			print 'is a ref' 
			txt += '	mov ecx , [ecx]	\n'
			var_type = var_type.content		
		
		txt += '	vV_push ecx	\n'
		
		
		return txt
		
	def solve_pop(self,data,scope):
	
	
		#ns_data = self.name_space.solve_var(data,scope)
	
		solved = self.solver.solve_var_name(data,scope)
		
		txt = solved[0]
		var_type = solved[1]
		

			
		#txt += '	lea ecx , [edi+eax]	\n'
		txt += '	vV_pop ecx	\n'
		txt += '	lea edi , [edi+eax]	\n'
		
		while isinstance(var_type,vV_Var.vV_Ref_Type):
		
			txt += '	mov edi , [edi]	\n'
			var_type = var_type.content
		txt += '	mov [edi] , ecx	\n'
		
		return txt


class Recursive_Var_Solver:


	txt = ''

	def __init__(self,namespace):
	
		self.name_space = namespace
		
		
	def solve_adress(self,data):
	
	
		if data[2]:
		
		
			
			if self.name_space.global_vars[data[1]].is_init:
			
				adr = "[i_global."+data[1] +']'
				
			else:
			
				adr = "[u_global."+data[1] +']'
					
		else:
			
			adr = data[1]
			
		return adr
		
		
	def solve_referencing(self,data,var_type):
	
		
		if isinstance(var_type,vV_Var.vV_Ref_Type):
		
			return self.solve_referencing(data,var_type.content) + '	mov edi , [edi]	\n'
			
		else:
		
			return '	lea edi , '+self.solve_adress(data)+'	\n'
			
			
		
	def indexed_referencing(self,var_type):
	
		
		if isinstance(var_type,vV_Var.vV_Ref_Type):
		
			return '	lea edi , [edi + eax]'
			
		else:
		
			return ''
		
		
	def solve_var_name(self,name,scope):
	
	
		ns_data = self.name_space.solve_var(name,scope)
		
		print ns_data
		
		if ns_data[0]:
		
			if len(name[1]) == 0:
				return ['	xor eax , eax\n'+'	lea edi , '+self.solve_adress(ns_data)+'	\n' , ns_data[3] ]
			else:
				ret_value = self.solve_indexing(name[1],ns_data[3])
				return [ self.solve_referencing(ns_data,ns_data[3]) + ret_value[0] , ret_value[1] ]
		
		else:
		
			assert False , "Var Not In Scope, FATAL!!! SHOULD BECATCHED BY TYPE CHECKER"
			
	def get_index_arg(self,argu):
	
		if argu == 'pop':
		
			return '	vV_pop ecx	\n'
			
		else:
		
			return '	mov ecx , '+str(argu)+'	\n'
			
	def check_bounds(self,var_type):
	
		i_max = str(var_type.size[0])
		txt = ''
		
		txt += '	cmp ecx , '+i_max+'	\n'
		txt += '	jge vV_bound_error	\n'
			
		return txt
	def calc_offset(self,var_type):
	
		if len(var_type.size) == 1:
		
			size = var_type.content.calc_size()
			
		else:
		
			size = var_type.size[1]
			
		pow2 = [2,4,8,16,32,64,128,256,512,1024,2048,4096]
		
		txt= ''
		txt += '	add eax , ecx	\n'
		
		if size/8.0 in pow2:
							
			txt += "	shl eax , "+str(pow2.index(size/8.0) + 1) +"	\n"
			
		elif size == 1:
		
			pass
			
		else:
		
			txt+= '	mov ecx , '+str(size)+'	\n'
			txt+= '	mul ecx	\n'
			
		return txt
		
	def next_index(self,var_type,argu):
	
	
		txt= ''
		
		txt += self.get_index_arg(argu)
		txt += self.check_bounds(var_type)
		txt += self.calc_offset(var_type)
		
		return txt
		
	def finish_array(self,var_type):
	
		if isinstance(var_type,vV_Var.vV_Ref_Type):
			size = var_type.calc_size()
		else:
			size = var_type.calc_partial_size(1)
		pow2 = [2,4,8,16,32,64,128,256,512,1024,2048,4096]
		txt = ''
		if size in pow2:
							
			txt += "	shl eax , "+str(pow2.index(size) + 1) +"	\n"
			
		elif size == 1:
		
			pass
			
		else:
		
			txt+= '	mov ecx , '+str(size)+'	\n'
			txt+= '	mul ecx	\n'
			
		return txt
			
	def solve_indexing(self,indexes,var_type):
	
	

		txt =''
		txt += '	xor eax , eax	\n'
		working_type = var_type
		
		current = 1
		for i in indexes:
		
			print i
			print working_type.size[0]
			#print'------------------------'
			txt += self.next_index(working_type,i)
			working_type = working_type.get_partial(1)
			print working_type.size
			print'------------------------'
			
			if isinstance(working_type,vV_Var.vV_Ref_Type) and current < len(indexes):
			
				#txt += self.finish_array(working_type)
				txt += '	add edi , eax	\n'
				txt += '	xor eax , eax	\n'
				working_type = working_type.content
				
			while isinstance(working_type,vV_Var.vV_Ref_Type) and current < len(indexes):
		
	
				txt += '	mov edi , [edi]	\n'
				working_type = working_type.content
	
			current += 1
		if isinstance(working_type,vV_Var.vV_Array_Type):
	
			txt += self.finish_array(working_type)
			
		
		return [txt , working_type]
	
	
	
