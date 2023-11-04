
import Cleaner.Global_Namespace as G_NS
import precompiler.VarUpdate.Code_Namespace as NS

import Cleaner.Syn_Parser as Syntaxer
import Cleaner.Parser as Parser
import Cleaner.OneWayParser as OW_Parser

import vm.Program


import os


class Ir_Data:

	prog = None
	labels = {}
	f_loca = {}
	is_main = False
	namespace = None
	
	def __init__(self):
	
		pass

class Recursive_Importer:


	def __init__(self,filename):
	
	
		self.namespace = G_NS.Global_Namespace(filename)
		#sself.main_file = 
		
	def file_validity(self,filename):
	
		#adress =''
		#for path in self.namespace.path:
		#	eff_path= path+filename
		#	print 'import: trying...'
		#	print eff_path
			
		if os.path.isfile(filename):
		
			return True
		else:	
				
			return False
		
	def import_file(self,filename):
	
		for path in self.namespace.paths:
			eff_path= path+filename
			print 'looking for imported...'
			print eff_path
			if self.namespace.is_imported(eff_path):
		
				return [False,self.namespace.get_namespace(eff_path),eff_path]
			
		for path in self.namespace.paths:	
			eff_path= path+filename
			print 'looking for file...'
			print eff_path
			if self.file_validity(eff_path): 
			
				return [True,self.namespace.create_namespace(eff_path),eff_path]
				
		
		
		
	def rec_parser(self,result_array,file_name,namespace,main=False):
	
		par = Parser.Parser('')

		par.default(file_name)
		parsed = par.first_pass()


		ow_parser = OW_Parser.One_Way_Parser(parsed,namespace)

		result = Ir_Data()
		
		print '\n\n\nNew Recursion Level:\n\n\n'
		
		
		for f in parsed:

			require = ow_parser.next_token()
			if require:
				
				print namespace.filename
				import_data = self.import_file(require[0])
				if import_data[0]:
					self.rec_parser(result_array,import_data[2],import_data[1])
				
				nickname = require[1]
				if require[1] == None:
				
					nickname = require[0].split('/')[-1].split('.')[0]
					
				namespace.imported[nickname] = import_data[1]
				#assert False , 'Unimplemented import: '+ require
				
				
		result.prog = vm.Program.Program(ow_parser.def_op)
		result.labels = ow_parser.label_manager.def_labels
		result.f_loca = ow_parser.func_loca
		result.namespace = namespace
		
		result_array.append(result)
		
		if main:
		
			result = Ir_Data()
			result.prog = vm.Program.Program(ow_parser.main_op)
			result.labels = ow_parser.label_manager.labels
			#result.f_loca = ow_parser.func_loca
			result.namespace = namespace
			result.is_main = True
			result_array.append(result)
			
			
		print '\n\n\End of Recursion Level:\n\n\n'	
		ow_parser = None	
		
	
		
	def parse_main(self):
	
	
		result = []
		
		self.rec_parser(result,self.namespace.main_file,self.namespace.main_namespace,True)
		
		return result
		
	def build_var_decl(self):
	
	
		return self.namespace.build_var_file()

