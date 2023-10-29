import Cleaner.Parser as Parser
import vV.VM_Opcode as OP

import Cleaner.Syn_Parser as Syntaxer

import Cleaner.OneWayParser as OW_Parser


import vm.Program
import vm.Machine

import transpiler.Translator as Trans
import transpiler.Var_Solver as Var_Solver

par = Parser.Parser('')
#par.default('../w_samples/source/rule110.vV')
par.default('Cleaner/parsetest.vV')

parsed = par.first_pass()


ow_parser = OW_Parser.One_Way_Parser(parsed)

#ow_parser.convert_all()

for f in parsed:

	print f
		
		
for f in parsed:

	ow_parser.next_token()
	
	
	
print '	Variables:\n\n'

	
for vr in ow_parser.name_space.global_vars:

	print '------------------------------'
	print ow_parser.name_space.global_vars[vr].name
	print ow_parser.name_space.global_vars[vr].var_type
	
	
print '	Functions:\n\n'

for func in ow_parser.name_space.functions:

	#print func
	print ow_parser.name_space.functions[func].name
	
	print '	Args: '
	for arg in ow_parser.name_space.functions[func].referenced_vars:
		print ow_parser.name_space.functions[func].referenced_vars[arg].name + ' : ' + str(ow_parser.name_space.functions[func].referenced_vars[arg].var_type)
	
	
	print '\n	Locals: '
	
	for loc in ow_parser.name_space.functions[func].local_vars:
	
		print ow_parser.name_space.functions[func].local_vars[loc].name + ' : ' + str(ow_parser.name_space.functions[func].local_vars[loc].var_type)
		
		
		
print 'code :'

print '	Function code:'

for o in ow_parser.def_op:

	print o.value , o.arg
	
print '\n	Body code:'

i = 0
for o in ow_parser.main_op:

	
	print str(i) +' : '+ str(o)
	print o.value , o.arg
	
	i+=1
	
print '\n 	Func Location:'

print ow_parser.func_loca



tmp_label = {}
output_file = ''



print ow_parser.label_manager.labels

print ow_parser.label_manager.def_labels


vs = Var_Solver.Var_Solver(ow_parser.name_space)


prog2 = vm.Program.Program(ow_parser.def_op)

piler2 = Trans.Translator(prog2,ow_parser.label_manager.def_labels,vs)

piler2.generate_label_names()
piler2.def_label_names = ow_parser.func_loca

for p in range(prog2.size):


	piler2.step_compile()





prog = vm.Program.Program(ow_parser.main_op)

piler = Trans.Translator(prog,ow_parser.label_manager.labels,vs)
piler.out_path='Cleaner/'

piler.add_inserted_code(piler2.output)

piler.generate_label_names()
piler.generate_header()

for p in range(prog.size):


	piler.step_compile()
	
piler.end_file()
piler.generate_var_file()
piler.print_file()






