import w.VM_Opcode as OP
import WErrors
import Pre_Compiler_states as State
import Opcode




class Block:

	adress = 0
	end_adress = 0
	b_type	= OP.Block_Type.NONE
	filepos = ''
	end_filepos = ''
	sub_blocks = []
	sub_blocks_inverted = []
	
	arg_adress = 0
	
	def __init__(self,adr,b_t,f_p):
	
		self.adress = adr
		self.b_type = b_t
		self.filepos = f_p
		self.sub_blocks = []
	
	
	
	
class Block_Manager:

	blocks = []
	level = 0
	
	def __init__(self):
	
		self.blocks = []
		self.level = 0
		
	
		
	def manage_block(self,op_adr,b_type,filepos):
	
		actual = Block(op_adr,b_type,filepos)
		
		if actual.b_type == OP.Block_Type.IF:
		
			self.start_block(actual)
			return []
		
		elif actual.b_type == OP.Block_Type.DO:
		
			self.start_block(actual)
			return []
			
		elif actual.b_type == OP.Block_Type.BREAK:	
		
		
			rec = 1
			while self.blocks[0-rec].b_type != OP.Block_Type.DO:
			
				rec += 1
				
			self.blocks[0-rec].sub_blocks.append(actual.adress)
			
			return []
		
			
			
			
			
		elif actual.b_type == OP.Block_Type.WHILE:
		
			assert self.blocks[-1].b_type == OP.Block_Type.DO, "block Mismatch"
			
			self.blocks[-1].arg_adress = actual.adress
			
			return [self.end_block(actual)]
			
		elif actual.b_type == OP.Block_Type.ELSE:
		
			rec = 1
			
			assert self.blocks[-1].b_type in [OP.Block_Type.IF], "Block Mismatch"
			
			
			
			#while self.blocks[0-rec].b_type != OP.Block_Type.IF:
			
			#	rec += 1
			
			if self.blocks[-1].b_type == OP.Block_Type.IF:
				
				self.blocks[-1].sub_blocks.append(actual.adress)
			
				self.blocks[-1].arg_adress = actual.adress + 1
				
				
				
				
			#For Elifs
			#elif self.blocks[-1].b_type == OP.Block_Type.IF:
			
			
			
			
			#print "hello"
			#Start a new block
			self.start_block(actual)
			return []
			
			
		elif actual.b_type == OP.Block_Type.END:
		
		
			assert self.blocks[-1].b_type in [OP.Block_Type.IF,OP.Block_Type.ELSE], "Block Mismatch"
			
			self.blocks[-1].arg_adress = actual.adress
			
			if self.blocks[-1].b_type == OP.Block_Type.IF:
			
				return [self.end_block(actual)]
				
			elif self.blocks[-1].b_type == OP.Block_Type.ELSE:
			
				loc_b = self.end_block(actual)
				
				assert self.blocks[-1].b_type == OP.Block_Type.IF, "Block Mismatch"
				
				return [loc_b ,self.end_block(actual)]
				
				
		
	def start_block(self,block):
	
		self.blocks.append(block)
		self.level +=1
		
	def end_block(self,block):
			
		b = self.blocks.pop()
		self.level-=1
		return b



class Block_Stack:

	depth = 0
	origin = []
	btype = []
	
	b_list = []
		
	o_fpos = []
	

	def __init_(self):
	
		pass
		#self.depth = 0
		#self.origin = []
		#self.type = []
		
		#self.o_fpos = []
		
		


class Context:


	main_file=0
	
	block_logic =  Block_Stack()
	
	labels = {}
	
	label_count = 0
	
	def __init_(self):
	
		#self.block_logic = Block_Stack()
		self.state = State.NOT_READY
		self.main_path= 0 
		self.current_path = 0
		self.main_file = 0
		self.current_file = 0
		self.current_line = 0
		self.current_col = 0
		#self.labels = {}
		
		
	
		
		
	def set_line(self,line):
	
		self.current_line = line
		
	def set_col(self,col):
	
		self.current_col = col
		
	def add_label(self, a, btype):
	
			
		self.labels[a] = self.label_count 
		
		self.label_count +=1
		
		
		
	def set_current_file(self,filepath):
	
		self.current_file = filepath
		
	def build_location(self):
	
		if self.current_file != 0 and self.state != State.NOT_READY:
		
			return WErrors.Location(self.current_path,self.current_file,self.current_line,self.current_col)
		
	def set_main(self):
	
		if (self.main_file != 0 )and (self.main_file != self.current_file):
			raise DuplicateMainError("test will this show?",build_location)
			
		else:
		
			self.main_file = self.current_file
			self.main_path = self.current_path
			
			
			
			
			
	def start_block(self,op_adr,op_type):
	
		self.block_logic.origin.append(op_adr)
		
		self.block_logic.btype.append(op_type)
		
		self.block_logic.o_fpos.append(self.build_location())
		
		self.block_logic.depth += 1
		
	def get_current_block_type(self):
	
		
		if self.block_logic.depth > 0:
		
			return self.block_logic.btype[-1]
			
		else:
		
			return OP.Block_Type.NONE
			
	def end_block(self):
	
	
		a = self.block_logic.origin.pop()
		
		t = self.block_logic.btype.pop()
		
		oa = self.block_logic.o_fpos.pop()
		
		self.block_logic.depth -= 1
		
		return a , t , oa



class Symbol_Solver:


	def __init__(self):
	
	
		pass
		
		
class Operation_Decoder:

	def __init__(self):
	
		
		pass
		

	def solve(str,cmd):
	
		blockinfo = 0
		opcode = Opcode.Opcode()

#Handle all possible cases in order

#01: direct mapping to Opcode

		if cmd in OP.direct_op.values():

			#print'cmd! ' + cmd
			#opcode.value = OP.direct_op.keys()[OP.direct_op.values().index(cmd)]
			opcode.value = OP.get_dir_opcode_by_string(cmd)
			
#02: direct with block structure


		elif cmd in OP.block_op.values():
		
			opcode.value=OP.get_virual_opcode_by_string(cmd)
			blockinfo = 1

#02: numeric value

		elif cmd.isdigit():
		
			opcode.value=OP.PUSH
			opcode.arg = int(cmd)			
			
#03: affixed Ops

	#03.1:prefx
	
	#03.1.1: digit_prefix
	
		elif cmd[0].isdigit():
		
			if cmd[1:] in OP.int_prefixed.values():
			
				opcode.value = OP.get_virual_opcode_by_string(cmd[1:])
				opcode.arg = int(cmd[0])
	
	#03.1.2: format prefix
		elif cmd[0] in OP.format_prefixes.keys():
			
			if cmd[1:] in OP.format_prefixed.values():

				opcode.value = OP.get_virual_opcode_by_string(cmd[1:])
				opcode.arg = OP.format_prefixes[cmd[0]]


	#03.2:suffix
		elif cmd[-1] in OP.suffixes_op.values():

			
			pass
			
			'''
			
			if cmd[-1] == '?':		#TODO: remove hardcoded Values
			
				
			
				if OP.get_virual_opcode_by_string(cmd[:-1]) in OP.prefix_allow_TEMP:
				
					opcode.value=OP.get_virual_opcode_by_string(cmd[:-1]) + 8
					opcode.arg = 0


			'''
#04: composed Ops

#-1: catch errors

		else:
		
			opcode.value=0
			
			print 'unrecognised command : ' +cmd
			
			
		return opcode,blockinfo
		
class File_Loader:

	def __init__(self):
	
		self.raw_lines = []
		
	def load_file(self,file_path):
	
		with open(file_path,"r") as file:
		
			self.raw_lines = file.readlines()
			
		return self.raw_lines






			
			
class Pre_Compiler:

	def __init__(self):
	
		self.flags = 0
	
		self.context = Context()
		
		self.stacks = Block_Stack()
		
		self.symbol_solver = Symbol_Solver()
		
		self.file_loader = File_Loader()
		
		self.operation_decoder = Operation_Decoder()
		
		
		
		
		self.block_manager = Block_Manager()
		
		
		self. op_array = []
		
		self.raw_data = []
		
	def setup_startup(self,flags):		#TODO: DEFINE FLAGS
		
		self.flags = flags
		
		self.op_array = []
		
		self.raw_data = []
		
				#---init each subcomponent---------------------------------------

		#File Loader
		
		#OP Decoder
		
		#Symbol Solver

		#Context
		
	
				#---update state--------------------------------------------------
		
		self.context.state = State.READY
		
	def start_block(self,adr,block_type,orf_adr):
	
	
		pass
	
	def manage_block(self,op):
	
		#if op.value == OP.IF:
		pass
			
		
	


	def open_main_file(self,filepath):
	
		self.context.state = State.LOADING_FILE
		
		self.raw_data = self.file_loader.load_file(filepath)
		
		self.context.current_file = filepath.split("/")[-1:]
		
		self.context.current_path = filepath.split("/")[:-1]
		
		self.context.set_line(0)
		
		self.context.set_col(0)
		
		self.context.set_main()
		
		#self.context.set_current_file(filepath.split("/")[-1:])
		
		self.context.state = State.FILE_READY
		
		

	def first_pass(self):
	
	
	#	print self.raw_data[0]
	
		self.context.state = State.ISOLATING
		line = 0
		col = 0
		buff = ''
		
		file_end = 0
		
		
		while not file_end:
		
			mode = 0
			buff=''
			#raw_input("test")
		
			while self.context.state == State.ISOLATING:
			
				r = self.raw_data[line][col]
				#print 'r'
				
				if r in OP.separator:
				
					if mode == 0:
					
						pass
						
					else:
					
						self.context.state =State.DECODING
						mode = 0
				else:
				
					if mode == 0:
					
						mode = 1
						buff+=r
						
						self.context.set_line(line)
						self.context.set_col(col)
						
						
					else:
					
						buff+=r
				
				col += 1
				if col >= len(self.raw_data[line]):
					col = 0
					line += 1
					if line >= len(self.raw_data):
					
						file_end = 1
						
						if mode == 1:
						
							self.context.state =State.DECODING
							#mode = 0
						else:
					
							break
				
					
							#----------------should get every symbol separated
				
			
			if file_end and mode == 1:
			
				break
		
			self.context.state =State.ISOLATING
			print 'o Isolated: ' +buff +'		Col: ' +str(self.context.current_col) + ' line: ' +str(self.context.current_line)
			
			
			
						#------------------Decode Phase------------------
			
			
			op, info = self.operation_decoder.solve(buff)
		
			op.adress = len(self.op_array)
			
			self.op_array.append(op)
		
			#print'  > Opcode: '+str(op.value) +'	arg :' +str(op.arg) 
			
			if info > 0:
			
			
				#print "\n"
				#print self.block_manager.level
				#tmp = self.block_manager.manage_block(op.adress,OP.block_type[op.value],self.context.build_location)
				#if len(tmp)>=1:
				#	for b in tmp:
						
				#		print b.adress , b.arg_adress
				#		print b.sub_blocks
				#		print "\n"
				#else:
				
				#	print "\n Block Start \n"
					
				#print self.block_manager.level
				#print "\n"
				
			
				
				if True:
				
					tmp = self.block_manager.manage_block(op.adress,OP.block_type[op.value],self.context.build_location)
					if len(tmp)>=1:
					
						superblock_end = tmp[0].arg_adress
				
						for b in tmp:
						
							
						
							if b.b_type in [ OP.Block_Type.IF , OP.Block_Type.ELSE ]:
							
								self.op_array[b.adress].arg = b.arg_adress
								self.context.add_label(b.arg_adress,b.b_type)
								
								for a in b.sub_blocks:
								
									self.op_array[a].arg = superblock_end
									
							elif b.b_type == OP.Block_Type.DO:
							
								self.op_array[b.arg_adress].arg = b.adress
								self.context.add_label(b.adress,b.b_type)
								
								for a in b.sub_blocks:
								
									self.op_array[a].arg = superblock_end + 1
									self.context.add_label(superblock_end + 1,b.b_type)
									
								for a in b.sub_blocks_inverted:
								
									self.op_array[a].arg = b.adress
									
							else:
							
								assert False, "FATAL: BLOCK TYPE NOT MANAGED"
							
					
					
					
					if op.value in [OP.DO,OP.END_BLOCK]:
					
						self.op_array.pop()
			
			'''					
				
				
				elif op.value == OP.IF:
				
					self.context.start_block(op.adress,OP.block_type[op.value])
					
				elif op.value == OP.ELSE:
				
					starter = self.context.get_current_block_type()
					
					assert starter in [ OP.Block_Type.IF ], "TODO: HANDLE BLOCK ERRORS"
					
					a, t, oa = self.context.end_block()
					 
					self.op_array[a].arg = op.adress + 1
					
					
					
					self.context.add_label(op.adress + 1,OP.block_type[op.value])
					
					
				
					self.context.start_block(op.adress,OP.block_type[op.value])
					
					#self.op_array.pop()
					
			#		print 'Setting adress of Op at '+str(a)+ ' to be '+str(op.adress + 1)
				
					
				elif op.value == OP.DO:
				
					self.context.start_block(op.adress,OP.block_type[op.value])
					
					self.op_array.pop()		#remove the do from Opcodes
					
				elif op.value == OP.WHILE:
				
					starter = self.context.get_current_block_type()
					
					assert starter in[ OP.Block_Type.DO] , "TODO: HANDLE BLOCK ERRORS"
					
					a, t, oa = self.context.end_block()
					
					self.op_array[-1].arg = a
					
					
					
					
					self.context.add_label(a,t)
					
					
					
					
				elif op.value == OP.END_BLOCK:
				
					starter = self.context.get_current_block_type()
					
					assert starter in [ OP.Block_Type.IF , OP.Block_Type.ELSE], "TODO: HANDLE BLOCK ERRORS"
					
					a, t, oa = self.context.end_block()
					 
					self.op_array[a].arg = op.adress
					
					
					
					
					
					
					self.context.add_label(op.adress,OP.block_type[op.value])
					
					
					
					
					
					
					self.op_array.pop()		#remove the end from Opcodes
					
					print 'Setting adress of Op at '+str(a)+ ' to be '+str(op.adress + 1)
			
			#	print'   >block boundary detected'
			
			
			
			
			
			'''
				
				
				
			print"current Op adress: " + str(len(self.op_array))
				
				
		
	 
		return self.op_array , self.context.labels














