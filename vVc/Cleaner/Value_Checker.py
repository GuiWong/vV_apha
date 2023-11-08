
import vV.VM_Opcode as OP
import precompiler.VarUpdate.vV_Variable as vV_Var 

import os
import sys
home_path = os.path.expanduser('~') 

sys.path.append(home_path+'/.local/share/vVCompiler/utilities/')

import Logger
import copy


class Array_Initializer:


	def __init__(self):
	
	
		pass
		
	def reset_values(self):
	
	
		self.output=[]
		self.size=[]
		self.dim = 0
		
		self.current_size = []
		self.current_dim = 0
		
		self.size_is_init = []
		
		
	def init_sizes(self):
	
		for s in self.size:
		
			self.size_is_init.append(True)
			self.current_size.append(0)
	
		
		
	def read_value_before_close(self,tok,v_type=None):
	
		cop = tok
		
		while cop[-1] == ']':
		
			cop = cop[:-1]
			
		return check_for_valid_value(cop,v_type)
		
		
	def check_array_value(self,tok,var_type):
	
		if var_type == None:
		
			return self.check_untyped_array_value(tok)
	
		if not isinstance(var_type,vV_Var.vV_Array_Type):
		
			Logger.log('Bad Type for Array Value',  2 , Logger.Type.WARNING , Logger.Flag.TEXT)
			Logger.log(str(var_type),  2 , Logger.Type.WARNING , Logger.Flag.TEXT)
			return [False,[]]
			
		
			
		else:
		
			return self.check_typed_array_value(tok,var_type)
		
		
	def check_typed_array_value(self,tok,var_type):
	
		self.reset_values()
		self.size=var_type.size
		self.dim = var_type.dim
		
		cutted = tok.split(',')
		Logger.log(str(cutted),  12 , Logger.Type.DEBUG , Logger.Flag.DATA)
		
		current_deepness = 0
		
		self.init_sizes()
		
		
		for val in cutted:
		
			tmp = val
			while tmp[0] == '[':
			
				current_deepness += 1
				tmp = tmp[1:]
				
				if current_deepness > self.size_is_init:
				
					self.size_is_init.append(False)
					self.current_size.append(0)
					assert False , 'UNREACHABLE'
				
				
			valu = self.read_value_before_close(tmp,var_type.content)
			
			if not valu[0]:
				Logger.log('Error decoding value in array initialisation',  2 , Logger.Type.WARNING , Logger.Flag.TEXT)
				Logger.log(val,  2 , Logger.Type.WARNING , Logger.Flag.DATA)
				return [False,[]]
				
			if not can_cast_to(valu[2],var_type.content,valu[1]):
				
				Logger.log('Error casting value in array initialisation',  2 , Logger.Type.WARNING , Logger.Flag.TEXT)
				Logger.log(val,  2 , Logger.Type.WARNING , Logger.Flag.DATA)
				Logger.log(str(valu[1])+ ' to ' + str(var_type.content),  2 , Logger.Type.WARNING , Logger.Flag.DATA)
				return [False,[]]
				
				
			self.current_size[current_deepness-1]+=1
			
			
			
			while tmp[-1] == ']':
			
				
				
				if not self.current_size[current_deepness-1] == self.size[current_deepness-1]:
				
					
					Logger.log('Error : Size of array not matching size of var',  2 , Logger.Type.ERROR , Logger.Flag.TEXT)
					Logger.log(self.size,  4 , Logger.Type.DEBUG , Logger.Flag.DATA)
					Logger.log(self.current_size,  4 , Logger.Type.DEBUG , Logger.Flag.DATA)
					Logger.log(str(cutted),  4 , Logger.Type.DEBUG , Logger.Flag.DATA)
					return [False,[]]
					
				self.current_size[current_deepness-1] = 0
					
				current_deepness -= 1
				tmp = tmp[:-1]	
				
				self.current_size[current_deepness-1]+=1
			
			
				
			self.output.append(valu[1])
			
		
		Logger.log(str(self.output),  8 , Logger.Type.DEBUG , Logger.Flag.DATA)
		
		ret = copy.copy(self.output)
		return [True,ret,var_type.content]
		
		assert False , 'Unimplemented'
			
		
	def check_untyped_array_value(self,tok):
		
		self.reset_values()
		
		cutted = tok.split(',')
		Logger.log(str(cutted),  12 , Logger.Type.DEBUG , Logger.Flag.DATA)
		
		assert False , 'Unimplemented'
		
def can_cast_to(src_t,dst_t,value):

	if src_t.__class__ == dst_t.__class__:
	
		return True
		
	if isinstance(src_t,vV_Var.vV_Byte_Type):
	
		if isinstance(dst_t,vV_Var.vV_Int_Type):
		
			return True
			
	if isinstance(src_t,vV_Var.vV_Int_Type):
	
		if isinstance(dst_t,vV_Var.vV_Byte_Type):
		
			if value < 256:
			
				return True
				
			else:
			
				Logger.log("Can't cast value to byte :"+ str(value) ,  0 , Logger.Type.ERROR , Logger.Flag.TEXT)
				
	return False
			

def check_for_valid_value(txt,var_type=None):


	ret = check_for_value(txt,var_type)
	
	Logger.log(str(ret), 6 , Logger.Type.DEBUG , Logger.Flag.DATA)
	
	if not ret[0]:
	 
		return ret
	
	if ret[2] == OP.STR_LITERAL:
	
	
		ret[1] = [ret[1] ,OP.STR_LITERAL ]
			
		if var_type == None:
		
			ret[2] = vV_Var.vV_Array_Type(vV_Var.vV_Byte_Type,1,[len(ret[1][0])])
			
			#ret[1] = [ret[1] ,OP.STR_LITERAL ]
			return ret
			
		elif isinstance(var_type,vV_Var.vV_Array_Type):
		
			if var_type.dim == 1:
			
				if var_type.size[0] == len(ret[1][0]):
			
					if isinstance(var_type.content,vV_Var.vV_Byte_Type):
			
						ret[2] = var_type
						return ret
				
					else:
					
						logtxt='Bad Type for array initialisation from string literal'
						Logger.log(logtxt,  0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
						assert False , 'TODO: Redo error handeling'
						
						
				elif var_type.size[0] == '':
				
					var_type.size[0] = len(ret[1][0])
					
					if isinstance(var_type.content,vV_Var.vV_Byte_Type):
			
						ret[2] = var_type
						return ret
				
					else:
					
						logtxt='Bad Type for array initialisation from string literal'
						Logger.log(logtxt,  0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
						assert False , 'TODO: Redo error handeling'

				
				else:
				
					logtxt='Bad Size for array initialisation from string literal'
					Logger.log(logtxt,  0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
					assert False , 'TODO: Redo error handeling'
				
			else:
				logtxt='Bad Dimention for array initialisation from string literal'
				Logger.log(logtxt,  0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
				assert False , 'TODO: Redo error handeling'
				
		else:
		
			logtxt='Bad Type for initialisation from string literal'
			Logger.log(logtxt,  0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
			assert False , 'TODO: Redo error handeling'
				
		
	elif ret[2].__class__ == var_type.__class__:
	
		
		return ret
		
		
	elif var_type == None:
	
		return ret
		
	elif can_cast_to(var_type,ret[2],ret[1]):
	
		return ret
		
	elif can_cast_to(var_type.content,ret[2],ret[1]):
	
		return ret
		
	else:
		Logger.log(str(ret), 6 , Logger.Type.DEBUG , Logger.Flag.DATA)
		Logger.log(txt, 6 , Logger.Type.DEBUG , Logger.Flag.DATA)
		Logger.log(str(var_type), 6 , Logger.Type.DEBUG , Logger.Flag.DATA)
		Logger.log(str(ret[2]), 6 , Logger.Type.DEBUG , Logger.Flag.DATA)
		assert False , 'Type mismatch'
	return ret


def check_for_value(txt,var_type=None):


	v = 0
	return_type = 0
	
	try:
		v = int(txt[0],10)
		
	except ValueError:
		
		if txt[0] not in ["'" , '"' , OP.index_op[OP.SQRBRACKETL]]:
			return [False]
			
		else:
		
			v=0
	

	try:
		v = int(txt,10)
		return [True,v,vV_Var.vV_Int_Type()]
		
	except ValueError:
	
		pass
		
	try:
		v = int(txt,2)
		return [True,v,vV_Var.vV_Int_Type()]
		
	except ValueError:
	
		pass
		
	try:
		v = int(txt,16)
		return [True,v,vV_Var.vV_Int_Type()]
		
	except ValueError:
	
		pass
		
	if txt[0] in ["'" , '"' ] and txt[-1] == txt[0]:
	
		content = txt[1:-1]
		
		
		if len(content) > 4:
		
			return_type=OP.STR_LITERAL
			
			
			
			return [True,content,return_type]
		
		
		
	
		if len(content) <= 1:
		
			return_type=vV_Var.vV_Byte_Type()
			
		elif len(content) <= 4:
		
			return_type=vV_Var.vV_Int_Type()
			
			
		v = ord(txt[1])
			
		if len(txt) >3 :
		
			v += ord(txt[2]) << 8
			
		if len(txt) >4 :
		
			v += ord(txt[3]) << 16
		if len(txt) == 6 :
		
			v += ord(txt[4]) << 24
			
			
		return [True,v,return_type]
		
		
	if txt[0] == OP.index_op[OP.SQRBRACKETL] and txt[-1] == OP.index_op[OP.SQRBRACKETR]:
	
	
		a_i = Array_Initializer()
		
		val = a_i.check_array_value(txt,var_type)
		
		if not val[0]:
		

			Logger.log('Error parsing array value',  0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
			return [False]
		
		return_type = val[2]
		
		Logger.log(val)
		
		if not val[0]:
		
		
			Logger.log(val,  4 , Logger.Type.DEBUG , Logger.Flag.DATA) 
			Logger.log('Error parsing array value',  0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
			assert False , 'TODO: Redo error handeling'
			
		else:
		
			return [True,[val[1],OP.ARR_INIT],return_type]
			
			

		
	
	
