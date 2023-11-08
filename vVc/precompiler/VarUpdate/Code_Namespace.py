
import vV_Function
import vV_Variable


import vV.VM_Opcode as OP



class NameSpace_Error:


	SYMBOL_REDEFINE = 1



#Errors: catched by compilerto get adress?
#ret_value indicate Errors?



class NameSpace_Manager:


	global_vars = {}
	functions = {}
	system_vars = {}
	is_main = False
	
	internal_filename=''
	
	def __init__(self,filename=''):
	
		self.filename = filename
		
		self.build_internal_name()
	
		self.global_vars = {}
		self.functions = {}
		
		self.imported = {}
		
		self.system_vars['I']=vV_Variable.vV_Variable('I',204,vV_Variable.vV_Iterator_Type(vV_Variable.vV_Int_Type(),2,96),False,0, OP.ACCESS_PUBLIC ,  OP.CONSTANT)
		
		#print self.system_vars['I'].var_type.content
		

	
	def build_internal_name(self):
	
		self.internal_filename = self.filename.split('/')[-1].split('.')[0]
		
		
	
	def define_function(self,name,args = {}):
	
		if name in self.functions.keys(): 
		
			return NameSPace_Error.SYMBOL_REDEFINE
		
		
		self.functions[name] = vV_Function.vV_Function(name,args)
		
		return 0
		
	def define_global(self,var_obj):
	
		#assert name not in self.global_vars.keys() ,"Raise redefs erreor, need proper_error_managment"
		
		if var_obj.name in self.global_vars.keys():
		
			return NameSPace_Error.SYMBOL_REDEFINE
		
		self.global_vars[var_obj.name] = var_obj  #vV_Variable.vV_Variable()
		
		return 0
		
		
	def is_a_func(self,funcname,namespace=None):
	
		if namespace==None:
		
			if funcname in self.functions:
			
				return True
				
			else:
			
				return False
				
		else:
		
			return self.imported[namespace].is_a_func(funcname)
	
	def get_function(self,funcname,namespace=None):
	
		print 'looking for func:'
		print funcname
		if namespace==None:
		
			if funcname in self.functions:
			
				return self.functions[funcname]
				
			else:
			
				return False
				
		else:
		
			return self.imported[namespace].get_function(funcname)
			
	def get_var(self,varname,scope = None,namespace=None):

	
		ret_val = ''
		
		print 'solving var obj '+varname[0]
		
		if namespace==None:
		
			if varname[0] == 'vV_PUSH_ARG':
		
				#return [True,'eax',False,varname[1]]
				
				assert False , 'TODO: manage typeof arguments to func'
		
		
			if scope in self.functions:
		
				f_obj = self.functions[scope].get_var_obj(varname[0])
				if not f_obj[0]:
				
					assert False , 'couldnt get a var object from fuction'
				return [True , f_obj[1]]
			
				
			if varname[0] in self.global_vars:
		
				
				return [True, self.global_vars[varname[0]] ]
		
			elif varname[0] in self.system_vars:
		
				return [True,self.system_vars[ varname[0]]]
			
			else:
		
				print varname
				print namespace
				assert False , 'Should be unreachable'
				return [False]
		else:
		
			print self.imported
			return self.imported[namespace].get_var(varname,scope)
			assert False,'Unimplemented '+ varname[0] +'in'+ namespace
			
						
	def is_var_init(self,varname,namespace):
	
		if namespace == None or (self.is_main and namespace == self.internal_filename):
		
			return  self.global_vars[varname].is_init
			
		elif namespace == self.internal_filename and not self.is_main:
		
			return self.global_vars[varname].is_init
		else:
		
			return self.imported[namespace].global_vars[varname].is_init
					
		
		
	def solve_var(self,varname,scope = None,namespace=None):
	
		ret_val = ''
		
		print 'solving var '+varname[0]
		
		if namespace==None:
		
			if varname[0] == 'vV_PUSH_ARG':
		
				return [True,'eax',False,varname[1]]
		
		
			if scope in self.functions:
		
				loc = self.functions[scope].solve_var(varname[0])
			
				if loc[0]:			#May need to check for ptr type
			
					return [True,loc[1],False,loc[2]]
				
			if varname[0] in self.global_vars:
		
				
				return [True,  self.global_vars[varname[0]].name,True,self.global_vars[varname[0]].var_type]
		
			elif varname[0] in self.system_vars:
		
				return [True,'[rsp+8]',False,self.system_vars[varname[0]].var_type,True]
			
			else:
		
				return [False]
		else:
		
			print self.imported
			return self.imported[namespace].solve_var(varname,scope)
			assert False,'Unimplemented '+ varname[0] +'in'+ namespace	
			
		
		
		
		
		
		
