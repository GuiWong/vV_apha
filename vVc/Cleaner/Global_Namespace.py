
import precompiler.VarUpdate.Code_Namespace as NS
import precompiler.VarUpdate.vV_Variable as vV_Var

import os
import sys

import vV.VM_Opcode as OP

home_path = os.path.expanduser('~') 

sys.path.append(home_path+'/.local/share/vVCompiler/utilities/')

import Logger

class Global_Namespace:


	def __init__(self,main_file):
	
		self.main_namespace = NS.NameSpace_Manager(main_file)
		self.main_file = main_file
		
		self.main_namespace.is_main = True
		
		self.imported = {}
		
		self.paths = ['']
		
		self.paths.append(self.calc_main_path())
		
		self.bss_txt = ''
		self.data_txt = ''
		
	def calc_main_path(self):
	
		path = self.main_file.split('/')
		outpath = '/'.join(path[:-1]) +'/'
		return outpath
		
	def solve_reserve(self,var):
	
		size = var.var_type.calc_size() / 8
		
		return 'resb '+str(size) +' \n'
		
		
		
	def solve_assign(self,var):
	
		if isinstance(var.var_type,vV_Var.vV_Int_Type):
		
			return 'dq '+str(var.init_value)+'\n'
			
		elif isinstance(var.var_type,vV_Var.vV_Byte_Type):
		
			return 'db '+str(var.init_value)+'\n'
			
		elif isinstance(var.var_type,vV_Var.vV_Array_Type):
		
		
			testret = ''
			
			if isinstance(var.var_type.content,vV_Var.vV_Byte_Type):
			
				if var.init_value[1] == OP.ARR_INIT:
				
					Logger.log( 'Translating from array format', 8 , Logger.Type.DEBUG , Logger.Flag.TEXT) 
					Logger.log( str(var.init_value) , 8 , Logger.Type.DEBUG , Logger.Flag.DATA) 
					
					testret+=' db '
					for i in range(len(var.init_value[0])):
					
						testret += ' '+ str(var.init_value[0][i]) +  ' '
						
						if i < len(var.init_value[0])-1:
						
							testret += ','
							
					testret += '\n'
					
					Logger.log( testret , 0 , Logger.Type.DEBUG , Logger.Flag.DATA) 				
					
					#assert False , 'Needto implement initialised array format '
					
				elif var.init_value[1] == OP.STR_LITERAL:
				
					Logger.log( 'Translating from array format', 8 , Logger.Type.DEBUG , Logger.Flag.TEXT) 
					Logger.log( str(var.init_value) , 8 , Logger.Type.DEBUG , Logger.Flag.DATA) 
					testret += 'db "'+str(var.init_value[0])+'"\n'
				
				
				else:
				
					Logger.log( 'Unrecognised Format for Array Value', 0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
					Logger.log( str(var.init_value[1]) , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
					Logger.log( str(var.init_value) , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
					
					assert False , 'TODO: redo Errors Handeling'
					
			elif isinstance(var.var_type.content,vV_Var.vV_Int_Type):
			
				if var.init_value[1] == OP.ARR_INIT:
				
					Logger.log( 'Translating from array format', 8 , Logger.Type.DEBUG , Logger.Flag.TEXT) 
					Logger.log( str(var.init_value) , 8 , Logger.Type.DEBUG , Logger.Flag.DATA) 
					
					testret+=' dd '
					for i in range(len(var.init_value[0])):
					
						testret += ' '+ str(var.init_value[0][i]) +  ' '
						
						if i < len(var.init_value[0])-1:
						
							testret += ','
							
					testret += '\n'
					
					Logger.log( testret , 0 , Logger.Type.DEBUG , Logger.Flag.DATA) 
					#assert False , 'Needto implement initialised array format '
					
				elif var.init_value[1] == OP.STR_LITERAL:
				
					Logger.log( 'unimplemented Int Array from String litteral', 0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
					Logger.log( str(var.init_value[1]) , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
					assert False , 'UNREACHABLE'
				
				else:
				
					Logger.log( 'Unrecognised Format for Array Value', 0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
					Logger.log( str(var.init_value[1]) , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
					Logger.log( str(var.init_value) , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
					
					assert False , 'TODO: redo Errors Handeling'
				
				#assert False , 'TODO: redo Errors Handeling'
			
			
			#Logger.log( 'Not implemented translation to value', 0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
			#Logger.log( str(var.init_value) , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
			Logger.log( testret , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
			Logger.log( str(var.var_type.content) , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
			
			return testret
			#assert False , 'Needto implement initialised pther types'
			
		else:
		
			Logger.log( 'Not implemented translation to value', 0 , Logger.Type.ERROR , Logger.Flag.TEXT) 
			Logger.log( str(var.init_value) , 0 , Logger.Type.ERROR , Logger.Flag.DATA) 
			assert False , 'Needto implement initialised pther types'
		
		
	def build_var_file(self):
	
	
		self.bss_txt = ' segment .bss\n'
		self.data_txt = ' segment .data\n'
		
		
		for i_ns in self.imported.values():
		
			txt = '_'+i_ns.internal_filename

			self.bss_txt += '	u_global'+txt+':\n'
			self.data_txt += '	i_global'+txt+':\n'
			for var in i_ns.global_vars.keys():
			
				line = ''
				line += '.'+var+':'
				
				if i_ns.global_vars[var].is_init:
				
					line+= self.solve_assign(i_ns.global_vars[var])
					self.data_txt += line
					
				else:
				
					line+= self.solve_reserve(i_ns.global_vars[var])
					self.bss_txt += line
					
		self.bss_txt += '	u_global:\n'
		self.data_txt += '	i_global:\n'
		
		for var in self.main_namespace.global_vars.keys():
		
			line = ''
			line += '.'+var +':'
			
			if self.main_namespace.global_vars[var].is_init:
		
				line+= self.solve_assign(self.main_namespace.global_vars[var])
				self.data_txt += line
				
			else:
				
				line+= self.solve_reserve(self.main_namespace.global_vars[var])
				self.bss_txt += line
				
		return [self.bss_txt,self.data_txt]					
					
					
			
		
		
		
	def is_imported(self,filename):
	
	
		if filename in self.imported:
		
			return True
			
		elif filename == self.main_namespace.filename:
		
			return True
			
		else:
		
			return False
			
	def get_namespace(self,filename):


		return self.imported[filename]
		
	def create_namespace(self,filename):
	
		assert not self.is_imported(filename) , 'Trying to Import already imported file'
		
		self.imported[filename] = NS.NameSpace_Manager(filename)
		
		return self.imported[filename]
		
	def set_functions_prefixes(self):
	
		for i_ns in self.imported.values():
		
			#print i_ns.internal_filename
			for func in i_ns.functions.values():
			
			#	print func.name
				func.effective_namespace = i_ns.internal_filename + '_'
			#	print func.effective_namespace

