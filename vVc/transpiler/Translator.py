
import vV.VM_Opcode as OP
import precompiler.Opcode as Opcode
import vm.Program 

import Cleaner.Recursive_Var_Solver as R_V_S

class Translator:


	
	lib_path = 'vVc/assembly/w_runtime/'
	
	out_path = 'w_samples/assembly/'
	
	filename = ''
	
	extension = ".was"



	def __init__(self,prog,labs,var_solver,filename='output'):
	
		self.filename = filename
		self.program = prog
		self.labels = labs
		self.label_names = {}
		self.output = ''
		
		self.def_label_names = {}
		
		
		self.pc = -1
		self.sp = 0#64
		
		self.current_op = 0
		
		self.label_count = 0
		
		self.inserted = ''
		
		
		
		
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
		
		
			print self.labels[l_adr]
		
			lbid = self.labels[l_adr]
			
			
			lbname = 'wblock_'+str(lbid)

			
			
			self.label_names[l_adr] = lbname
		
	def generate_label(self,name):
	
	
		return '\n\n	'+name+':		\n\n\
;------------------------------------------------------\n\n'


	def generate_var_file(self):
	
		self.var_solver.generate_var_decl()
	
		outf= self.out_path+self.filename+'_vars.was'
		
		with open(outf, 'w+') as imp:
		
			imp.write(self.var_solver.generate_var_file())

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
			
		self.output += '\n ;OpADR: ['+str(self.pc)+']  '
			
		self.translate_opcode()
		
		
		
	def end_file(self):
	
	
		self.output += '''\
		
		ret

;Transpiled from vV with vVc version 0.0.4
		
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
			txt = '\
; PUSH opcode \n\n\
\
	vV_push '+str(arg) +' \n\
\n'


			
			
		elif op == OP.SWAP:
		
			txt = '\
; SWAP opcode \n\n\
\
\n\
	vV_swap		\n\
\n'
	
	

			
		elif op == OP.DROP:
		
			txt = '\
; DROP opcode \n\n\
\
	sub vV_sp , 4	\n'
				
			
		elif op == OP.DUP:
		
			if arg == 0:
			
				arg = 1
		
			txt = '\
; DUP opcode ('+str(arg)+')			\n\
\n\
\
	vV_dup '+str(arg)+'			\n\n'
		
									
			
		elif op == OP.ADD:
		
			txt = '\
; ADD opcode 					\n\
\n\
	mov eax , vV_2nd			\n\
	add eax , vV_top			\n\
	mov vV_2nd , eax			\n\
\n\
	vV_dec_sp 1		\n'
			
		elif op == OP.SUB:
		
			txt = '\
; SUB opcode 					\n\
\n\
	mov eax , vV_2nd			\n\
	sub eax , vV_top			\n\
	mov vV_2nd, eax			\n\
\n\
	vV_dec_sp 1		\n'
			
		elif op == OP.MUL:
		
			txt = '\
; MUL opcode 					\n\
\n\
\n\
	mov eax , vV_2nd			\n\
	mul DWORD vV_top			\n\
	mov vV_2nd , eax			\n\
\n\
	vV_dec_sp 1				\n\
						\n'
			
		elif op == OP.DIV:
		
			txt = '\
; DIV opcode 					\n\
\n\
	xor edx , edx				\n\
	mov eax , vV_2nd			\n\
	div DWORD vV_top			\n\
	mov vV_2nd , eax			\n\
\n\
	vV_dec_sp 1				\n'
	
			
		elif op == OP.NEG:
			txt = '\
; NEG opcode 					\n\
\n\
	neg DWORD vV_top			\n'
			
		elif op == OP.MOD:
		
			txt = '\
; MOD opcode 					\n\
\n\
	xor edx , edx				\n\
	mov eax , vV_2nd			\n\
	div DWORD vV_top			\n\
	mov vV_2nd , edx			\n\
\n\
	sub r15 , 4				\n'
			
		
		
		elif op == OP.LSH:
		
			txt = '\
; LSH opcode 					\n\
\n\
	shl DWORD vV_top , 1			\n'
			
		elif op == OP.RSH:
		
			txt = '\
; RSH opcode 					\n\
\n\
	shr DWORD vV_top , 1			\n'
		
		elif op == OP.NOT:
		
			txt = '\
; NOT opcode 					\n\
\n\
	not DWORD vV_top			\n'
			
		elif op == OP.OR:
		
			txt = '\
; AND opcode					\n\
\n\
	mov eax , vV_top			\n\
	or DWORD vV_2nd , eax			\n\
\n\
	vV_dec_sp 1				\n'
			

		elif op == OP.AND:
		
			txt = '\
; OR opcode					\n\
\n\
	mov eax , vV_top			\n\
	and DWORD vV_2nd , eax			\n\
\n\
	vV_dec_sp 1				\n'
			
		elif op == OP.XOR:
		
			txt = '\
; XOR opcode					\n\
\n\
	mov eax , vV_top			\n\
	xor DWORD vV_2nd , eax			\n\
\n\
	vV_dec_sp 1				\n'
			
			
		elif op == OP.LESS:		#WARNING TODO WARNING
						#very fragile code because
						#of hardcoded jumps
			txt = '\
; LESS opcode					\n\
\n\
	mov eax , vV_top			\n\
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
	
				
		elif op == OP.MORE:
		
			txt = '\
; MORE opcode					\n\
\n\
	mov eax , vV_top			\n\
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
			
			
		elif op == OP.EQUAL:
		
			txt = '\
; EQUAL opcode					\n\
\n\
	mov eax , vV_top			\n\
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
				
				
		elif op == OP.IF:		#Becomes a jump
			txt = '\
; IF opcode					\n\
\n\
	vV_dec_sp 1			\n\
	or DWORD[vV_sp] , 0			\n\
	je '+self.label_names[arg]+'	\n'
				
				
		elif op in [ OP.ELSE ]:		#Becomes a jump
			txt = '\
; ELIF opcode					\n\
\n\
	jmp '+self.label_names[arg]+'	\n'
	
	

	
			
		elif op == OP.WHILE:
		
			txt = '\
; WHILE opcode					\n\
\n\
	vV_dec_sp 1				\n\
	or DWORD[vV_sp] , 0			\n\
	jne '+self.label_names[arg]+'		\n'
	
		elif op == OP.BREAK:
		
			txt = '\
; Break opcode					\n\
\n\
	jmp '+self.label_names[arg]+'		\n'	
			

			
		elif op== OP.GET:
		
			txt = '\
; GET opcode ('+str(arg)+')			\n\
\n'		
			if arg == OP.Format.NONE:
			
				txt+='\
	call vV_io_get_default			\n\
						\n'
			
			elif arg == OP.Format.DEC:
			
				txt+='\
	mov r10d , vV_ascii_as_dec		\n\
	call vV_io_get				\n\
						\n'
						
			elif arg == OP.Format.HEX:
			
				txt+='\
	mov r10d , vV_ascii_as_hex		\n\
	call vV_io_get				\n\
						\n'
						
			elif arg == OP.Format.BIN:
			
				txt+='\
	mov r10d , vV_ascii_as_bin		\n\
	call vV_io_get				\n\
						\n'	
						
														
			elif arg == OP.Format.CHR:
			
				txt+='\
		\n\
	call vV_io_get_char				\n\
						\n'
						
			elif arg == OP.Format.PCHR:
			
				txt+='\
								\n\
	call vV_io_get_packed_char				\n\
						\n'
						
	
			


		elif op == OP.OUT:

			txt = '\
; OUT opcode ('+str(arg)+')			\n\
\n'

			if arg == OP.Format.NONE:
			
				txt+='\
	call vV_io_out_default			\n\
						\n'
			
			elif arg == OP.Format.DEC:
			
				txt+='\
	mov r10d , vV_FORMAT_DEC		\n\
	call vV_io_out				\n\
						\n'
						
			elif arg == OP.Format.HEX:
			
				txt+='\
	mov r10d , vV_FORMAT_HEX		\n\
	call vV_io_out				\n\
						\n'
						
			elif arg == OP.Format.BIN:
			
				txt+='\
	mov r10d , vV_FORMAT_BIN		\n\
	call vV_io_out				\n\
						\n'	
						
						
						
			elif arg == OP.Format.CHR:
			
				txt+='\
		\n\
	call vV_io_out_char				\n\
						\n'
						
			elif arg == OP.Format.PCHR:
			
				txt+='\
								\n\
	call vV_io_out_packed_char				\n\
						\n'
						
						
			else:
			
				assert False, " FATAL ERROR, Format for out not valid"



		elif op == OP.BUFF_OUT:

			txt = '\
; BUFF_OUT opcode ('+str(arg)+')			\n\
\n'

			if arg == OP.Format.NONE:
			
				txt+='\
	call vV_io_out_buffer_default			\n\
						\n'
			
			elif arg == OP.Format.DEC:
			
				txt+='\
	mov r10d , vV_FORMAT_DEC		\n\
	call vV_io_out_buffer				\n\
						\n'
						
			elif arg == OP.Format.HEX:
			
				txt+='\
	mov r10d , vV_FORMAT_HEX		\n\
	call vV_io_out_buffer				\n\
						\n'
						
			elif arg == OP.Format.BIN:
			
				txt+='\
	mov r10d , vV_FORMAT_BIN		\n\
	call vV_io_out_buffer				\n\
						\n'	
						
						
			elif arg == OP.Format.CHR:
			
				txt+='\
\n\
	call vV_io_out_char_buffer			\n\
						\n'
						
			elif arg == OP.Format.PCHR:
			
				txt+='\
\n\
	call vV_io_out_packed_char_buffer				\n\
						\n'
						
			else:
			
				assert False, " FATAL ERROR, Format for out not valid"


		elif op == OP.FLUSH:

			txt = '\
; FLUSH opcode					\n\
\n\
		call vV_io_flush	\n'



		elif op == OP.ENDEF:

			txt = '\
; End of func opcode					\n\
\n'
			txt += self.var_solver.namespace.functions[self.current_scope].generate_foot()
			self.current_scope = None
		
		elif op == OP.CALL:

			txt = '\
; Function Call					\n\
\n\
		call '+arg[0]+'			\n'
	

		elif op == OP.PUSH_VAR:

			txt = '\
; Var invocation					\n\
\n'
			print arg
			print '\n-------------------------'
			print self.var_op_solver.solve_push(arg,self.current_scope)
			print '-------------------------\n'
			
			
			txt += self.var_op_solver.solve_push(arg,self.current_scope)
			#assert False, 'breakpoint'
			#txt += self.var_solver.push_var(arg,self.current_scope)
			#assert False ,"TODO: MANAGE VARSOLVING"
		
		elif op == OP.ASSIGN:

			txt = '\
; Var assignement					\n\
\n'
			print arg
			print '\n-------------------------'
			print self.var_op_solver.solve_pop(arg,self.current_scope)
			print '-------------------------\n'
			
			
			
			txt += self.var_op_solver.solve_pop(arg,self.current_scope)
			#txt += self.var_solver.pop_var(arg,self.current_scope)
		
			#assert False ,"TODO: MANAGE VARSOLVING"
			
		elif op == OP.REF_ASSIGN:

			txt = '\
; Var Ref assignement					\n\
\n'
			print '#########################\n\n'
			print op
			print arg
			print '#########################\n\n'
			
			print '\n-------------------------'
			print self.var_op_solver.solve_assign(arg[0],arg[1],self.current_scope)
			print '-------------------------'
			#print self.rec_var_solver.solve_var_name(arg[1],self.current_scope)
			#print self.rec_var_solver.solve_indexing(arg[1])
			#print '-------------------------\n'
			
			#assert False , 'Op Unimplemented'
			#txt += self.var_solver.ref_assign(arg[0],arg[1],self.current_scope)
			txt += self.var_op_solver.solve_assign(arg[0],arg[1],self.current_scope)
		
		elif op == OP.FLUSH2:

			txt = '\
; FLUSH opcode					\n\
\n\
		call vV_io_flush_no_nline	\n'

	
		elif op == OP.CALL_W_ARG:
			txt = '\
; Function Call with args					\n'		
			print arg
			i=0
			tbl = []
			size = 0
			arg[1].reverse()
			for assi in arg[1]:
				print assi
				#print self.var_solver.ref_assign(assi,['vV_PUSH_ARG',self.var_solver.namespace.functions[arg[0]].get_arg_type(i)],self.current_scope)
				txt += self.var_solver.ref_assign(assi,['vV_PUSH_ARG',self.var_solver.namespace.functions[arg[0]].get_arg_type(i)],self.current_scope)
				tbl = txt.split('\n')
				tbl.pop()
				tbl.pop()
				tbl.append( '	push rax\n')
				txt = '\n'.join(tbl)
				i+= 1
				size+=1	#For now
			
			
			#print txt
			
			txt+= '	call '+arg[0]+'\n'
			#for j in range(i):
			
				
			#	txt+= '	pop rax\n'
			txt+= 'add rsp , '+ str(size*8)
			#assert False , 'Unimplementaed'

		elif op == OP.LOOP:

			txt = '\
; Loop init 					\n'		
			txt+='	vV_pop eax	;get index\n'
			txt+='	push rax	\n'
			txt+='	vV_pop eax	;get limit\n'
			txt+='	push rax	\n'		
			
		elif op == OP.ENDLOOP:

			txt = '\
; Loop check 					\n'	
			txt+='	inc DWORD[rsp + 8]\n'	
			txt+='	mov rax , [rsp + 8]	;get index\n'
			txt+='	mov rcx , [rsp]	;get max\n'
			txt+='	cmp eax , ecx	\n'
			txt+='	jbe '+self.label_names[arg[0]]+'	\n'
			
		elif op == OP.CLEANUP_LOOP:

			txt = '\
; Loop Cleanup 					\n'		
			txt+='	add rsp , 16	\n'	
	

		self.output += txt







