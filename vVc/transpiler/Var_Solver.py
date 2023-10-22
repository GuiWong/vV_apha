

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
		
	def adress_array_direct(self,var_name,scope):
	
	
		print 'Solving ref Array'
		print var_name
	
		setup = ''	
		pow2 = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096]
		argu = []
		d = len(var_name)
		offset = 0
		
		tmp = self.namespace.solve_var(var_name,scope)
			
		if d > 1:
					
			argu = var_name[1]
			print argu
		
		if tmp[2]:
			
			print "----------------------"
			print tmp[3].size
			i=1
					
			setup += "	xor eax , eax	\n"
			for d in argu:
					
				v=0
						#if d=="pop":
			
				siz = 0
				if i< len(tmp[3].size):
						
					siz = tmp[3].size[i]
							
				else:
						
					siz = tmp[3].content.calc_size()/8
						
				print d
				if d=="pop":
						
					setup += "	vV_pop edi		\n"
					setup += "	cmp edi , "+str(tmp[3].size[i-1])+"		\n"
					setup += "	jge vV_bound_error		\n"				
					setup += "	add eax , edi			\n"
							
				else:
					setup += "	mov edi , "+str(d)+"			\n"
					setup += "	cmp edi , "+str(tmp[3].size[i-1])+"		\n"
					setup += "	jge vV_bound_error		\n"
					setup += "	add eax , edi			\n"
							
							
				if siz in pow2:
							
					setup += "	shl eax , "+str(pow2.index(siz)) +"	\n"
				else:
					setup += "	mov ecx , "+str(siz)+"\n"
					setup += "	mul ecx		\n"
						#setup += " 	add edi , eax				\n"
						#offset += d
					i+=1
						
						
			print "\n\n-----------"
			print tmp[3].dim
			print argu
			if tmp[3].dim != len(argu) and len(argu)!=0:
					
				setup += "	shl eax , 2 \n"
						#assert False, "Unimplemented partial solving, should be catched by TypeChecker"
						
						
			setup += "	mov esi , eax		\n"
			
			setup += "	mov edi , u_global."+tmp[1]+"\n"
						
			adr = "[edi + esi]"
				
				
			return [adr,setup]
					
		else:
				
			assert False, "Locals Array unimplemented"
					
	
		
		
	def adress_array(self,var_name,scope):
	
	
		print 'Solving ref Array'
		print var_name
	
		setup = ''	
		pow2 = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096]
		argu = []
		d = len(var_name)
		offset = 0
		
		tmp = self.namespace.solve_var(var_name,scope)
			
		if d > 1:
					
			argu = var_name[1]
			print argu
		
		if tmp[2]:
			
			print "----------------------"
			print tmp[3].size
			i=1
					
			setup += "	xor eax , eax	\n"
			for d in argu:
					
				v=0
						#if d=="pop":
			
				siz = 0
				if i< len(tmp[3].content.size):
						
					siz = tmp[3].content.size[i]
							
				else:
						
					siz = tmp[3].content.content.calc_size()/8
						
				print d
				if d=="pop":
						
					setup += "	vV_pop edi		\n"
					setup += "	cmp edi , "+str(tmp[3].content.size[i-1])+"		\n"
					setup += "	jge vV_bound_error		\n"				
					setup += "	add eax , edi			\n"
							
				else:
					setup += "	mov edi , "+str(d)+"			\n"
					setup += "	cmp edi , "+str(tmp[3].content.size[i-1])+"		\n"
					setup += "	jge vV_bound_error		\n"
					setup += "	add eax , edi			\n"
							
							
				if siz in pow2:
							
					setup += "	shl eax , "+str(pow2.index(siz)) +"	\n"
				else:
					setup += "	mov ecx , "+str(siz)+"\n"
					setup += "	mul ecx		\n"
						#setup += " 	add edi , eax				\n"
						#offset += d
					i+=1
						
						
			print "\n\n-----------"
			print tmp[3].content.dim
			print argu
			if tmp[3].content.dim != len(argu) and len(argu)!=0:
					
				setup += "	shl eax , 2 \n"
						#assert False, "Unimplemented partial solving, should be catched by TypeChecker"
						
						
			setup += "	mov esi , eax		\n"
			
			setup += "	mov edi , [u_global."+tmp[1]+"]\n"
						
			adr = "[edi + esi]"
				
				
			return [adr,setup]
					
		else:
				
			assert False, "Locals Array unimplemented"
					
	
		
		
		
				
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
			
				
				pow2 = [1,2,4,8,16,32,64,128,256,512,1024,2048,4096]
				argu = []
				d = len(var_name)
				offset = 0
			
				if d > 1:
					
					argu = var_name[1]
					print argu
		
				if tmp[2]:
			
					print "----------------------"
					print tmp[3].size
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
							setup += "	cmp edi , "+str(tmp[3].size[i-1])+"		\n"
							setup += "	jge vV_bound_error		\n"				
							setup += "	add eax , edi			\n"
							
						else:
							setup += "	mov edi , "+str(d)+"			\n"
							setup += "	cmp edi , "+str(tmp[3].size[i-1])+"		\n"
							setup += "	jge vV_bound_error		\n"
							setup += "	add eax , edi			\n"
							
							
						if siz in pow2:
							
							setup += "	shl eax , "+str(pow2.index(siz)) +"	\n"
						else:
							setup += "	mov ecx , "+str(siz)+"\n"
							setup += "	mul ecx		\n"
						#setup += " 	add edi , eax				\n"
						#offset += d
						i+=1
						
						
					print "\n\n-----------"
					print tmp[3].dim
					print argu
					if tmp[3].dim != len(argu) and len(argu)!=0:
					
						setup += "	shl eax , 2 \n"
						#assert False, "Unimplemented partial solving, should be catched by TypeChecker"
						
						
					setup += "	mov esi , eax		\n"
					setup += "	mov edi , u_global."+tmp[1]+"\n"
						
					adr = "[edi + esi]"
					
				else:
				
					assert False, "Locals Array unimplemented"
			
			
			elif isinstance(tmp[3].content,vV_Var.vV_Ref_Type):
			
			
				return self.adress_array_direct(var_name,scope) 
					
			else:
			
				assert False, "Unimplemented type for array"
				
				
				
		elif isinstance(tmp[3],vV_Var.vV_Ref_Type):
		
			print tmp[3].content
			
			if isinstance(tmp[3].content, vV_Var.vV_Int_Type):
			
				return ['[edi]' , "mov edi , [u_global."+tmp[1]+"]\n"]
				
			elif isinstance(tmp[3].content, vV_Var.vV_Array_Type):
			
				if isinstance(tmp[3].content.content, vV_Var.vV_Int_Type):
				
					return self.adress_array(var_name,scope)#['[edi]' , "mov edi , [u_global."+tmp[1]+"]\n"]
					#assert False, "Unimplemented  Array ref"
					
				elif isinstance(tmp[3].content.content, vV_Var.vV_Ref_Type):
				
					assert False, "ERROR  ref to refArray"
				
			else:
			
				assert False, "Unknown or unimplemented Ref Type"
		
				
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
		
		info = self.namespace.solve_var(varname,scope)
		
		print info
		
		print adr
		txt+=adr[1]
		
		if isinstance(info[3],vV_Var.vV_Int_Type):
		
			txt += 'mov eax , '+adr[0]+'\n' 
			txt += 'vV_push eax\n' 
		
			return txt
			
		elif isinstance(info[3],vV_Var.vV_Ref_Type):
		
		
			txt += 'mov eax , '+adr[0]+'\n' 
			#txt += 'mov eax , [ecx]	\n'
			txt += 'vV_push eax\n' 
			
			return txt
			
			
		elif isinstance(info[3],vV_Var.vV_Array_Type):
		
		
			adress = self.adress_array_direct(varname,scope)
			
			txt = adress[1]
			print "\n************************\n"
			print txt
			
			if isinstance(info[3].content,vV_Var.vV_Int_Type):
			
				txt += 'mov eax , '+adr[0]+'\n' 
				txt += 'vV_push eax\n' 
			
				return txt
				
			elif isinstance(info[3].content,vV_Var.vV_Ref_Type):
			
				txt += 'mov ecx , '+adr[0]+'\n' 
				txt += 'mov eax , [ecx]	\n'
				txt += 'vV_push eax\n' 
			
				return txt
				
			
			
			print adress
			
		else:
		
			assert False , "TODO"
		
		
	def pop_var(self,varname,scope):
	
		txt = ''
		
		adr = self.solve_var(varname,scope)
		txt+=adr[1]
		
		
		txt += 'vV_pop eax\n' 
		txt += 'mov '+adr[0]+' , eax\n' 
		
		return txt
		
		
		
	def ref_assign(self,src,dest,scope):
		
		txt = ''
		#print self.namespace.solve_var(dest[0],scope)
		src_type = self.namespace.solve_var(src,scope)
		dest_type = self.namespace.solve_var(dest,scope)
		
		
		print "\n solving ref assignement \n\n"
		print src_type
		print dest_type
		
		
		if isinstance(src_type[3],vV_Var.vV_Int_Type):
		
			if isinstance(dest_type[3],vV_Var.vV_Int_Type):
			
				
				src_adr =  self.solve_var(src,scope)[0]
				dst_adr = self.solve_var(dest,scope)[0]
				
				
				print "\n|\n|"
				print dst_adr
				print "\n|\n|"
				
		
				txt += 'mov eax , '+src_adr+' 	\n'
				txt += 'mov '+dst_adr+' , eax	\n'
				
			elif isinstance(dest_type[3],vV_Var.vV_Ref_Type):
			
				src_adr =  self.solve_var(src,scope)[0]
				dst_adr = self.solve_var(dest,scope)[1].split(',')[1][:-1]
				
				print dst_adr
		
				assert isinstance(dest_type[3].content,vV_Var.vV_Int_Type),"FATAL: Should have been catched by type checks"
				txt += 'mov eax , '+src_adr[1:-1]+' 	\n'
				txt += 'mov '+dst_adr+' , eax	\n'
				
				
			elif isinstance(dest_type[3],vV_Var.vV_Array_Type):
			
				txt = ''
			
				src_adr =  self.solve_var(src,scope)
				dst_adr = self.adress_array_direct(dest,scope)
				
				
				#adress_array
				print src_adr
				print dst_adr
				
				txt += dst_adr[1]

				
				if isinstance(dest_type[3].content,vV_Var.vV_Int_Type):
				
				
					txt +=' mov eax , '+src_adr[0]+'	\n'
					
					
				elif isinstance(dest_type[3].content,vV_Var.vV_Ref_Type):
				
					assert isinstance(dest_type[3].content.content,vV_Var.vV_Int_Type),"FATAL: Should have been catched by type checks"
				
					txt +=' mov eax , '+src_adr[0][1:-1]+'	\n'
					txt +=' mov '+dst_adr[0]+' , eax		\n'
				
				else:
				
					assert False , "FATAL: NOT VALID TYPE"
		
					txt +=' mov eax , '+src_adr[0]+'	\n'
					txt +=' mov '+dst_adr[0]+' , eax		\n'
				
				
			else:
			
				assert False, "Unimplemented"
				
			
			print txt	
			return txt
			
			
		elif isinstance(src_type[3],vV_Var.vV_Array_Type):
		
		
			if isinstance(dest_type[3],vV_Var.vV_Array_Type):
			
				
				txt =''
				
				print src_type[3]
				
				assert src_type[3].content.__class__ == dest_type[3].content.__class__ , "UNIMPLEMENTED YET"
				
				assert src_type[3].calc_partial_size(len(src[1])) == dest_type[3].calc_partial_size(len(dest[1])) , 	"FATAL, Should be checked By Type Checker"
				
				print src_type[3].calc_size() 
				
				#TODO: Cleaner solving of Adress
				
				src_adr =  self.solve_var(src,scope)[1].split(',')[-1]
				dst_adr = self.solve_var(dest,scope)[1].split(',')[-1]
				
				print src_adr[:-1]
				print dst_adr
				
				
				txt+='mov ecx , '+str(src_type[3].calc_size())+' \n'
				txt+='mov rsi , '+src_adr[:-1]+ '	\n'
				txt+='mov rdi , '+dst_adr+'		\n'
				txt+='rep movsb		\n'
				
				
				return txt
				
				
			elif isinstance(dest_type[3],vV_Var.vV_Ref_Type):
			
				
				txt =''
				
				#assert src_type[3].content.__class__ == dest_type[3].content.content.__class__ , "SHOULDBEOK"
				
				
				print src_type[3].calc_partial_size(len(src[1]))
				print dest_type[3].calc_pointed_size()
				
				assert src_type[3].calc_partial_size(len(src[1])) == dest_type[3].calc_pointed_size() ,	"LIMITED FOR NOW"
				
				print src
				
				src_adr =  self.adress_array_direct(src,scope)#[1].split(',')[-1]
				dst_adr = self.solve_var(dest,scope)[1].split(',')[-1]
				
				print src_adr
				print dst_adr
				
				txt+= src_adr[1]
				
				txt+= '	lea eax , '+src_adr[0]+'	\n'
				txt+= '	mov '+dst_adr[:-1]+' , eax	\n'
				
				
				
				return txt
	#mov ecx , %1
	#lea rsi , [vV_sp-cell(%1)]
	#mov rdi , vV_sp
		
	#rep movsd
				
				
		
		
		else:
		
		
			assert False, "Unimplemented"
			
			
			
		
		
		
		
		
		
		



