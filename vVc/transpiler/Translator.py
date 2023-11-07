
import vV.VM_Opcode as OP
import precompiler.Opcode as Opcode
import vm.Program 

import Cleaner.Recursive_Var_Solver as R_V_S

import os
import sys
home_path = os.path.expanduser('~') 

sys.path.append(home_path+'/.local/share/vVCompiler/utilities/')

import Logger

class ComF:

	OPADR = 1
	OPNAME = 2
	NLBTW = 4
	NLADR = 8
	NLNAME = 16
	TABOP = 32
	
	



class Translator:


	
	lib_path = 'vVc/assembly/w_runtime/'
	
	out_path = 'w_samples/assembly/'
	
	filename = ''
	
	extension = ".was"
	
	comment_flag = 3	#All Comments



	def __init__(self,prog,labs,var_solver,filename='output'):
	
		self.filename = filename
		self.program = prog
		self.labels = labs
		self.label_names = {}
		self.output = ''
		
		self.def_label_names = {}
		
		self.name_space = ''
		
		
		self.pc = -1
		self.sp = 0#64
		
		self.current_op = 0
		
		self.label_count = 0
		
		self.inserted = ''
		
		
		self.comment_flag=ComF.OPADR | ComF.OPNAME | ComF.NLBTW | ComF.NLNAME | ComF.TABOP
		
		
		
		self.current_scope =None	#V0.0.4
		self.var_solver = var_solver
		
		self.var_op_solver = R_V_S.Var_Op_Solver(self.var_solver.namespace)
		
		
	def fetch(self):
	
		self.pc += 1
		self.current_op = self.program.code[self.pc]
		
	def add_inserted_code(self,raw):
	
		self.inserted = raw
		
	def generate_label_names(self):
	
	
		for l_adr in self.labels.keys():
		
		
			Logger.log('Label Creation : ' , Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.TEXT)
			Logger.log(self.labels[l_adr] , Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.DATA) 
		
			lbid = self.labels[l_adr]
			
			
			
			
			lbname = 'wblock_'+self.var_solver.namespace.internal_filename+str(lbid)

			Logger.log(lbname, Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.DATA) 

			self.label_names[l_adr] = lbname
		
	def generate_label(self,name):
	
	
		return '\n\n	'+name+':		\n\n\
;------------------------------------------------------\n\n'


	def generate_var_file(self,txt=None):
	
		if txt == None:
			self.var_solver.generate_var_decl()
			txt_out = self.var_solver.generate_var_file()
			
		else:
		
			txt_out = txt
	
		outf= self.out_path+self.filename+'_vars.was'
		
		with open(outf, 'w+') as imp:
		
			imp.write(txt_out)
			
	def generate_txt(self,op_txt,op_name):
	
		outf = ''
		if self.comment_flag & ComF.OPNAME:
		
			outf+= op_name
			
		if self.comment_flag & ComF.NLNAME:
		
			outf+='\n'
			
		if self.comment_flag & ComF.TABOP:
		
			outf+='	'
			
		outf += op_txt
		
		if self.comment_flag & ComF.NLBTW:
		
			outf+= '\n'
			
		return outf
		

	def generate_header(self):
	
	
		self.output+= '\
%include "'+self.lib_path+'vV_defines.asm"		\n\
%include "'+self.lib_path+'vV_error_code.asm"		\n\
%include "'+self.lib_path+'vV_runtime.asm"		\n\
\
%include "'+self.lib_path+'vV_system00.asm"		\n\
%include "'+self.lib_path+'vV_errors.asm"		\n\
\
%include "'+self.lib_path+'vV_system10.asm"		\n\
%include "'+self.lib_path+'vV_io.asm"			\n\
%include "'+self.lib_path+'vV_ascii.asm"		\n\
\
%include "'+self.out_path+self.filename+'_vars.was"	\n\
%include "'+self.lib_path+'vV_system90.asm"		\n\
\
\n'


		



		self.output+= '''

global w_entry_point



segment .text 


'''
		self.output+=self.inserted
		self.output+= '''
		



vV_entry_point:


	push rbp
	mov rbp, rsp			;Setup Stack Frame
	
	'''
			
		
	
	def step_compile(self):
	
	
	
		
	
		self.fetch()
		
		
			
		if self.pc in self.def_label_names.keys():
		
			#self.output += self.generate_label(self.def_label_names[self.pc])
	
			
			self.current_scope = self.def_label_names[self.pc]	

			self.output += self.var_solver.namespace.functions[self.def_label_names[self.pc]].generate_head()
			
		if self.pc in self.labels.keys():
		
			self.output += self.generate_label(self.label_names[self.pc])
			
		if self.comment_flag & ComF.OPADR:
			
			self.output += ';OpADR: ['+str(self.pc)+'] ' 
			
		if self.comment_flag & ComF.NLADR:
		
			self.output+='\n'
			
		self.translate_opcode()
		
		
		
	def end_file(self):
	
	
		self.output += '''\
		
		mov rsp , rbp
		pop rbp
		ret

;Transpiled from vV with vVc version 0.0.4.5
		
		'''
		
	def print_file(self):
	
		with open(self.out_path + self.filename + self.extension , 'w+') as f1:
			f1.write(self.output)
			f1.close()
		
		
	
	def translate_opcode(self):
	
	
		op = self.current_op.value
		arg = self.current_op.arg
		txt = ''
		
		if op == OP.PUSH:


			txt = self.generate_txt('vV_push '+str(arg) +'\n','; PUSH opcode \n')
			
			
		elif op == OP.SWAP:
		
			txt = self.generate_txt('vV_swap \n','; SWAP opcode \n')	

			
		elif op == OP.DROP:
		
			txt = self.generate_txt('vV_dec_sp 1 \n','; DROP opcode \n')
			
		elif op == OP.DUP:
		
			if arg == 0:
			
				arg = 1
		
			txt = self.generate_txt('vV_dup '+str(arg)+'\n',' DUP opcode ('+str(arg)+')')						
			
		elif op == OP.ADD:
		
			txt = 'mov eax , vV_2nd			\n\
	add eax , vV_top			\n\
	mov vV_2nd , eax			\n\
	vV_dec_sp 1		\n'
	
			txt = self.generate_txt(txt,'; ADD opcode \n')
			
			
			
		elif op == OP.SUB:
		
			txt = 'mov eax , vV_2nd			\n\
	sub eax , vV_top			\n\
	mov vV_2nd, eax			\n\
	vV_dec_sp 1		\n'
	
			txt = self.generate_txt(txt,'; SUB opcode \n')
			
		elif op == OP.MUL:
		
			txt = 'mov eax , vV_2nd			\n\
	mul DWORD vV_top			\n\
	mov vV_2nd , eax			\n\
	vV_dec_sp 1	\n'
			txt = self.generate_txt(txt,'; MUL opcode \n')
			
		elif op == OP.DIV:
		
			txt = 'xor edx , edx				\n\
	mov eax , vV_2nd			\n\
	div DWORD vV_top			\n\
	mov vV_2nd , eax			\n\
	vV_dec_sp 1				\n'
	
			txt = self.generate_txt(txt,'; DIV opcode \n')
			
		elif op == OP.NEG:

			txt = self.generate_txt('neg DWORD vV_top\n','; NEG opcode \n')
			
		elif op == OP.MOD:
		
			txt = 'xor edx , edx	\n\
	mov eax , vV_2nd			\n\
	div DWORD vV_top			\n\
	mov vV_2nd , edx			\n\
	vV_dec_sp 1				\n'
			
			txt = self.generate_txt(txt,'; MOD opcode \n')
		
		elif op == OP.LSH:
		
			txt = self.generate_txt('shl DWORD vV_top , 1\n','; LSH opcode \n')
			
		elif op == OP.RSH:
		
			txt = self.generate_txt('shr DWORD vV_top , 1\n','; RSH opcode \n')
		
		elif op == OP.NOT:
		
			txt = self.generate_txt('not DWORD vV_top\n','; NOT opcode \n')
			
		elif op == OP.OR:
		
			txt = 'mov eax , vV_top			\n\
	or DWORD vV_2nd , eax			\n\
	vV_dec_sp 1				\n'
	
			txt = self.generate_txt(txt,'; OR opcode \n')
			

		elif op == OP.AND:
		
			txt = 'mov eax , vV_top			\n\
	and DWORD vV_2nd , eax			\n\
	vV_dec_sp 1				\n'
			
			txt = self.generate_txt(txt,'; AND opcode \n')
			
		elif op == OP.XOR:
		
			txt = 'mov eax , vV_top			\n\
	xor DWORD vV_2nd , eax			\n\
	vV_dec_sp 1				\n'
	
			txt = self.generate_txt(txt,'; XOR opcode \n')
			
			
		elif op == OP.LESS:		#WARNING TODO WARNING
						#very fragile code because
						#of hardcoded jumps
			txt = 'mov eax , vV_top			\n\
	cmp DWORD vV_2nd , eax			\n\
\n\
	jae short 0xb				\n\
\n\
			mov DWORD vV_2nd , -1	\n\
\n\
	jmp short 0x9				\n\
\n\
			mov DWORD vV_2nd , 0	\n\
\n\
	vV_dec_sp 1				\n'
	
			txt = self.generate_txt(txt,'; LESS opcode \n')
				
		elif op == OP.MORE:
		
			txt = 'mov eax , vV_top			\n\
	cmp DWORD vV_2nd , eax			\n\
\n\
	jbe short 0xb				\n\
\n\
			mov DWORD vV_2nd , -1	\n\
\n\
	jmp short 0x9				\n\
\n\
			mov DWORD vV_2nd , 0	\n\
\n\
	vV_dec_sp 1				\n'
	
			txt = self.generate_txt(txt,'; MORE opcode \n')
			
			
		elif op == OP.EQUAL:
		
			txt = 'mov eax , vV_top			\n\
	cmp DWORD vV_2nd , eax			\n\
\n\
	jnz short 0xb				\n\
\n\
			mov DWORD vV_2nd , -1	\n\
\n\
	jmp short 0x9				\n\
\n\
			mov DWORD vV_2nd , 0	\n\
\n\
	vV_dec_sp 1				\n'
	
			txt = self.generate_txt(txt,'; EQUAL opcode \n')
				
				
		elif op == OP.IF:		#Becomes a jump
			txt = 'vV_dec_sp 1			\n\
	or DWORD[vV_sp] , 0			\n\
	je '+self.label_names[arg]+'	\n'
	
			txt = self.generate_txt(txt,'; IF opcode \n')
				
				
		elif op in [ OP.ELSE ]:		#Becomes a jump
	
			txt = self.generate_txt('jmp '+self.label_names[arg]+'	\n','; ELSE opcode \n')
			
		elif op == OP.WHILE:
		
			txt = 'vV_dec_sp 1				\n\
	or DWORD[vV_sp] , 0			\n\
	jne '+self.label_names[arg]+'		\n'
	
			txt = self.generate_txt(txt,'; WHILE opcode \n')
	
		elif op == OP.BREAK:
		
			txt = self.generate_txt('jmp '+self.label_names[arg]+'\n','; BREAK opcode \n')
			
		elif op== OP.GET:
		
			txt = '\
; GET opcode ('+str(arg)+')			\n\
\n'		
			if arg == OP.Format.NONE:
			
				txt+='call vV_io_get_default	\n'
			
			elif arg == OP.Format.DEC:
			
				txt+='mov r10d , vV_ascii_as_dec		\n\
	call vV_io_get		\n'
						
			elif arg == OP.Format.HEX:
			
				txt+='mov r10d , vV_ascii_as_hex		\n\
	call vV_io_get		\n'
						
			elif arg == OP.Format.BIN:
			
				txt+='mov r10d , vV_ascii_as_bin		\n\
	call vV_io_get		\n'	
						
														
			elif arg == OP.Format.CHR:
			
				txt+='call vV_io_get_char	\n'
						
			elif arg == OP.Format.PCHR:
			
				txt+='call vV_io_get_packed_char \n'
				
			else:
			
				Logger.log('FATAL : Format for get not valid : '+arg , 0 , Logger.Type.ERROR , Logger.Flag.TEXT)
				assert False, " FATAL ERROR, Format for get not valid"
						
			txt = self.generate_txt(txt,';GET opcode ('+str(arg)+')\n')
			


		elif op == OP.OUT:

			txt = ''

			if arg == OP.Format.NONE:
			
				txt+=' call vV_io_out_default	\n'
			
			elif arg == OP.Format.DEC:
			
				txt+=' mov r10d , vV_FORMAT_DEC	\n\
	call vV_io_out \n'
						
			elif arg == OP.Format.HEX:
			
				txt+=' mov r10d , vV_FORMAT_HEX	\n\
	call vV_io_out	\n'
						
			elif arg == OP.Format.BIN:
			
				txt+=' mov r10d , vV_FORMAT_BIN	\n\
	call vV_io_out\n'	
						
						
						
			elif arg == OP.Format.CHR:
			
				txt+='call vV_io_out_char\n'
						
			elif arg == OP.Format.PCHR:
			
				txt+='call vV_io_out_packed_char\n'
						
						
			else:
			
				Logger.log('FATAL : Format for out not valid : '+arg , 0 , Logger.Type.ERROR , Logger.Flag.TEXT)
				assert False, " FATAL ERROR, Format for out not valid"

			txt = self.generate_txt(txt,'; BUFF_OUT opcode ('+str(arg)+')\n')

		elif op == OP.BUFF_OUT:

			txt = ''

			if arg == OP.Format.NONE:
			
				txt+='call vV_io_out_buffer_default	\n'
			
			elif arg == OP.Format.DEC:
			
				txt+='mov r10d , vV_FORMAT_DEC\n\
	call vV_io_out_buffer\n'
						
			elif arg == OP.Format.HEX:
			
				txt+='mov r10d , vV_FORMAT_HEX\n\
	call vV_io_out_buffer	\n'
						
			elif arg == OP.Format.BIN:
			
				txt+='mov r10d , vV_FORMAT_BIN\n\
	call vV_io_out_buffer	\n'	
						
						
			elif arg == OP.Format.CHR:
			
				txt+='call vV_io_out_char_buffer\n'
						
			elif arg == OP.Format.PCHR:
			
				txt+='call vV_io_out_packed_char_buffer \n'
						
			else:
			
				Logger.log('FATAL : Format for out not valid : '+arg , 0 , Logger.Type.ERROR , Logger.Flag.TEXT)
				assert False, " FATAL ERROR, Format for out not valid"

			txt = self.generate_txt(txt,'; OUT opcode ('+str(arg)+')\n')

		elif op == OP.FLUSH:


			txt = self.generate_txt('call vV_io_flush \n','; FLUSH opcode\n')



		elif op == OP.ENDEF:

			txt = self.generate_txt(self.var_solver.namespace.functions[self.current_scope].generate_foot(),'; End of func opcode\n')
			self.current_scope = None
		
		elif op == OP.CALL:


			Logger.log('func Call: ' + str(arg) , Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.TEXT)
				
			f_name = arg
			f_namespace = None
			f_name , f_namespace = self.var_op_solver.solve_var_namespace(arg)
			
			Logger.log('Name : '+str(f_name) + ' - namespace: '+str(f_namespace), Logger.FILE_1 | 6 , Logger.Type.DEBUG , Logger.Flag.DATA)
			
			func_obj = self.var_solver.namespace.get_function(f_name , f_namespace)
			
			if f_namespace == None:
			
				f_namespace = ''
			
			else:
			
				f_namespace += '_'
				
			
			
			Logger.log('Function access namespace : ' + func_obj.effective_namespace  , Logger.FILE_1 | 8 , Logger.Type.DEBUG , Logger.Flag.TEXT)	
			
			
			txt = self.generate_txt('call '+func_obj.effective_namespace+f_name+'\n','; Function Call\n')
	

		elif op == OP.PUSH_VAR:

			txt = self.generate_txt(self.var_op_solver.solve_push(arg,self.current_scope) , '; Var invocation\n')

			Logger.log('Pushing var : ' + str(arg) , Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.TEXT)	
			Logger.log('Assembly:\n'+txt, Logger.FILE_8 | 5 , Logger.Type.DEBUG , Logger.Flag.DATA)
			
		elif op == OP.ASSIGN:

			txt = self.generate_txt(self.var_op_solver.solve_pop(arg,self.current_scope),'; Var assignement\n')

			Logger.log('Popping var : ' + str(arg), Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.TEXT)	
			Logger.log('Assembly:\n'+txt, Logger.FILE_8 | 5 , Logger.Type.DEBUG , Logger.Flag.DATA)


			
		elif op == OP.REF_ASSIGN:
	
			txt = self.generate_txt(self.var_op_solver.solve_assign(arg[0],arg[1],self.current_scope),'; Var Ref assignement	\n')
			
			Logger.log('Var Assign : ' + str(arg) , Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.TEXT)	
			Logger.log('Assembly:\n'+txt, Logger.FILE_8 | 5 , Logger.Type.DEBUG , Logger.Flag.DATA)
			
		elif op == OP.DEREF_ASSIGN:

			#txt +=                 self.var_op_solver.solve_assign(arg[0],arg[1],self.current_scope,arg[2])
			txt = self.generate_txt(self.var_op_solver.solve_assign(arg[0],arg[1],self.current_scope,arg[2]),'; Var Deref assignement	\n')
			
			Logger.log('Var Assign : ' + str(arg) , Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.TEXT)	
			Logger.log('Assembly:\n'+txt, Logger.FILE_8 | 5 , Logger.Type.DEBUG , Logger.Flag.DATA)
			
	
		
		elif op == OP.FLUSH2:

			txt = self.generate_txt('call vV_io_flush_no_nline \n','; FLUSH opcode\n')
			
		elif op == OP.CALL_W_ARG:
		
			txt = ''	
			Logger.log('func Call with args : ' + str(arg) , Logger.FILE_1 | 5 , Logger.Type.DEBUG , Logger.Flag.TEXT)	
			
				

			i=0
			tbl = []
			size = 0
			#arg[1].reverse()
			
			f_name = arg[0]
			f_namespace = None
			
			f_name , f_namespace = self.var_op_solver.solve_var_namespace([arg[0]])
			
			Logger.log('Name : '+str(f_name) + ' - namespace: '+str(f_namespace), Logger.FILE_1 | 6 , Logger.Type.DEBUG , Logger.Flag.DATA)
			
			for assi in arg[1]:
				
				
				Logger.log(assi, Logger.FILE_1 | 8 , Logger.Type.DEBUG , Logger.Flag.DATA)
					
				
				name = assi
				namespace = None
				
				#if ':' in assi:
					
				name , namespace = self.var_op_solver.solve_var_namespace(assi)
				
				
				Logger.log('Name : '+name + 'namespace: '+str(namespace), Logger.FILE_1 | 6 , Logger.Type.DEBUG , Logger.Flag.DATA)
				
				
				
				#print name
				#print namespace
				
				#print f_name
				#print f_namespace
				
				
				
				tmp_type = self.var_solver.namespace.get_function(f_name , f_namespace).get_arg_type(i)
				
				txt += self.var_op_solver.solve_assign(assi,['vV_PUSH_ARG',tmp_type],self.current_scope)
				
				#tbl = txt.split('\n')
				#tbl.pop()
				#tbl.pop()
				#tbl.append( '	push rax\n')
				#txt = '\n'.join(tbl)
				i+= 1
				size+=1	#For now
			
			

			txt+= '	call '+self.var_solver.namespace.get_function(f_name , f_namespace).effective_namespace+f_name+'\n'
			#for j in range(i):
			
				
			#	txt+= '	pop rax\n'
			txt+= 'add rsp , '+ str(size*8)
			
			txt = self.generate_txt(txt,'; Function Call with args\n')
			Logger.log('Assembly:\n'+txt, Logger.FILE_8 | 5 , Logger.Type.DEBUG , Logger.Flag.DATA)


		elif op == OP.LOOP:

		
			txt='	vV_pop eax	;get index\n'
			txt+='	push rax	\n'
			txt+='	vV_pop eax	;get limit\n'
			txt+='	push rax	\n'	
			
			txt = self.generate_txt(txt,'; Loop check \n')	
			
		elif op == OP.ENDLOOP:
	
			txt='	inc DWORD[rsp + 8]\n'	
			txt+='	mov rax , [rsp + 8]	;get index\n'
			txt+='	mov rcx , [rsp]	;get max\n'
			txt+='	cmp eax , ecx	\n'
			txt+='	jb '+self.label_names[arg[0]]+'	\n'
			
			txt = self.generate_txt(txt,'; ; Loop init \n')
			
		elif op == OP.CLEANUP_LOOP:
	
			txt = self.generate_txt('add rsp , 16	\n','; Loop Cleanup \n')

		elif op == OP.KILL:
				
			txt='	mov ah , vV_ERR_USER_UNDEFINED\n'
			txt+='	or ax , 0	\n'
			txt+='xor rbx , rbx	\n'

		
			txt+='call vV_error		\n'
	
			txt = self.generate_txt(txt,'; User kill\n')
			
		elif op == OP.DEREF_PUSH:
		
			txt = self.generate_txt(self.var_op_solver.solve_deref_push(arg,self.current_scope) , '; Var invocation\n')
			

		self.output += txt







