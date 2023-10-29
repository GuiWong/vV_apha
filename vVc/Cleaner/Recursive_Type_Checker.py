

import vV.VM_Opcode as OP

import precompiler.VarUpdate.vV_Variable as vV_Var


def calc_effective_type(type_a,argus):

	print argus
	#assert isinstance(type_a , vV_Var.vV_Array_Type) , "ERROR, SHOULDN't solve non-Array"
	if isinstance(type_a , vV_Var.vV_Array_Type):
	
		return type_a.get_partial(len(argus))
		
	elif isinstance(type_a , vV_Var.vV_Ref_Type):
	
		return calc_effective_type(type_a.content,argus)
		
	else:
	
		return type_a
		
def reduce_array(array,parts,dim):

	#partial_size = 
	#for d in range(dim):
	pass
		
	
	

def check_valid(type_b,type_a):


	print 'checking type'
	print type_a
	print type_b
	
	if type_a.__class__ == type_b.__class__:
	
		content_check = False
		
		if type_a.__class__ in [vV_Var.vV_Int_Type]:
		
			print "Both Are Ints"
			content_check = True
			
		if (not content_check) and type_a.content.__class__ == type_b.content.__class__:
		
			content_check = True
			
			
		if content_check:
		
			if type_a.calc_size() == type_b.calc_size():
			
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
				
				if type_a.get_partial(dimdown).__class__ == type_b.content.__class__:
					if (type_a.get_partial(dimdown).__class__ == vV_Var.vV_Int_Type):
							return True
					else:
						if type_a.get_partial(dimdown).calc_size() == type_b.content.calc_size():
						
							if type_a.get_partial(dimdown).content.__class__ == type_b.content.content.__class__:
						
								return True
								
				print 'Cant create Ref from not matching data !'
				return False
				
				
				#return check_valid(type_a.get_partial(dimdown),type_b.content)		Forbidden for dest
			
			else:
			
				
			
				return False
	
	else:


		if type_a.__class__ == vV_Var.vV_Ref_Type:
			
				print "One is a ref"
				
				#dimdown = type_a.dim
				#print dimdown
				
				return check_valid(type_a.content,type_b)
				
		elif type_b.__class__ == vV_Var.vV_Ref_Type:
		
				print "One is a ref"
				return check_valid(type_a,type_b.content)
		

