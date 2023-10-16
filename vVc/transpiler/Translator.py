
import w.VM_Opcode as OP
import precompiler.Opcode as Opcode
import vm.Program 



class Translator:


	
	lib_path = 'vVc/assembly/w_runtime/'
	
	out_path = 'w_samples/'
	
	filename = ''
	
	extension = ".was"



	def __init__(self,prog,labs,filename='output'):
	
		self.filename = filename
		self.program = prog
		self.labels = labs
		self.label_names = {}
		self.output = ''
		
		
		self.pc = -1
		self.sp = 0#64
		
		self.current_op = 0
		
		self.label_count = 0
		
	def fetch(self):
	
		self.pc += 1
		self.current_op = self.program.code[self.pc]
		
	def generate_label_names(self):
	
	
		for l_adr in self.labels.keys():
		
			lbid = self.labels[l_adr]
			
			
			lbname = 'wblock_'+str(lbid)

			
			
			self.label_names[l_adr] = lbname
		
	def generate_label(self,name):
	
	
		return '\n\n	'+name+':		\n\n\
;------------------------------------------------------\n\n'

	def generate_header(self):
	
	
		self.output+= '\
%include "'+self.lib_path+'vV_defines.asm"		\n\
%include "'+self.lib_path+'vV_io.asm"			\n\
%include "'+self.lib_path+'w_runtime.asm"		\n'


		self.output+= '''

global w_entry_point



segment .text 




w_entry_point:


	mov rbp, rsp			;Setup Stack Frame
	
	'''
			
		
	
	def step_compile(self):
	
	
	
		
	
		self.fetch()
		
		if self.pc in self.labels.keys():
		
			self.output += self.generate_label(self.label_names[self.pc])
			
		self.output += '\n ;OpADR: ('+str(self.pc)+')\n'
			
		self.translate_opcode()
		
		
		
	def end_file(self):
	
	
		self.output += '''\
		
		ret

;Transpiled from vV with vVc version 0.0.1.5
		
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
		
					
		elif op == OP.OUT:

			txt = '\
; OUT opcode ('+str(arg)+')			\n\
\n\
						\n\
	call wio_out				\n\
						\n'	
	
				
			
		elif op == OP.ADD:
		
			txt = '\
; ADD opcode 					\n\
\n\
	mov eax , [r15 - 8]			\n\
	add eax , [r15-4]			\n\
	mov [r15-8] , eax			\n\
\n\
	sub r15 , 4		\n'
			
		elif op == OP.SUB:
		
			txt = '\
; SUB opcode 					\n\
\n\
	mov eax , [r15 - 8]			\n\
	add eax , [r15-4]			\n\
	mov [r15-8] , eax			\n\
\n\
	sub r15 , 4		\n'
			
		elif op == OP.MUL:
		
			txt = '\
; MUL opcode 					\n\
\n\
\n\
	mov eax , [r15 - 8]			\n\
	mul DWORD[r15-4]			\n\
	mov [r15-8] , eax			\n\
\n\
	sub r15 , 4				\n\
						\n'
			
		elif op == OP.DIV:
		
			txt = '\
; DIV opcode 					\n\
\n\
	xor edx , edx				\n\
	mov eax , [r15 - 8]			\n\
	div DWORD[r15-4]			\n\
	mov [r15-8] , eax			\n\
\n\
	sub r15 , 4				\n'
	
			
		elif op == OP.NEG:
			txt = '\
; NOT opcode 					\n\
\n\
	neg DWORD[r15-4]			\n'
			
		elif op == OP.MOD:
		
			txt = '\
; MOD opcode 					\n\
\n\
	xor edx , edx				\n\
	mov eax , [r15 - 8]			\n\
	div DWORD[r15-4]			\n\
	mov [r15-8] , edx			\n\
\n\
	sub r15 , 4				\n'
			
		
		
		elif op == OP.LSH:
		
			txt = '\
; LSH opcode 					\n\
\n\
	shl DWORD[r15-4] , 1			\n'
			
		elif op == OP.RSH:
		
			txt = '\
; RSH opcode 					\n\
\n\
	shr DWORD[r15-4] , 1			\n'
		
		elif op == OP.NOT:
		
			txt = '\
; NOT opcode 					\n\
\n\
	not DWORD[r15-4]			\n'
			
		elif op == OP.OR:
		
			txt = '\
; AND opcode					\n\
\n\
	mov eax , [r15-4]			\n\
	or DWORD[r15-8] , eax			\n\
\n\
	sub r15 , 4				\n'
			

		elif op == OP.AND:
		
			txt = '\
; OR opcode					\n\
\n\
	mov eax , [r15-4]			\n\
	and DWORD[r15-8] , eax			\n\
\n\
	sub r15 , 4				\n'
			
		elif op == OP.XOR:
		
			txt = '\
; XOR opcode					\n\
\n\
	mov eax , [r15-4]			\n\
	xor DWORD[r15-8] , eax			\n\
\n\
	sub r15 , 4				\n'
			
			
		elif op == OP.LESS:		#WARNING TODO WARNING
						#very fragile code because
						#of hardcoded jumps
			txt = '\
; LESS opcode					\n\
\n\
	mov eax , [r15-4]			\n\
	cmp DWORD[r15-8] , eax			\n\
\n\
	jae short 0xb				\n\
\n\
			mov DWORD[r15-8] , -1	\n\
\n\
	jmp short 0x9				\n\
\n\
			mov DWORD[r15-8] , 0	\n\
\n\
	sub r15 , 4				\n'
	
				
		elif op == OP.MORE:
		
			txt = '\
; MORE opcode					\n\
\n\
	mov eax , [r15-4]			\n\
	cmp DWORD[r15-8] , eax			\n\
\n\
	jbe short 0xb				\n\
\n\
			mov DWORD[r15-8] , -1	\n\
\n\
	jmp short 0x9				\n\
\n\
			mov DWORD[r15-8] , 0	\n\
\n\
	sub r15 , 4				\n'
			
			
		elif op == OP.EQUAL:
		
			txt = '\
; EQUAL opcode					\n\
\n\
	mov eax , [r15-4]			\n\
	cmp DWORD[r15-8] , eax			\n\
\n\
	jnz short 0xb				\n\
\n\
			mov DWORD[r15-8] , -1	\n\
\n\
	jmp short 0x9				\n\
\n\
			mov DWORD[r15-8] , 0	\n\
\n\
	sub r15 , 4				\n'
				
				
		elif op == OP.IF:		#Becomes a jump
			txt = '\
; IF opcode					\n\
\n\
	sub r15 , 4				\n\
	xor DWORD[r15] , -1			\n\
	jne '+self.label_names[arg]+'	\n'
				
				
		elif op in [ OP.ELSE]:		#Becomes a jump
			txt = '\
; ELSE opcode					\n\
\n\
	jmp '+self.label_names[arg]+'	\n'
			
		elif op == OP.WHILE:
		
			txt = '\
; WHILE opcode					\n\
\n\
	sub r15 , 4				\n\
	or DWORD[r15] , 0			\n\
	jne '+self.label_names[arg]+'	\n'
			

			



		elif op == OP.GET:

			txt = '\
; OUT opcode ('+str(arg)+')			\n\
\n\
						\n\
	call wio_get				\n\
						\n'











		self.output += txt







