

import vV.VM_Opcode as OP

import precompiler.VarUpdate.vV_Variable as vV_Var


def solve_from_to_arg(arg):

	data = arg.split(':')
	
	print data
	
	assert len(data) == 2 ,"array cutting can't have more than 2 args"
	
	for i in range(len(data)):
	
		if data[i] == '':
		
			data[i] = None
		
		else:
		
			data[i] = int(data[i])
	
		print type(data[i])	
		
	
	return data
	assert False , 'unimplemented'


def calc_effective_type(type_a,argus):

	print argus
	#assert isinstance(type_a , vV_Var.vV_Array_Type) , "ERROR, SHOULDN't solve non-Array"
	if isinstance(type_a , vV_Var.vV_Array_Type):
	
		for argu in argus[1:]:
			#print argu
			assert type(argu)!=str or ':' not in argu , 'Unimplemented partial array indexing'
		
		reduce_value = len(argus)
			
		if reduce_value > 0 and type(argus[0])==str and ':' in argus[0]:
		
			reduce_value -=1
			f_t_arg = solve_from_to_arg(argus[0])
			print f_t_arg
			ret_data = type_a.get_partial(reduce_value).get_from_to(f_t_arg[0],f_t_arg[1])
			return ret_data
		
		return type_a.get_partial(reduce_value)
		
	elif isinstance(type_a , vV_Var.vV_Ref_Type):
	
		return calc_effective_type(type_a.content,argus)
		
	else:
	
		return type_a
		
def reduce_array(array,parts,dim):

	#partial_size = 
	#for d in range(dim):
	pass
		
	
	

def check_valid(type_b,type_a,dest_derefed = False):


	print 'checking type'
	print type_a
	print type_b
	
	if type_a.__class__ == type_b.__class__:
	
		content_check = False
		
		if type_a.__class__ in [vV_Var.vV_Int_Type]:
		
			print "Both Are Ints"
			content_check = True
			
			return True
		if type_a.__class__ in [vV_Var.vV_Byte_Type]:
		
			print "Both Are Byte"
			content_check = True
			
			return True
			
			
		if (not content_check) and type_a.content.__class__ == type_b.content.__class__:
		
			content_check = True
			
			
		if content_check:
		
			if type_a.get_total_elem() == type_b.get_total_elem():
			
				print 'Same Array Size'
				return True
			
		else:
		
			print 'bad content : '
			print type_a.content
			print type_b.content
			
			if type_a.content.__class__ == vV_Var.vV_Ref_Type:
			
				print "One is a ref"
				
				dimdown = type_a.dim
				print dimdown
				
				for d in range(dimdown):
				
					if type_b.size[d] != type_a.size[d]:
					
						print 'BAD Base Size '
						return False
				
				print 'Good Base Size '
				
				return check_valid(type_a.content,type_b.get_partial(dimdown))
				
			elif type_b.content.__class__ == vV_Var.vV_Ref_Type:
			
				print "One is a ref"
				
				dimdown = type_b.dim
				print dimdown
				
				for d in range(dimdown):
				
					if type_b.size[d] != type_a.size[d]:
					
						print 'BAD Base Size '
						return False
				
				print 'Good Base Size '
				
				if type_a.get_partial(dimdown).__class__ == type_b.content.content.__class__:
				
				
					if (type_a.get_partial(dimdown).__class__ == vV_Var.vV_Int_Type):
							return True
					else:
						if type_a.get_partial(dimdown).get_total_elem() == type_b.content.get_total_elem():
						
							if type_a.get_partial(dimdown).content.__class__ == type_b.content.content.__class__:
						
								return True
								
				print 'Cant create Ref from not matching data !'
				return False
				
				
				#return check_valid(type_a.get_partial(dimdown),type_b.content)		Forbidden for dest
			
			else:
			
				
				if isinstance(type_a.content,vV_Var.vV_Int_Type):
				
					if isinstance(type_b.content,vV_Var.vV_Byte_Type):
					
						return True
				
				if isinstance(type_a.content,vV_Var.vV_Byte_Type):
				
					if isinstance(type_b.content,vV_Var.vV_Int_Type):
					
						return True
				
				print 'unpossible cast for array content: '+str(type_a.content)+' to '+str(type_b.content)
				return False
	
	else:
	
		if type_a.__class__ == vV_Var.vV_Int_Type and type_b.__class__ == vV_Var.vV_Byte_Type:
		
			print 'int to byte casting'
			return True
			
		elif type_a.__class__ == vV_Var.vV_Byte_Type and type_b.__class__ == vV_Var.vV_Int_Type:
		
			print 'byte to int casting'
			
			
			if dest_derefed:
			
				print 'Unvalid <int> ref creation from <Byte> data'
				
				return False
				
			else:
			
				return True


		if type_a.__class__ == vV_Var.vV_Ref_Type:
			
				print "One is a ref"
				
				#dimdown = type_a.dim
				#print dimdown
				
				return check_valid(type_a.content,type_b,dest_derefed)
				
		elif type_b.__class__ == vV_Var.vV_Ref_Type:
		
				print "One is a ref"
				return check_valid(type_a,type_b.content,True)
		

