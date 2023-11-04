
import vV.VM_Opcode as OP
import WErrors as ERR
import copy


def build_type(type_id):


	if type_id == OP.UINT_32:
	
		return vV_Int_Type()
		
	elif type_id == OP.UINT_8:
	
		return vV_Byte_Type()
		
	else:
	
		raise ERR.InvalidType('To Implement',False,False)


class vV_Primary_Type:

	size = 0
	
	def __str__(self):
	
		return "Unimplemented Type"
		
	def calc_size(self):
	
		return self.size
		

		
class vV_Pointer_Type:

	size = 32
	content = vV_Primary_Type()
	use_offset = False
	
	def calc_size(self):
	
		return self.size
	
	def calc_pointed_size(self):
	
		return self.content.calc_size()
		
class vV_Structure_Type:

	content = vV_Primary_Type()
	
	def calc_size(self):
	
		return content.calc_size()



class vV_Byte_Type(vV_Primary_Type):


	size = 8
	
	def __init__(self):
	
		pass
			
	def __str__(self):
	
		return "<byte>"
		
	def copy(self):
	
		return vV_Byte_Type()

		
class vV_Int_Type(vV_Primary_Type):


	size = 32
	
	def __init__(self):
	
		pass
	
	def __str__(self):
	
		return "<int>"
	
	def copy(self):
	
		return vV_Int_Type()
		
		
class vV_Ref_Type(vV_Pointer_Type):

	def __init__(self,content):
	
		self.content = content
	
	def __str__(self):
	
		return "("+str(self.content)+")"
		
	def calc_partial_size(self,dim_down):
	
	
		return self.content.calc_partial_size(dim_down)
		
	def copy(self):
	
		return vV_Ref_Type(self.content.copy())
		
class vV_Iterator_Type(vV_Structure_Type):

	direct = 0
	skip = 0
	def __init__(self,content,direct,skip):

		self.content = content
		self.direct = direct
		self.skip= skip
		
		
class vV_Array_Type(vV_Structure_Type):

	content = vV_Primary_Type()
	dim = 1
	size = []
	
	def __init__(self,content,dims,size):

		self.content = content
		self.dim = dims
		
		print size
		#print self.size
		self.size = []
		
		for s in size:
		
			self.size.append(s)
			
		print self.size
		self.size.reverse()
		#print self.size
		
		
	def copy(self):
	
		reversed_size = copy.copy(self.size)
		reversed_size.reverse()
	
		return vV_Array_Type(self.content.copy(), self.dim , copy.copy(reversed_size))
		
	def get_partial(self,deepness):
	
		assert deepness <= self.dim , "Fatal: trying to reduce an array toomuch"
		
		if deepness < self.dim:
			reversed_size = self.size[deepness:]
			reversed_size.reverse()
			return vV_Array_Type(self.content, self.dim - deepness , reversed_size)
		else:
			return self.content
			
	def get_from_to(self,from_index,to_index):
	
		if from_index == None:
		
			from_index = 0
			
		if to_index == None:
		
			to_index = self.size[0]
			
		print type(from_index)
		print type(self.size[0] )
			
		assert from_index < self.size[0] , 'min index_mismatch : '+str(from_index) + ' with max : '+str(self.size[0])
		assert to_index <= self.size[0] , 'max index mismatch : '+str(to_index)
		
		reversed_size = self.size
		reversed_size[0]= (to_index - from_index )
		reversed_size.reverse()
		
		return vV_Array_Type(self.content, self.dim , reversed_size)
		
	def calc_partial_size(self,dim_down):
	
		
		e = 1
		for d in range(dim_down,self.dim):
		
			e = e * self.size[d]
			
		e = e * self.content.calc_size()
		
		return e
		
		
	def calc_size(self):
	
	
		e = 1
		for d in range(self.dim):
		
			e = e * self.size[d]
			
		e = e * self.content.calc_size()
		
		return e
		
	def get_total_elem(self):
	
		e = 1
		for d in range(0,self.dim):
		
			e = e * self.size[d]
			
		#e = e * self.content.calc_size()
		
		return e
			
	'''		
	def __str__(self):
	
		buff = []
		for d in range(self.dim):
		
			buff.append('[' + str(self.size[d])+']')
			
		buff.reverse()
		#print buff
		buff = ''.join(buff)

	
		return str(self.content) +"["+str(self.dim)+"]"#  ---  "+str(self.content) + buff
		
	'''	
		
class vV_Type:		#Need to refactor

	UNFOUND = 0
	VALUE = 1
	POINTER = 2	

	
class Scope:

	GLOBAL = 1
	LOCAL = 2
	

scope_names = ["global","local"]
type_names = ["unfound","value","pointer"]


class vV_Variable:


		
	name = ''
	var_type = vV_Primary_Type()
	scope = Scope.GLOBAL
	is_init = False
	init_value = 0
	
	internal_id = 0	#may be usefull for argument ordering double verification




	def __init__(self,name,scope,vV_type,is_init=False,init_value=0):
	
		self.name = name
		self.var_type = vV_type
		self.scope = scope
		self.is_init = is_init
		self.init_value = init_value
		
	def calc_size(self):
	
		return self.var_type.calc_size()
		

		
	def value_debug_txt(self):
	
	
		if self.is_init:
		
			return "With Value: "+str(self.init_value)
			
		else:
		
			return "not initialized to any value"
		
		
	#def __str__(self):
	
	#	return "Var "+self.name+" \n Scope: "+OP.var_define.keys()[OP.var_define.values().index(self.scope)]+"\n Type: "+str(self.var_type)+"\n "+ self.value_debug_txt()
		
		
