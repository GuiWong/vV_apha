import vV.VM_Opcode as OP
import WErrors
import Pre_Compiler_states as State
import Opcode
import options as O



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
		
		
def check_numeric_format(txt):

	v = 0

	try:
		v = int(txt,10)
		return [True,v]
		
	except ValueError:
	
		pass
		
	try:
		v = int(txt,2)
		return [True,v]
		
	except ValueError:
	
		pass
		
	try:
		v = int(txt,16)
		return [True,v]
		
	except ValueError:
	
		pass
		
	if txt[0] in ["'" , '"' ] and txt[-1] == txt[0] and len(txt) <= 6:
	
		v = 0
	
		if len(txt) > 2 :
		
			v = ord(txt[1])
			
		if len(txt) >3 :
		
			v += ord(txt[2]) << 8
			
		if len(txt) >4 :
		
			v += ord(txt[3]) << 16
		if len(txt) == 6 :
		
			v += ord(txt[4]) << 24
			
			
		print "\n\n "+ str(v) + "\n\n"
			
		return [True,v]
			
	
	return [False]
	
	
		
	
	
	
	
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
			
			return [self.end_block()]
			
		elif actual.b_type in [OP.Block_Type.ELSE,OP.Block_Type.ELIF]:
		
			ret = []
			
			assert self.blocks[-1].b_type in [OP.Block_Type.IF,OP.Block_Type.ELIF], "Block Mismatch"

			
			if self.blocks[-1].b_type == OP.Block_Type.IF:
				
				self.blocks[-1].sub_blocks.append(actual.adress)
			
				self.blocks[-1].arg_adress = actual.adress + 1
				
			elif self.blocks[-1].b_type == OP.Block_Type.ELIF:
			
				self.blocks[-1].sub_blocks.append(actual.adress)
				
				assert self.blocks[-2].b_type == OP.Block_Type.IF,"block Mismatch"
				
				self.blocks[-2].sub_blocks.append(actual.adress + 1)
				
				
			if self.blocks[-1].b_type == OP.Block_Type.ELIF:
			
				ret.append(self.end_block())
			
			self.start_block(actual)
			
			return ret
			
			
		elif actual.b_type == OP.Block_Type.END:
		
		
			assert self.blocks[-1].b_type in [OP.Block_Type.IF,OP.Block_Type.ELSE], "Block Mismatch"
			
			self.blocks[-1].arg_adress = actual.adress
			
			if self.blocks[-1].b_type == OP.Block_Type.IF:
			
				return [self.end_block()]
				
			elif self.blocks[-1].b_type == OP.Block_Type.ELSE:
			
				loc_b = self.end_block()
				
				assert self.blocks[-1].b_type == OP.Block_Type.IF, "Block Mismatch"
				
				return [loc_b ,self.end_block()]
				
				
		
	def start_block(self,block):
	
		self.blocks.append(block)
		self.level +=1
		
	def end_block(self):
			
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
			raise DuplicateMainError("test will this show?",self.build_location())
			
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
		
		
class Function_Registerer:

	functions = {}
	
	def __init__(self):
	
		self.functions = {}
		
	
		
		
class Operation_Decoder:

	def __init__(self):
	
		
		pass
		

	def solve(str,cmd):
	
		blockinfo = 0
		opcode = Opcode.Opcode()
		valu= check_numeric_format(cmd)

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

		elif valu[0]:
		
			opcode.value=OP.PUSH
			opcode.arg = valu[1]		
			
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



#05: Defined keyword

		#elif cmd in 

#-1: catch errors

		else:
		
			opcode.value=0
			
			print 'unrecognised command : ' +cmd
			
			#raise WErrors.W_ERROR('acab',str(self.context.build_location()))
			
			
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
		
		self.def_context = Context()
		
		self.stacks = Block_Stack()
		
		self.symbol_solver = Symbol_Solver()
		
		
		self.function_registerer = Function_Registerer()
		
		
		
		self.file_loader = File_Loader()
		
		self.operation_decoder = Operation_Decoder()
		
		
		
		
		self.block_manager = Block_Manager()
		
		
		self.op_array = []
		
		self.raw_data = []
		
		#trying function
		
		self.def_op_array = []
		
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
		
		self.context.current_file = filepath.split("/")[-1:][0]
		
		self.context.current_path = '/'.join(filepath.split("/")[:-1])
		
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
		
		
		
		def_state = 0	#not def (0:ndef 1:start_def 2:setname 3:def 4:endef
		
		
		while not file_end:
		
			in_quotes = 0
		
			mode = 0
			buff=''
			#raw_input("test")
		
			while self.context.state == State.ISOLATING:
			
				r = self.raw_data[line][col]
				#print 'r'
				
				if r in OP.quotes.keys():
				
					if in_quotes != 0 and OP.quotes[r] == in_quotes:
				
						in_quotes = 0
					
					elif in_quotes == 0 and mode == 0:
				
						in_quotes = OP.quotes[r]
						
						self.context.set_line(line+1)
						self.context.set_col(col+1)
						
						
						
					else:
					
						raise WErrors.ParserError('Misplaced Quote', self.context.build_location())
				
				if r in OP.separator and in_quotes == 0:
				
					if mode == 0:
					
						pass
						
					else:
					
					
						self.context.state =State.DECODING
						mode = 0
						
						if buff in OP.define.keys():
						
							self.context.state=State.DEFINING
							
							'''
							print "\n"
							print def_state
							print buff
							print OP.define[buff]
							print OP.ENDEF
							print OP.DEF
							print "\n"
							'''
							
						
							#check end of def
							if def_state == 3 and OP.define[buff] == OP.ENDEF:
							
								def_state = 4
						
							elif def_state == 0 and OP.define[buff] == OP.DEF:
							
								def_state = 1
								
							else:
							
								assert False,"Definition Boundary Mismatch"
						
						
						
				else:
				
					if mode == 0:
					
						mode = 1
						buff+=r
						
						self.context.set_line(line+1)
						self.context.set_col(col+1)
						
						
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
				
				
			#if self.context.state == State.DEFINING or def_state == 2:
			
				#self.context.state =State.ISOLATING
				
			self.context.state =State.ISOLATING
				
			if def_state == 2:
			
				print "Name  "
				self.function_registerer.functions[len(self.def_op_array)] = buff
				def_state = 3
				continue
				
			if def_state == 1:
				
				
				print "Define : "
				def_state = 2
				continue
				
				
		
			
			
			if self.flags & O.VERBOSE:
				print 'o Isolated: ' +buff +'		Col: ' +str(self.context.current_col) + ' line: ' +str(self.context.current_line)
			
			
			
						#------------------Decode Phase------------------
			
			
			op, info = self.operation_decoder.solve(buff)
			
			
			if op.value == 0:
			
				if buff in self.function_registerer.functions.values():
				
					op.value = OP.CALL
					op.arg = buff
			
			
			
			
			
			
			arrptr = self.op_array
			
			contxptr = self.context	
			other_ctx = self.def_context
			
			
			
			if def_state != 0:
		
				arrptr = self.def_op_array
				contxptr = self.def_context
				other_ctx = self.context
				
			if def_state == 4:
			
				def_state = 0
				
			
				
				
			op.adress = len(arrptr)
			
			arrptr.append(op)
			
			
			
			assert op.value !=0, "Unknow Opcode Found at : " + str(self.context.build_location())
		
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
							
								arrptr[b.adress].arg = b.arg_adress
								contxptr.add_label(b.arg_adress,b.b_type)
								other_ctx.label_count +=1
								
								for a in b.sub_blocks:
								
									arrptr[a].arg = superblock_end
									
							elif b.b_type == OP.Block_Type.DO:
							
								arrptr[b.arg_adress].arg = b.adress
								contxptr.add_label(b.adress,b.b_type)
								other_ctx.label_count +=1
								
								for a in b.sub_blocks:
								
									arrptr[a].arg = superblock_end + 1
									contxptr.add_label(superblock_end + 1,b.b_type)
									other_ctx.label_count +=1
									
								for a in b.sub_blocks_inverted:
								
									arrptr[a].arg = b.adress
									
							else:
							
								assert False, "FATAL: BLOCK TYPE NOT MANAGED"
							
					
					
					
					if op.value in [OP.DO,OP.END_BLOCK]:
					
						arrptr.pop()
						
					elif op.value == OP.ELIF:
					
						tmpopcode = Opcode.Opcode()
						tmpopcode.value = OP.ELIF2
						tmpopcode.adress = len(arrptr)
						tmpopcode.arg = 0
			
						arrptr.append(tmpopcode)
			
			
				
				
			if self.flags & O.VERBOSE:	
				print"current Op adress: " + str(len(arrptr))
				
			#print def_state
				
				
		
	 	print self.def_op_array , self.function_registerer.functions
		return [self.op_array , self.context.labels] , [self.def_op_array , self.context.labels , self.function_registerer.functions]














