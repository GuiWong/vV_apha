
import vV_Variable

import vV.VM_Opcode as OP



class Recursive_Dereferencer:


	def __init__(self):
	
		pass
		
		
		
	
		
	def check_ref_ass_valid(self,src,dst,op_w_arg):
	
	
		#print self.__class__
		#print type(src)
		print src , dst
		#print src.__class__ is dst.__class__

		
		if src.__class__ is dst.__class__:
		
			print "Good Type"
			if isinstance(src,vV_Variable.vV_Int_Type):
				
				print "Int: OK"
				return True
		
			if src.content.__class__ is dst.content.__class__:
			
				print "content OK"
				
				print src.calc_partial_size(len(op_w_arg[1][0][1]))
				print dst.calc_partial_size(len(op_w_arg[1][1][1]))
					
				if dst.calc_partial_size(len(op_w_arg[1][1][1])) == src.calc_partial_size(len(op_w_arg[1][0][1])):
					
					print "Same Size, All Ok"
					return True
					
				else:
				
					print "Bad Size"
					return False
			
			
			else:
				print src.content
				print dst.content
				
				#print src.content.content
				
				
				if isinstance(src.content,vV_Variable.vV_Ref_Type):
				
					if src.content.content.__class__ == dst.content.__class__:
					
						assert False , "To implement"
						
					elif src.content.content.__class__ == dst.__class__:
		
		
						print "Source Array Holding ref To valid type"
					
						dim_down = src.dim
					
						sizes= [0,0]
					
						for d in range(dim_down):
					
							sizes[0] += src.size[d]
							sizes[1] += dst.size[d]
						
						
						assert sizes[0] == sizes[1] , "ONLY ALLOW Same Size before referencing"
					
					
						new_src = src.content
						new_dst = dst.get_partial(dim_down)
					
						print new_src , new_dst
					
					
						return self.check_ref_ass_valid(new_src,new_dst,op_w_arg)
					
					
					
					
					
					#return self.check_ref_ass_valid(src.content , dst , op_w_arg)
					
				elif isinstance(dst.content,vV_Variable.vV_Ref_Type) and dst.content.content.__class__ == src.content.__class__:
		
		
					print "Dest Array Holding ref To valid type"
					
					
					
				print "Bad content Type"
				return False
				
		elif isinstance(src,vV_Variable.vV_Ref_Type) and src.content.__class__ == dst.__class__:
		
		
			print " creating data from reference "
			
			
			print src.content.content.__class__
			print dst.__class__
			
			
			return self.check_ref_ass_valid(src.content , dst , op_w_arg)
			
		elif isinstance(dst,vV_Variable.vV_Ref_Type) and dst.content.__class__ == src.__class__:
		
		
			print " creating reference from data  "
			
			#print dst.content.content.__class__
			#print src.__class__
			
			
			return self.check_ref_ass_valid(  src ,dst.content, op_w_arg)
			
			
			#return False
			
		else:
			
			
			if isinstance(dst,vV_Variable.vV_Array_Type) and len(op_w_arg[1][1][1]) > 0:
			
				print "Reducing dest Array"
				new_dst = dst.get_partial(len(op_w_arg[1][1][1]))
				
				
				newop = [op_w_arg[0] ,[ op_w_arg[1][0] , [op_w_arg[1][1][0],[]]]]
				
				print newop
				
				return self.check_ref_ass_valid(src,new_dst,newop)
				
			elif isinstance(src,vV_Variable.vV_Array_Type) and len(op_w_arg[1][0][1]) > 0:
			
				print "Reducing src Array"
				new_src = src.get_partial(len(op_w_arg[1][0][1]))
				
				newop = [op_w_arg[0] , [ [op_w_arg[1][0][0],[]] , op_w_arg[1][1]]]
				
				print newop
				
				return self.check_ref_ass_valid(new_src,dst,op_w_arg)
			
			
			#print isinstance(dst,vV_Variable.vV_Ref_Type)
			print "Bad Type"
			return False
		
			
		
		
		

class Type_Checker:

	
	def __init__(self):
	
		self.dereferencer = Recursive_Dereferencer()
		
		
	def result_type(self,context,vartype,op_w_arg):
	
	
		if context == None:
		
			if isinstance(vartype, vV_Variable.vV_Int_Type):
			
				#print " var is of type int : " + str(vartype)
				
				
				if op_w_arg[0] == OP.PUSH_VAR:
				
					return True
				
				elif op_w_arg[0] == OP.ASSIGN:
				
					return True
					
				else:
				
					assert False ,"Unimplemented Typecheck for "+str(op_w_arg)+ " Opcode"
					
				
			elif isinstance(vartype, vV_Variable.vV_Array_Type):
			
				#print " var is of type array : " + str(vartype)
				
				
				
				if op_w_arg[0] in [OP.PUSH_VAR,OP.ASSIGN]:
				
					#print op_w_arg
					dim = vartype.dim
					#print dim
					dim = dim - len(op_w_arg[1])
					#print dim
					
					
					if dim > 0:
					
						return False
						assert False ,"Trying to Push a non int value"
						
					elif dim < 0 :
					
						return False
						assert False ,"TODO: Check For content type op type result"
						
					return True
					
				else:
				
					assert False ,"Unimplemented Typecheck for "+str(op_w_arg)+ " Opcode"
				
				
				
				
			elif isinstance(vartype, vV_Variable.vV_Ref_Type):
			
				print "TODO: Implement RefType in Translator"
				
				if op_w_arg[0] in [OP.PUSH_VAR,OP.ASSIGN]:
				

					return True
					
				else:
				
					return False
				
			else:
			
				assert False , "unrecognised type : "+str(vartype)
		
		else:
		
			print op_w_arg
			if op_w_arg[0] == OP.REF_ASSIGN:
			
			
				return self.dereferencer.check_ref_ass_valid(context,vartype,op_w_arg)
			
				
				
		#Check <int> = <int>
			
				if isinstance(vartype, vV_Variable.vV_Int_Type) and isinstance(context, vV_Variable.vV_Int_Type):
			
			
					print "int: "
					return True
			
		#Check <Array> = <Array>
			
				elif isinstance(vartype, vV_Variable.vV_Array_Type) and isinstance(context, vV_Variable.vV_Array_Type):
			
					print "array: "
					
					dim = vartype.dim
					dim = dim - len(op_w_arg[1][0][1])
					
					print op_w_arg[1]
					print len(op_w_arg[1][0][1])
					print len(op_w_arg[1][1][1])
					
					
					print vartype.dim
					
					print context.dim
					
					print context.calc_partial_size(len(op_w_arg[1][0][1]))
					print vartype.calc_partial_size(len(op_w_arg[1][1][1]))
					
					if vartype.calc_partial_size(len(op_w_arg[1][1][1])) == context.calc_partial_size(len(op_w_arg[1][0][1])):
					
						print "Same Size"
						
						if type(vartype.content) == type(context.content):
				
							print "good type"
							return True
						else:
						
							print "bad type"
							return False
					
					else:
				
						print "Bad Size"
						return False
					
					
				elif isinstance(vartype , vV_Variable.vV_Ref_Type):
			
			
			
			
					
					assert False, "unimplemented yet"
					return False
		
		
				assert False, "unimplemented yet"




