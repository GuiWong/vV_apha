
import precompiler.VarUpdate.Code_Namespace as NS
import precompiler.VarUpdate.vV_Variable as vV_Var



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
			
		else:
		
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
			
	def get_namspace(self,filename):


		return self.imported[filename]
		
	def create_namespace(self,filename):
	
		assert not self.is_imported(filename) , 'Trying to Import already imported file'
		
		self.imported[filename] = NS.NameSpace_Manager(filename)
		
		return self.imported[filename]

