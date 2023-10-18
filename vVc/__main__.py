import vV.VM_Opcode as OP
import WErrors
import precompiler.Pre_Compiler_states as State

import precompiler.Pre_Compiler as Precompiler


import options as O

import precompiler.Opcode



import sys

import vm.Program
import vm.Machine

import transpiler.Translator as Trans
#import transpiler.Pre_Translator as Pre_Trans



#----------------------Variables--------------------------------------------


flags = 0

outformat = 0

output_file = 0

source_file = 0




#---------------------Arguments Parsing---------------------------------------


argv = sys.argv
next_arg = 0

if len(argv) == 1:

	print ' Usage: wcs -o out -f format -args file(s)  [UNIMPLEMENTED] \n\n\n\
|	No format for now, only inpur file Needed\n\
|	you can use the bash script "wc0" with:\n\
|		./wc0 path/to/file\n\
|	transpiled (assembly) and compiled files endup in \n\
|		"w_samples/"\n\
|	a file showing machine code and essembly instruction\n\
|	is created in "inw_samples/tmp"\n| \n| \n\
|		THIS IS A WORK IN PROGRESS\n\
|		IT IS IN VERY EARLY STAGES AND \n\
|		IS ONLY INTENDED FOR PERSONAL USE FOR NOW\n\
|	\n\
|	Use at your own risk, i learned assembly during\n\
|	this project, I have no idea how bad it could go... \n\n\n\n'

	
else:

	for arg in argv[1:]:
	
		if arg[0] == '-':
		
			if arg in O.argflag.keys():
			
				flags = flags | O.argflag[arg]
				
			elif arg in O.argarg:
			
				assert next_arg == 0 , O.argarg.key(next_arg) + "option needs an argument )"
					
				next_arg = arg
				
			else:
			
				assert False, "Unrecognised or unimplemented option : "+arg
				
		elif next_arg != 0:
		
		
			if next_arg == FORMAT:
			
				assert outformat == 0 , "Trying to define more than one file format"
				outformat = arg
				next_arg = 0
					
			elif nextarg == OUTPUT_FILE:
			
				assert output_file == 0 , "Trying to define more than one file format"
				
				output_file = arg 
				next_arg = 0
				
			else:
			
				assert False , 'ERROR, SHOULD BE UNREACHABLE'
				
			
		else:
		
			if source_file == 0:
			
				source_file = arg
				
			else:
			
				print 'multiples sources files provided, currently unimplemented'
				print 'ignoring succequent filearguments'

#-------------------Apply Default settings--------------



assert source_file != 0, 'No Source file Provided'

if outformat == 0:

	outformat = O.Format.RAW


if output_file== 0:

	if '/' in source_file:
	
		output_file = source_file.split('/')[-1].split('.')[0]
		
	else:

		output_file = source_file.split('.')[0] 


#-------------------LOG---------------------------				
	
print '	Running wcs default mode (only mode for now) '
print'	source file provided: '+ source_file
print'	format:	'+O.outformat.keys()[O.outformat.values().index(outformat)]
print'	output file:	'+output_file
	
print'	'	
print'	press enter to proceed to precompile step'




#---------------------Init Phase---------------------------------------



pre_compiler = Precompiler.Pre_Compiler()

pre_compiler.setup_startup(flags)


pre_compiler.open_main_file(source_file)


print'	'
print'	'
print'	file '+source_file+' loaded'

print'	'	
print'	starting pass 1'



a, b = pre_compiler.first_pass()

code_arr = a[0]
labels = a[1]


def_arr = b[0]
v2_lab = b[1]
def_lab = b[2]


#print labels


prog2 = vm.Program.Program(def_arr)


piler2 = Trans.Translator(prog2,v2_lab,output_file)
piler2.generate_label_names()
piler2.def_label_names = def_lab

for p in range(prog2.size):


	piler2.step_compile()





prog = vm.Program.Program(code_arr)

vm = vm.Machine.Emul(prog)

piler = Trans.Translator(prog,labels,output_file)



piler.add_inserted_code(piler2.output)


piler.generate_label_names()
piler.generate_header()

for p in range(prog.size):


	piler.step_compile()
	
piler.end_file()
piler.print_file()


print "file successfully created"

#while True:


#	vm.step_exec()

'''
	vm.fetch()
	
	vm.debug_info()
	
	vm.execute_opcode()
	
	vm.show_stack()
	
	raw_input()
'''

#---------------------End Phase--------------------------------------------



exit(0)







