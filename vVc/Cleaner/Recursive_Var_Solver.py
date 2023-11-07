
import precompiler.VarUpdate.vV_Variable as vV_Var

import Cleaner.Recursive_Type_Checker as R_TC

import copy

import os
import sys
home_path = os.path.expanduser('~') 

sys.path.append(home_path+'/.local/share/vVCompiler/utilities/')

import Logger

def solve_var_namespace(data):
	
	name = data[0]
		
	if '.' in name:
		
		return name.split('.')
			
	else:
		
		return [name,None]

class Var_Op_Solver:

	current_assign= 0

	def __init__(self,namespace):
	
		self.solver = Recursive_Var_Solver(namespace)
		
		
		self.call_data = []
		
	def solve_var_namespace(self,data):
	
		name = data[0]
		
		if '.' in name:
		
			return name.split('.')
			
		else:
		
			return [name,None]
			
	def solve_deref_push(self,data,scope,deref_level = 0):
	
	
	
		deref_level = data[2]
		name,namespace = self.solve_var_namespace(data)
	
		ns_data = self.solver.name_space.solve_var([name],scope,namespace)
		
		
		Logger.log( name			,	10  , Logger.Type.DEBUG)
		Logger.log(  namespace			,	10  , Logger.Type.DEBUG)
		Logger.log(  ns_data[3]		,	10  , Logger.Type.DEBUG)
		Logger.log(  ns_data[3].calc_size()	,	10  , Logger.Type.DEBUG)	
		
		if not ns_data[0]:
			Logger.log( str(data) +' '+ str(scope) +' '+ str(name) +' '+ str(namespace) , 0 , Logger.Type.ERROR, Logger.Flag.DATA)
			
			assert False , 'Couldnt solve var: '+scope
			
		

		
		solved = self.solver.solve_var_name(data,scope)
		
		txt = solved[0]
		var_type = solved[1]	
		
		Logger.log( ' solving var deref push : '+data[0] , 8 , Logger.Type.DEBUG, Logger.Flag.TEXT)
		
		Logger.log( var_type , 8 , Logger.Type.DEBUG, Logger.Flag.DATA)
		
		Logger.log( solved , 8 , Logger.Type.DEBUG, Logger.Flag.DATA)
		

		
		if not isinstance(var_type, vV_Var.vV_Ref_Type):
		
			assert False , "can't deref a value"
			
			
		txt += '	add rdi , rax	\n'
		txt += '	mov eax , [rdi]\n'
		
		while deref_level > 0:
		
			txt+= 	self.make_64_adress(var_type)
			txt+= '	mov eax , [rax]	\n'
			deref_level-= 1
		
		
		txt += '	vV_push eax	'
		
		
		Logger.log( txt , 8 , Logger.Type.DEBUG, Logger.Flag.DATA)
		
		#assert False , 'unimplemented deref op'
		return txt
		

		
				
	def solve_push(self,data,scope):
	
		
		name,namespace = self.solve_var_namespace(data)
	
		ns_data = self.solver.name_space.solve_var([name],scope,namespace)
		
		
		Logger.log( name			,	10  , Logger.Type.DEBUG)
		Logger.log(  namespace			,	10  , Logger.Type.DEBUG)
		Logger.log(  ns_data[3]		,	10  , Logger.Type.DEBUG)
		Logger.log(  ns_data[3].calc_size()	,	10  , Logger.Type.DEBUG)
			
		
		if not ns_data[0]:
			print data
			print scope
			
			print name
			print namespace
			
			print ns_data
			
			print self.solver.name_space.filename
			print self.solver.name_space.imported
			
			print self.solver.name_space.imported[namespace].global_vars
			
			print self.solver.name_space.functions.keys()
			assert False , 'Couldnt solve var: '+scope
		print ns_data[3]
	
		solved = self.solver.solve_var_name(data,scope)
		
		txt = solved[0]
		var_type = solved[1]
		
		print 'solving push:'
		print var_type
		print data[0]
		#print 
		

		txt += '	add rdi , rax	\n'	
		
		
		if isinstance(var_type,vV_Var.vV_Int_Type):
		
			txt += '	mov eax , [rdi]	\n'
			
		elif isinstance(var_type,vV_Var.vV_Byte_Type):
		
			txt += '	mov al , [rdi]	\n'
			
		else:
		
			txt += '	mov eax , [rdi] \n'
		
		while isinstance(var_type,vV_Var.vV_Ref_Type):
			
			print 'is a ref' 
			print var_type.use_offset
			txt += self.make_64_adress(var_type)
			
			
			if isinstance(var_type.content,vV_Var.vV_Byte_Type):
				txt += '	mov rdi , rax	\n'
				txt += '	xor rax , rax	\n'
				txt += '	mov al , [rdi]	\n'
			else:
				txt += '	mov eax , [rax]	\n'
			
			var_type = var_type.content		
		
		#txt += self.make_32_adress(var_type)
		txt += '	vV_push eax	\n'
		
		
		return txt
		
	def solve_pop(self,data,scope):
	
	
		
	
		#ns_data = self.name_space.solve_var(data,scope)
	
		solved = self.solver.solve_var_name(data,scope)
		
		txt = solved[0]
		var_type = solved[1]
		

			
		#txt += '	lea ecx , [edi+eax]	\n'
		txt += '	vV_pop ecx	\n'
		
		txt += '	add rdi , rax	\n'
		#txt += '	lea edi , [rdi]	\n'
		
		txt += '	mov rax , rdi	\n'
		
		last_ref_offset=False
		
		while isinstance(var_type,vV_Var.vV_Ref_Type):
		
			txt += '	mov eax , [rax]	\n'
			#if var_type.use_offset:
			#	assert False, 'Unimplemented'
			txt += self.make_64_adress(var_type)
			
			last_ref_offset = var_type.use_offset
			
			var_type = var_type.content

		
		if isinstance(var_type,vV_Var.vV_Int_Type):
		
			txt += '	mov [rax] , ecx	\n'
			
		elif isinstance(var_type,vV_Var.vV_Byte_Type):
					
			txt += '	mov BYTE[rax] , cl	\n'
			
		
		
		return txt
		
	def solve_assign(self, src , dst , scope , deref = 0):
	
	
		
		src_dat = self.solver.solve_var_name(src,scope)
		dst_dat = self.solver.solve_var_name(dst,scope)
		txt=''
		
		
		deref_max = deref
		
		#original_type
		
		Logger.log('padding')
		
		print src_dat
		print dst_dat
		
		if isinstance(dst_dat[1],vV_Var.vV_Ref_Type):
		
			Logger.log( str(dst_dat[1].use_offset) )
		
		print src_dat[1].calc_size()/8
		print dst_dat[1].calc_size()/8
		
		
		
		
		
		
		#is already redued!!!!
		#if isinstance(src_dat[1],vV_Var.vV_Int_Type): 
		
		
		if dst[0] == 'vV_PUSH_ARG':
		
			dst[1].use_offset=self.check_src_offset(src,scope)
			#self.call_data.append(self.check_src_offset(src,scope))
			#assert False, 'Breakpoint'
		else:
		
			if deref == 0:
				self.check_offset_adress( src , dst , scope,src_dat,dst_dat , deref)
			else:
				final_dst = dst_dat[1]
				while deref > 0:
				 	
				 	
				 	final_dst = final_dst.content
				 	deref -= 1
				 	
				 	
				 	
				final_dst_array = ['',final_dst]
				#final_dst_array[1] = final_dst
				
				#dst_dat[1] = final_dst
				 	
				self.check_offset_adress( src , dst , scope,src_dat,final_dst_array)
		
		
		if isinstance(dst_dat[1],vV_Var.vV_Ref_Type):
		
			Logger.log( str(dst_dat[1].use_offset) )			
		

		txt+=src_dat[0]
		#txt += '	lea esi , [edi+eax]	\n'
		txt += '	mov rsi , rdi	\n'
		txt += '	add rsi , rax	\n'
		
		
		
		derefed = 0
		new_dst = dst_dat[1]
		
		if dst[0]=='vV_PUSH_ARG':
			
			
			txt += '	push rax	\n'
			txt += '	mov rdi , rsp	\n'
			txt += self.recursive_assignator(src_dat[1],dst_dat[1])
			#txt += '	mov rax , rsi	\n'
			#txt += self.make_32_adress(dst[1])
			#txt += '	push rax	\n'
		else:
			txt += dst_dat[0]
			
			
			txt += '	add rdi , rax	\n'
			
			
			if deref_max > 0:
				txt += '	mov rax , rdi	\n'
			while derefed < deref_max:
			
			
				print '\n--'
				print new_dst.use_offset
				#assert False , 'BP'
			
				
				txt += '	mov eax , [rax]	\n'	
				txt += self.make_64_adress(new_dst)
				
				new_dst = new_dst.content
				#new_dst = new_dst.content
				derefed += 1
			if deref_max > 0:
				txt += '	mov rdi , rax	\n'	
			#txt += '	mov rdi , rax	\n'
			
			
			if deref_max > 0:
			
				txt += self.recursive_assignator(src_dat[1],final_dst)
			
			else:
			
				txt += self.recursive_assignator(src_dat[1],new_dst)
			
		self.current_assign+=1
		
		
		#if dst[0] == 'ptr':
		
		#	print '\n\n'
		#	print txt
		#	print '\n\n'
		#	assert False ,'breakpoint'
		return txt
			
		
		
	#def recursive_offset_adresser(self,)
	
	
	def check_src_offset(self,src,scope):
	
		print '\n '+str(src)+'\n'
		name , namespace = solve_var_namespace(src)
		print name
		print namespace
		src_data = self.solver.name_space.solve_var([name,[]],scope,namespace)
		src_dat = self.solver.solve_var_name(src,scope)
		
		if not src_data[2]:
			
			if isinstance(src_data[3],vV_Var.vV_Ref_Type) or isinstance(src_data[3],vV_Var.vV_Int_Type):
			
				return True
				
			elif isinstance (src_data[3],vV_Var.vV_Array_Type):
			
				assert False, 'Need to implement local Arrays'
				
		return False
		
	def check_offset_adress(self,src,dst,scope , src_dat , dst_dat, deref = 0):
	
	
		src_name, src_namespace = solve_var_namespace(src)
		dst_name, dst_namespace = solve_var_namespace(dst)
		
		print src_name
		print dst_name
	
		src_data = self.solver.name_space.solve_var([src_name],scope,src_namespace)
		dst_data = self.solver.name_space.solve_var([dst_name],scope,dst_namespace)
		
		
		print '\n dst: '
		print dst
		print dst_data
		print dst_data[3].calc_size() / 8
		print '---'
		print src
		print src_data
		print src_dat
		#src_dat = self.solver.solve_var_name(src,scope)
		#dst_dat = self.solver.solve_var_name(dst,scope)
		print dst_data
		offseted = False
		
		#assert False , 'Break'
		
		if not src_data[2]:
			
			if isinstance(src_data[3],vV_Var.vV_Ref_Type) or isinstance(src_data[3],vV_Var.vV_Int_Type):
			
				offseted=True
				
			elif isinstance (src_data[3],vV_Var.vV_Array_Type):
			
				assert False, 'Need to implement local Arrays'
				
			
			
		
		
		if isinstance(dst_dat[1],vV_Var.vV_Ref_Type):
		
			print 'Found a ref creation'
			#print dst_data
			print offseted
			print dst
			if dst_data[2]:
			
				self.solver.name_space.global_vars[dst_data[1]].var_type.use_offset=offseted
			
			else:
			
				if dst[0] == 'vV_PUSH_ARG':
				
					print dst[1]
					
					
				elif dst[0] in self.solver.name_space.functions[scope].local_vars.keys():
				
					#self.solver.name_space.functions[scope].local_vars[dst[0]].var_type.use_offset=offseted
					print offseted
					dst_dat[1].use_offset=offseted
					print self.solver.name_space.functions[scope].local_vars[dst[0]].var_type.use_offset
					#print self.solver.name_space.functions[scope].local_vars[dst[0]].var_type.content.use_offset
					#print  self.solver.name_space.functions[scope].local_vars[dst[0]]
					
					#print self.solver.name_space.functions[scope].local_vars[dst[0]].var_type
					
					#print dst_dat[1]
					print  self.solver.name_space.functions[scope].local_vars[dst[0]].var_type.use_offset
					
					#assert False, "Breakpoint"
				
				elif dst[0] in self.solver.name_space.functions[scope].referenced_vars.keys():
				
					self.solver.name_space.functions[scope].referenced_vars[dst[0]].var_type.use_offset=offseted
					
				else:
				
					assert False, "FATAL, couldn't solve var path : " +dst_data[1]+' - '+scope
					
			print 'Var offset should be updated'
			
			if isinstance(dst_dat[1].content,vV_Var.vV_Ref_Type):
			
				print 'ref of ref creation'
				
				offseted = src_dat[1].use_offset
			
				if dst_data[2]:
			
					self.solver.name_space.global_vars[dst_data[1]].var_type.content.use_offset=offseted
			
				else:
			
					if dst[0] in self.solver.name_space.functions[scope].local_vars.keys():
				
						self.solver.name_space.functions[scope].local_vars[dst[0]].var_type.content.use_offset=offseted
					 
						print  self.solver.name_space.functions[scope].local_vars[dst[0]].var_type.content
						print self.solver.name_space.functions[scope].local_vars[dst[0]].var_type.content
						print  self.solver.name_space.functions[scope].local_vars[dst[0]].var_type.content.use_offset
				
					elif dst[0] in self.solver.name_space.functions[scope].referenced_vars.keys():
				
						self.solver.name_space.functions[scope].referenced_vars[dst[0]].var_type.content.use_offset=offseted
					
					else:
				
						assert False, "FATAL, couldn't solve var path : " +dst_data[1]+' - '+scope
					
				
			
	def check_signature(self,src_type,dst_type):
	
		check = False
		
		
		
		if src_type.__class__ == dst_type.__class__:
		
			if isinstance(src_type,vV_Var.vV_Array_Type):
				
				if src_type.get_total_elem() == dst_type.get_total_elem():
					
						return self.check_signature(src_type.content,dst_type.content)
						
			elif isinstance(src_type,vV_Var.vV_Ref_Type):
			
				return self.check_signature(src_type.content,dst_type.content)
				
			elif isinstance(src_type,vV_Var.vV_Int_Type):
			
				return True
				
			elif isinstance(src_type,vV_Var.vV_Byte_Type):
			
				return True
				
		#elif isinstance(dst_type,vV_Var.vV_Ref_Type):
		
		#	return self.check_signature(src_type,dst_type.content)
			
		else:
		
		
			if isinstance(src_type,vV_Var.vV_Int_Type):
			
				if isinstance(dst_type,vV_Var.vV_Byte_Type):
				
					return True
			return False
			
	def reduce_array(self,arr_type,size):
	
	
		current_size = arr_type.get_total_elem()
		remaining_size = current_size / size
		
		assert current_size % size == 0 , "FATAL: can't cast array"
		
		if remaining_size == 1:
		
			return arr_type.content
		else:
		
			return vV_Var.vV_Array_Type(arr_type.content,1,[remaining_size])
 		
		
	def recursive_assignator(self,src_type,dst_type,loop_level=0):
	
	
		print '-----------------------------------'
		print src_type
		print dst_type
	
		if src_type.__class__ == dst_type.__class__:
		
			if isinstance(src_type,vV_Var.vV_Array_Type):
			
			
				if src_type.content.__class__ == dst_type.content.__class__:
				
					
					if src_type.calc_size() == dst_type.calc_size():
					
						txt = '	mov ecx , '+str(src_type.calc_size() / 8)+'	\n'
						txt += '	rep movsb	\n'
						return txt
						
					else:
					
						assert False , "TODO: Catch this on type check level"
										
				else:
				
					if isinstance(dst_type.content,vV_Var.vV_Ref_Type):
					
						size = dst_type.get_total_elem()
						
						print size
						print src_type.size
						
						new_src = self.reduce_array(src_type,size)
						dst_data_size = dst_type.content.calc_size() / 8
						src_data_size = new_src.calc_size() / 8
						
						print dst_data_size
						print src_data_size
						print new_src.size
						if self.check_signature(new_src,dst_type.content.content):
						
							txt= '	mov r8 , rsp	\n'
							txt+= '	push rsi 	\n'
							txt+= '	push rdi	\n'
							
							txt+= '	xor ecx , ecx	\n'
							txt+= 'loop_assign_'+str(self.current_assign)+'_'+str(loop_level)+':	\n' 
							
							txt+='	mov eax , ecx	\n'
							txt+='	mov edx , '+str(dst_data_size)+'	\n'
							txt+='	mul edx	\n'
							
							txt+='	mov rsi , [r8 - 8]	\n'					#Arrays are ALWAYS direct adressed??
							txt+='	add rsi , rax	\n'
							txt+='	mov rdi , [r8 -16]	\n'
							txt+='	lea edi , [edi + ecx * '+str(dst_data_size)+']	\n'
							
							
							closetxt = '	inc ecx	\n'
							closetxt +='	cmp ecx , '+str(size)+'	\n'
							closetxt +='	jb '+'loop_assign_'+str(self.current_assign)+'_'+str(loop_level)+'	\n'
							closetxt +='	add rsp , 16	\n'
							
							loop_level += 1
							
							return txt + self.recursive_assignator(new_src,dst_type.content,loop_level) + closetxt
					
						else:
							
							print new_src
							print dst_type.content
							#print new_src
							#print new_src.calc_size()
							#print dst_type.content
							assert False , "BAD SIGNATURE"		
				
				
					elif isinstance(src_type.content,vV_Var.vV_Ref_Type):
					
						assert False , "TODO: Implement Array Deref"
						
					elif isinstance(src_type.content,vV_Var.vV_Int_Type):
					
						if isinstance(dst_type.content,vV_Var.vV_Byte_Type):
						
							assert False , 'unimplemented int to byte array'
					
					elif isinstance(src_type.content,vV_Var.vV_Byte_Type):
					
						if isinstance(dst_type.content,vV_Var.vV_Int_Type):
						
							assert False , 'unimplemented byte to int array'
					
					else:
					
						assert False , 'unimplemented'
						
						
			else:
			
				if isinstance(src_type,vV_Var.vV_Ref_Type):
				
					if self.check_signature(src_type.content,dst_type.content):
					
						#if src_type.use_offset:
						
						#	assert False , 'Unimplemented'
						
						dst_type.use_offset = src_type.use_offset
					
						return '	mov eax , [rsi]	\n	mov DWORD[rdi] , eax	\n'
						
					elif self.check_signature(src_type,dst_type.content):
					
						#dst_type.content.use_offset = src_type.use_offset
						txt = ''
						
						txt += '	mov rax , rsi	\n' 
						txt += self.make_32_adress(dst_type)
						
						
						#if isinstance(dst_type.content,vV_Var.vV_Ref_Type):
						
						#	txt += '	mov edi , [rdi]	\n'
						#	txt += self.make_64_adress(dst_type.content)
						
		
						txt += '	mov [rdi] , eax	\n'
						txt 
						#if src_type.use_offset:
							
						#	print txt
						#	assert False , 'unimplemented'
							
						return txt
						
					else:
						print src_type.content
						print dst_type
						print '\n\n\n I dont understand this????\n\n\n'
						return '	mov eax , [rsi]	\n	mov DWORD[rdi] , eax	\n'+self.recursive_assignator(src_type.content,dst_type,loop_level)
					
				elif isinstance(src_type,vV_Var.vV_Int_Type):
				
					return '	mov eax , [rsi]	\n	mov DWORD[rdi] , eax	\n'
					
				elif isinstance(src_type,vV_Var.vV_Byte_Type):
				
					return '	mov al , [rsi]	\n	mov BYTE[rdi] ,al	\n'
					
					
				#if is_instance(dst_type)
			
		else:
		
			if isinstance(dst_type,vV_Var.vV_Ref_Type) and self.check_signature(src_type,dst_type.content):
			
			
				print '\n\nRef Creation:'
				print dst_type.use_offset
				
				#dst_type.use_offset
				txt = ''
				txt += '	mov  rax , rsi	\n'
				
				txt += self.make_32_adress(dst_type)
				
				txt += '	mov [rdi] , eax	\n'
				#if src_type.use_offset:
							
				#	Offset Set before
							
				return txt
				
			else:
			
				print'-----------'
				print src_type
				print src_type.dim
				print src_type.size
				print src_type.content
				print src_type.content.calc_size()
				print src_type.calc_size()
				print dst_type.content.calc_size()
				#print dst_type.content.calc_size()
				print'-----------'
				
			if isinstance(src_type,vV_Var.vV_Ref_Type):
			
				
				txt = ''
				txt += '	mov DWORD eax , [rsi]	\n'
				
				txt += self.make_64_adress(src_type)
				
				txt += '	mov rsi , rax	\n'
			
				return txt + self.recursive_assignator(src_type.content,dst_type,loop_level)
			
			
			if isinstance(src_type,vV_Var.vV_Int_Type):
			
				if isinstance(dst_type,vV_Var.vV_Byte_Type):
				
					txt = '	mov eax , [rsi]	\n'	
					txt += '	and rax , 0xff		\n'
					txt += ' 	mov BYTE[rdi] , al	\n'
					return txt
					
			if isinstance(src_type,vV_Var.vV_Byte_Type):
			
				if isinstance(dst_type,vV_Var.vV_Int_Type):
				
					txt = '	xor rax , rax		\n'
					txt += '	mov BYTE al , [rsi]	\n'	
					txt += ' 	mov DWORD[rdi] , eax	\n'
					return txt
					
			print src_type
			print dst_type
			print dst_type.content
			
			assert False, 'unreachable'
				
	def make_64_adress(self,ref_type):
	
		txt = ''
		if ref_type.use_offset:


			txt += '	add rax , [vV_local_offset]	\n'
			
		return txt
			
	def make_32_adress(self,ref_type):
	
		txt= ''
		if ref_type.use_offset:
		
			txt += '	sub rax , [vV_local_offset]	\n'
			
		return txt
				
				
class Recursive_Var_Solver:


	txt = ''

	def __init__(self,namespace):
	
		self.name_space = namespace
		
	def add_namespace(self,namespace):
	
		print self.name_space.internal_filename
	
		if namespace == None or (self.name_space.is_main and namespace == self.name_space.internal_filename):
		
			return ''
			
		elif namespace == self.name_space.internal_filename :
		
			return '_'+namespace
		else:
		
			txt = self.name_space.imported[namespace].internal_filename
			return '_'+txt
			#assert False , 'Breakpoint'
		
		
	def solve_adress(self,data,namespace=None):
	
	
		if data[2]:
		
		
			ns_txt = self.add_namespace(namespace)
			if self.name_space.is_var_init(data[1],namespace):
			#if self.name_space.global_vars[data[1]].is_init:
			
				adr = "[i_global"+ns_txt+"."+data[1] +']'
				
			else:
			
				adr = "[u_global"+ns_txt+"."+data[1] +']'
					
		else:
			
			adr = data[1]
			
		return adr
		
		
	def solve_referencing(self,data,var_type,namespace = None):
	
		
		if isinstance(var_type,vV_Var.vV_Ref_Type):
		
			return self.solve_referencing(data,var_type.content,namespace) + '	mov edi , [rdi]	\n'
			
		else:
		
			return '	lea rdi , '+self.solve_adress(data,namespace)+'	\n'
			
			
		
	def indexed_referencing(self,var_type):
	
		
		if isinstance(var_type,vV_Var.vV_Ref_Type):
		
			return '	lea edi , [edi + eax]'
			
		else:
		
			return ''
		
		
	def solve_var_name(self,name,scope):
	
	
		
		varname , namespace = solve_var_namespace(name)
		
		effective_namespace = self.name_space.internal_filename
		
		if namespace != None:
		
			effective_namespace = namespace
		
		#name[0] = varname
		vardata = name[1:]
		
		
	
	
		ns_data = self.name_space.solve_var([varname,vardata],scope,namespace)
		
		print ns_data
		print name
		
		if ns_data[0]:
		
			if name[0] == 'vV_PUSH_ARG':
			
				return ['' , name[1]]
				
			elif len(name[1]) == 0:
				return ['	xor rax , rax\n'+'	lea rdi , '+self.solve_adress(ns_data,effective_namespace)+'	\n' , ns_data[3] ]
			else:
				
				ret_value = self.solve_indexing(name[1],ns_data[3])
				return [ self.solve_referencing(ns_data,ns_data[3],effective_namespace) + ret_value[0] , ret_value[1] ]
		
		else:
		
			print '\n\n\n Scope Error:'
			print self.name_space.filename
			print scope
			print self.name_space.global_vars.keys()
			print self.name_space.functions.keys()
			print name
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
		
			size = var_type.content.calc_size() / 8
			
		else:
		
			size = var_type.size[1]
			
			
		if isinstance(var_type,vV_Var.vV_Iterator_Type):
		
			size = var_type.calc_size() / 8
			
		pow2 = [2,4,8,16,32,64,128,256,512,1024,2048,4096]
		
		txt= ''
		txt += '	add eax , ecx	\n'
		
		if size in pow2:
							
			txt += "	shl eax , "+str(pow2.index(size) + 1) +"	\n"
			
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
			size = var_type.calc_size() / 8
		else:
			size = var_type.calc_partial_size(1) / 8
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
		txt += '	xor rax , rax	\n'
		working_type = var_type.copy()
		
		
		while isinstance(working_type,vV_Var.vV_Ref_Type):
		
			working_type = working_type.content
		
		current = 1
		#stop
		for i in indexes:
		
			print i
			
			if type(i)==str and ':' in i:
			
				if current < len(indexes):
					assert False , 'Misplaced Array Reducing'
				else:
					#print R_TC.solve_from_to_arg(i)
					
					bounds_indexes = R_TC.solve_from_to_arg(i)
					
					start_indx = bounds_indexes[0]
					
					if start_indx == None:
					
						start_indx = 0
					
					txt += self.next_index(working_type,start_indx)
					
					working_type = working_type.get_from_to(bounds_indexes[0],bounds_indexes[1])
					print working_type
					print working_type.get_total_elem()
					#assert False , 'unimplemented array reducing op : '+str(i)
			
			else:
				txt += self.next_index(working_type,i)
				working_type = working_type.get_partial(1)

			
			if isinstance(working_type,vV_Var.vV_Ref_Type) and current < len(indexes):
			
				#txt += self.finish_array(working_type)
				txt += '	add edi , eax	\n'
				txt += '	xor rax , rax	\n'
				working_type = working_type.content
				
			while isinstance(working_type,vV_Var.vV_Ref_Type) and current < len(indexes):
		
	
				txt += '	mov edi , [edi]	\n'
				working_type = working_type.content
	
			current += 1
		if isinstance(working_type,vV_Var.vV_Array_Type):
	
			#txt += 'HERE'
			txt += self.finish_array(working_type)
			
		
		return [txt , working_type]
	
	
	
