

import transpiler.Translator as Trans
import transpiler.Var_Solver as Var_Solver
import vm.Program


class Recursive_Transpiler:


	def __init__(self,ir_array,out_file):
	
		
		self.main_ir = ir_array[-1]
		self.ir_array= ir_array[:-1]
		
		self.output_file = out_file
		
		assert self.main_ir.is_main, "FATAL!"
		
	def build_single_file(self,ir_data):
	
		print '\n\n\n\n BUILDING A NEW FILE FUNCTIONS'
		print ir_data.namespace.filename
		print ir_data.prog.size
		print '\n\n\n\n'
		vs =  Var_Solver.Var_Solver(ir_data.namespace)
		piler = Trans.Translator(ir_data.prog,ir_data.labels,vs)
		
		piler.generate_label_names()
		#assert len(ir_data.f_loca.keys()) >0 , 'No func def found'
		piler.def_label_names = ir_data.f_loca
		
		for p in range(ir_data.prog.size):


			piler.step_compile()
			
		return piler.output
		
	def build_file(self):
	
		
		imported = ''
	
		for i_ns in self.ir_array:
		
			imported += self.build_single_file(i_ns)
			print len(imported)
			print '\n\n\n\n'
			
		ir_data = self.main_ir
			
		vs =  Var_Solver.Var_Solver(ir_data.namespace)
		piler = Trans.Translator(ir_data.prog,ir_data.labels,vs,self.output_file)
		
		print imported
		
		piler.add_inserted_code(imported)
		piler.generate_label_names()
		piler.generate_header()

		
		
		for p in range(ir_data.prog.size):


			piler.step_compile()
			
		return piler
		
