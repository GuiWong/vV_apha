import vV.VM_Opcode as OP
import WErrors
import Pre_Compiler_states as State
import Opcode
import options as O

import VarUpdate.Code_Namespace as C_NS
import VarUpdate.vV_Variable as vV_Var
import VarUpdate.Type_Checker as Type_Checker



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
		v = int(txt[0],10)
		
	except ValueError:
		
		if txt[0] not in ["'" , '"' ]:
			return [False]
			
		else:
		
			v=0
	

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
			
			
		#print "\n\n "+ str(v) + "\n\n"
			
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
		
		
	def decode(self,token):
	
		s_arg = []	#square brackets arguments
		r_arg = []	#round brackets arguments
		cmd = ''
		valid = True
		
		if token[0] == OP.index_op[OP.SQRBRACKETL] and token[-1] not in OP.grouping_chars:		#Case of starting brackets
		
		
			tmp = token.split(OP.index_op[OP.SQRBRACKETR])
			
			cmd = tmp[-1]
			
			for a in tmp[:-1]:
			
				if a[0] != OP.index_op[OP.SQRBRACKETL]:
				
					valid = False
					
				else:
				
					s_arg.append(a[1:])
			
			
		elif token[-1] == OP.index_op[OP.SQRBRACKETR] and token[0] not in OP.grouping_chars:	#Case of closing brackets
		
		
			tmp = token.split(OP.index_op[OP.SQRBRACKETL])
			
			cmd = tmp[0]
			
			for a in tmp[1:]:
			
				if a[-1] != OP.index_op[OP.SQRBRACKETR]:
				
					valid = False
					
				else:
				
					s_arg.append(a[:-1])
			
		else:
		
			return [False]
			
			
		return [valid , cmd , s_arg , r_arg]
		
		
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
		
		
		if cmd == "b=":
		
			print valu

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
		elif cmd[0] in OP.format_prefixes.keys() and cmd[1:] in OP.format_prefixed.values():
			
			#if cmd[1:] in OP.format_prefixed.values():

			opcode.value = OP.get_virual_opcode_by_string(cmd[1:])	#ERROR WAS HERE(NEED AND FOR COND)
			opcode.arg = OP.format_prefixes[cmd[0]]


	#03.2:suffix
		elif cmd[-1] in OP.suffixes_op.values():

			
			pass
			
			
		elif cmd[-1] in OP.ref_suffix:
		
		
			opcode.value = OP.ref_suffix[cmd[-1]]
			
			opcode.arg = cmd[:-1]
			
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
			
			#print 'unrecognised command : ' +cmd
			
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
		
		
		self.context.labels = {}
		
		self.def_context.labels = {}
		
		self.stacks = Block_Stack()
		
		self.symbol_solver = Symbol_Solver()
		
		
		self.function_registerer = Function_Registerer()
		self.namespace_manager = C_NS.NameSpace_Manager()
		self.type_checker = Type_Checker.Type_Checker()
		
		
		
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
		
		
		
		
		current_func_name = ''
		var_def_state = 0
		
		current_var_scope = 0
		current_var_type = 0
		
		
		
		current_var_value = 0
		current_var_init = False
		
		
		while not file_end:
		
			in_quotes = 0
		
			mode = 0
			buff=''
			#raw_input("test")
		
			while self.context.state == State.ISOLATING:
			
				r = self.raw_data[line][col]
				#print 'r'
				
				if r in OP.comment and in_quotes == 0:
				
				
					if mode == 0:
					
						col=0
						line+=1
						#continue
						
					elif mode == 1:
				
						self.context.state =State.DECODING
						mode = 0
						col=0
						line+=1
						
					if line >= len(self.raw_data):
					
						file_end = True
						break
					continue
					
				
				if r in OP.quotes.keys():
				
					if in_quotes != 0 and OP.quotes[r] == in_quotes:
				
						in_quotes = 0
					
					elif in_quotes == 0 and mode == 0:
				
						in_quotes = OP.quotes[r]
						
						self.context.set_line(line+1)
						self.context.set_col(col+1)
						
						
						
					else:
					
						buff+=r
					
						#raise WErrors.ParserError('Misplaced Quote', self.context.build_location())
				
				if r in OP.separator and in_quotes == 0:
				
					if mode == 0:
					
						pass
						
					else:
					
					
						self.context.state =State.DECODING
						mode = 0
						
						if buff in OP.define.keys():
						
						
							assert var_def_state == 0 , " RAISE UNFINISHED VAR DEFINITION"
						
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
							
							
								#print "endef found "+ str(self.context.build_location())
							
								def_state = 4
						
							elif def_state == 0 and OP.define[buff] == OP.DEF:
							
								#print "def found "+ str(self.context.build_location())
								#print buff
							
								def_state = 1
								
							else:
							
								assert False,"Definition Boundary Mismatch "+ str(self.context.build_location()) +" "+ str(def_state)+ " " +str(OP.define[buff]) + " " + str(var_def_state)
								
#----------------------------------Var Update--------------------------------------------------------------------------------------------


						elif buff in OP.var_define:
						
							#assert var_def_state == 0 , "ILLEGAL LOCATION FOR SCOPE KEYWORD "+ str(self.context.build_location())

							if OP.var_define[buff] == OP.IMPLICIT:
							
								if def_state == 0:
								
									current_var_scope = OP.GLOBAL
									
								elif def_state >=2:
								
									current_var_scope = OP.GLOBAL
									
								else:
								
									assert False , "UNABLE TO define variable scope "+ str(self.context.build_location())

								
								var_def_state = 1
								

							else:
							
								current_var_scope = OP.var_define[buff]
								
								var_def_state = 1
								
								
							self.context.state=State.VAR_DEFINING
							
							
							print "Begin var init..."
							

								
							
						elif buff in OP.var_type:
						
						
							if var_def_state == 0:			#--> implicit scope
							
								
							
								if def_state == 0:
								
									current_var_scope = OP.GLOBAL
									
								elif def_state >=2:
								
									current_var_scope = OP.GLOBAL
						
							#current_var_type = OP.var_type[buff]
							
							
							
							try:
								current_var_type = vV_Var.build_type(OP.var_type[buff])
							except WErrors.InvalidType:
							
								assert False, "Unimplemented Type : "+self.context.build_location()
							
							
							print "setting var type..."
							
							self.context.state = State.VAR_DEFINING
							
							var_def_state = 2	#Scoped, Typed
								
							




#----------------------------------Var Update--------------------------------------------------------------------------------------------
						
						
						
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
			
			
			
		#	print "\n Isolated: " + buff + " defState: "+str(def_state) +" var_def_sate: "+str(var_def_state)
			
			if file_end and mode == 1:
			
				break
				
				
			#if self.context.state == State.DEFINING or def_state == 2:
			
				#self.context.state =State.ISOLATING
				
			if self.context.state == State.VAR_DEFINING:		#v0.0.4
				
				self.context.state =State.ISOLATING
				continue
				
			self.context.state =State.ISOLATING
				
			if def_state == 2:
			
		#		print " Function Name : "+buff+" "+str(self.context.build_location())
		
				for c in buff:
				
					assert c not in OP.forbiden_chars , "FORBIDEN CHAR IN FUNC NAME"
				
				
				self.function_registerer.functions[len(self.def_op_array)] = buff
				
				if self.namespace_manager.define_function(buff) != 0:	#v0.0.4
				
					assert False , "RAISE DEFINITION ERROR"		#v0.0.4
					
				current_func_name = buff					#v0.0.4
				
				def_state = 3
				continue
				
			if def_state == 1:
				
				
		#		print " Function Definition: "+buff+" "+str(self.context.build_location())
				
				def_state = 2
				continue


#----------------------------------Var Update--------------------------------------------------------------------------------------------				
				
			#if var_def_state != 0:
			
			
			
			
			if var_def_state == 1:		#scoped, untyped
			
			
				print "value found before type, defining it..."
			
				tmpre = check_numeric_format(buff) 
				
		#		print buff,tmpre
				
				if tmpre[0]:
				
					current_var_type = vV_Var.vV_Int_Type()
					current_var_value = tmpre[1]
					current_var_init = True
					
				else:
				
					if buff[-1] == OP.index_op[OP.SQRBRACKETR]:
					
					
						decoded = self.symbol_solver.decode(buff)
						
						
						tmp_type = 0
						tmp_val = []
						tmp_size = []
						tmp_dim = 0
						tmp_is_def = False
						tmp_is_init = False
						
						
						print decoded
						assert decoded[0] , "Error While Trying to decode Type: " + buff +" at: "+ str(self.context.build_location())
						
						
						if decoded[1] in OP.var_type:
						
						
						
						
							
							tmp_type = vV_Var.build_type(OP.var_type[decoded[1]])
							
							
							for dim in decoded[2]:
							
								assert dim.isdigit() , "NOT a numeric value in indexing operation ("+decoded[2][0]+") : " +str(self.context.build_location())
								
								tmp_size.append(int(dim))
								tmp_dim += 1
							
							tmp_is_def = True
							tmp_is_init = False
						
							
						elif decoded[1] == "None":	#TODO: define a return value for only brackets
						
						
						
							assert False , "inimplemented array initialisation  : " +str(self.context.build_location())
						
						
							
						else:
						
						
							assert False , "Unrecognised type ("+decoded[1]+") : " +str(self.context.build_location())
						
						
						
						
						print current_var_type
						print tmp_dim
						print tmp_size
						
						current_var_type = vV_Var.vV_Array_Type(tmp_type,tmp_dim,tmp_size )
						current_var_value =tmp_val
						current_var_init = tmp_is_init
							
							
					#	else:
						
					#		assert False , "NOT IMPLEMENTED (probably trying a multi dimentionnal array at "+str(self.context.build_location())+")"
							
						
						print current_var_type
						
						print current_var_type.calc_size()
						
					
						#assert False , "NEED TO IMPLEMENT BRACKET DECODING"
						
					
					else:
					
						assert False , "RAISE UNKNOWN VALUE TYPE : " +  str(self.context.build_location())
					
					
				var_def_state = 3	#scoped, typed, has value
					
					
				continue
				
				
				
			elif var_def_state >=2:#for now, debugging	#Scoped and typed, and inited
			
			
				vlu = check_numeric_format(buff) 
				if var_def_state == 2 and vlu[0]:		#Uninitialized
				
					print "setting var value"
				
					
		#			print buff,vlu
				

					current_var_value = vlu[1]
					current_var_init = True
					
					var_def_state = 3
					continue
					
				else:
			
			
			
					print "defining var name: " +buff
					
					for c in buff:
				
						assert c not in OP.forbiden_chars , "FORBIDEN CHAR IN FUNC NAME"		#May need to allow brackets, or pre-process str to extract info
					
					var_name = buff
					varo = vV_Var.vV_Variable(var_name,current_var_scope,current_var_type,current_var_init,current_var_value)
				
				#print"test12"
				#print varo.name
				#print varo.var_type
				#print varo.scope
				#print current_var_scope
				#print varo.init_value
				
				
				
				
				if current_var_scope == OP.GLOBAL:
				
					if self.namespace_manager.define_global(varo)== 0:
				
		#				print "\n",varo,"\n"
						pass
					
					else:
				
						assert False , "RAISE VAR NAME ERROR TYPE" +str(self.context.current_line) + str(self.context.build_location())
						
				elif current_var_scope == OP.LOCAL:
				
					if self.namespace_manager.functions[current_func_name].add_local_var(varo)==0:
				
		#				print varo
						pass
					
					else:
				
						assert False , "RAISE VAR NAME ERROR TYPE" +str(self.context.current_line) + str(self.context.build_location())
				
				var_def_state = 0
				
				current_var_scope = 0
				current_var_type = 0
				current_var_init = False
				current_var_value = 0
				
				
				print "Var should be saved"

				continue


			'''
				
			elif var_def_state == 2:		#scoped, typed
			
			
				print "can be name or value"
			
				tmpre2 = check_numeric_format(buff) 
				
				print buff,tmpre2
				
				if tmpre2[0]:
				
					current_var_type = OP.UINT_32
					current_var_value = tmpre2[1]
					current_var_init = True
					
				else:
				
					assert False , "RAISE UNKNOWN VALUE TYPE" + str(self.context.build_location())
					
					
				var_def_state = 3	#scoped, typed, has value
					
					
				continue
				
				
			'''

#----------------------------------Var Update--------------------------------------------------------------------------------------------				
		
			
		
			if self.flags & O.VERBOSE:
			
				print 'o Isolated: ' +buff +'		Col: ' +str(self.context.current_col) + ' line: ' +str(self.context.current_line)
			
			
			
						#------------------Decode Phase------------------
			
			
			op, info = self.operation_decoder.solve(buff)
			
			#if op.value == OP.DO:
			
			#	print "do :" +str(self.context.build_location())
			
			#if op.value == OP.WHILE:
			
			#	print "while :" +str(self.context.build_location())
			
			
			if op.value == 0:
			
				if buff in self.function_registerer.functions.values():
				
					op.value = OP.CALL
					op.arg = [buff]
	
#--------------------------Var Update------------------------------------------------------------		
			
				elif def_state == 3 and buff in self.namespace_manager.functions[current_func_name].local_vars:		#00.0.4
				
				
					op.value = OP.PUSH_VAR
					op.arg = [buff]
					
					print self.type_checker.result_type(None,self.namespace_manager.functions[current_func_name].local_vars[buff].var_type,[OP.PUSH_VAR,[]])
					
					
					print "push local var "+op.arg[0]
					
				
				elif buff in self.namespace_manager.global_vars:		#00.0.4
				
				
					op.value = OP.PUSH_VAR
					op.arg = [buff]
					
					print self.type_checker.result_type(None,self.namespace_manager.global_vars[buff].var_type,[OP.PUSH_VAR,[]])
					
					print "push global var "+op.arg[0]
					
					
				elif buff[0] == OP.index_op[OP.SQRBRACKETL]:
				
				
				
				
				
					decoded = self.symbol_solver.decode(buff)
					
					print decoded
					assert decoded[0] , "Error While Trying to decode Type: " + buff +" at: "+ str(self.context.build_location())
						
					valu = []
					
					for c in decoded[2]:
					
					
						if len(c) == 0:
							
							print "empty bracket"
							valu.append("pop")
							
							
						else:
							assert c.isdigit() , "Error, non numeric index ("+c+") at: "+ str(self.context.build_location())
						
							valu.append(int(c))
						
					valu.reverse()
					
					
					
						
						
					if def_state == 3 and decoded[1] in self.namespace_manager.functions[current_func_name].local_vars:
					
					
						op.value = OP.PUSH_VAR
						op.arg = [decoded[1],valu]
						
						
						#print self.type_checker.result_type(None,vV_Var.vV_Array_Type(0,1,[10]),[OP.PUSH_VAR,valu])
						
						print self.type_checker.result_type(None,self.namespace_manager.functions[current_func_name].local_vars[decoded[1]].var_type,[OP.PUSH_VAR,valu])
						
						
					elif decoded[1] in self.namespace_manager.global_vars:
					
					
						op.value = OP.PUSH_VAR
						op.arg = [decoded[1],valu]
						
						#print self.type_checker.result_type(None,vV_Var.vV_Array_Type(vV_Var.vV_Int_Type(),1,[10]),[OP.PUSH_VAR,valu])
						
						print self.type_checker.result_type(None,self.namespace_manager.global_vars[decoded[1]].var_type,[OP.PUSH_VAR,valu])
				
					print "array reading with args:"
					print op.arg
						
					#assert False , "NEED TO IMPLEMENT BRAQUET DECODING"
					
					
					
					
					
					
					
				else:
				
					assert False , "Unrecognised Opcode "+str(op.value) + " " +buff+" " +str(self.context.build_location())
					
					
					
			if op.value == OP.ASSIGN:
			
			
				print "assign potential var "+op.arg
				#op.arg = [op.arg]
				
				if def_state == 3 and op.arg in self.namespace_manager.functions[current_func_name].local_vars:
				
					op.arg = [op.arg]
					#op.arg = 
					
					#print "\n-----------------------\n\n"								
					#print self.namespace_manager.functions[current_func_name].solve_var(op.arg)
					#print "\n-----------------------\n\n"
					
				elif op.arg in self.namespace_manager.global_vars:
				
					op.arg = [op.arg]
					
					
				elif op.arg[0] == OP.index_op[OP.SQRBRACKETL]:
				

					decoded = self.symbol_solver.decode(buff)
					
					print decoded
					assert decoded[0] , "Error While Trying to decode Var Assignement" + buff +" at: "+ str(self.context.build_location())
						
					valu = []
					
					varname = decoded[1][:-1]
					
					for c in decoded[2]:
					
					
						if len(c) == 0:
							
							print "empty bracket"
							valu.append("pop")
							
							
						else:
							assert c.isdigit() , "Error, non numeric index ("+c+") at: "+ str(self.context.build_location())
						
							valu.append(int(c))
						
					#valu.append(varname)
					valu.reverse()
					
					
					if ( def_state == 3 and varname in self.namespace_manager.functions[current_func_name].local_vars ) or varname in self.namespace_manager.global_vars:
				
						op.arg = [varname,valu]
					#op.arg = 
					
					#print "\n-----------------------\n\n"								
					#print self.namespace_manager.functions[current_func_name].solve_var(op.arg)
					#print "\n-----------------------\n\n"
					
					else:
				
						assert False , "Undefined var for this scope "+str(self.context.build_location())
					
						
					
				else:
				
					assert False , "Undefined var for this scope "+str(self.context.build_location())
			
			
#--------------------------------------------------------------------------------------------------------			
			
			
			
			
			arrptr = 0
			
			contxptr = 0	
			other_ctx = 0
			
			if def_state != 0:
		
				arrptr = self.def_op_array
				#contxptr = self.def_context
				#other_ctx = self.context
				
			else:
			
				arrptr = self.op_array
			
				#contxptr = self.context	
				#other_ctx = self.def_context
				
			if def_state == 4:
			
			
	#			print "Finishing func"
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
					
						#print tmp
						superblock_end = tmp[0].arg_adress
				
						for b in tmp:
						
							
						
							if b.b_type in [ OP.Block_Type.IF , OP.Block_Type.ELSE ]:
							
								arrptr[b.adress].arg = b.arg_adress
								if def_state != 0:
									self.def_context.add_label(b.arg_adress,b.b_type)
									self.context.label_count +=1
								else:
									self.context.add_label(b.arg_adress,b.b_type)
									self.def_context.label_count +=1
								
								for a in b.sub_blocks:
								
									arrptr[a].arg = superblock_end
									
							elif b.b_type == OP.Block_Type.END:
							
							
								
							
								arrptr[b.adress].arg = b.arg_adress
								if def_state != 0:
									self.def_context.add_label(b.arg_adress,b.b_type)
									self.context.label_count +=1
								else:
									self.context.add_label(b.arg_adress,b.b_type)
									self.def_context.label_count +=1
								
								for a in b.sub_blocks:
								
									arrptr[a].arg = superblock_end
									
							elif b.b_type == OP.Block_Type.DO:
							
								arrptr[b.arg_adress].arg = b.adress
								if def_state != 0:
									self.def_context.add_label(b.adress,b.b_type)
									self.context.label_count +=1
								else:
									self.context.add_label(b.adress,b.b_type)
									self.def_context.label_count +=1
								
								for a in b.sub_blocks:
								
									arrptr[a].arg = superblock_end + 1
									if def_state != 0:
										self.def_context.add_label(superblock_end+1,b.b_type)
										self.context.label_count +=1
									else:
										self.context.add_label(superblock_end+1,b.b_type)
										self.def_context.label_count +=1
									
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
				
			#print self.context.labels
			#print self.def_context.labels
		
		'''
		
		print "---------------------------------------"		
			
		for key in self.namespace_manager.functions:
			
			print "Function : " + self.namespace_manager.functions[key].name 
			
			for va in self.namespace_manager.functions[key].local_vars:
			
				print "	"+ va + str(self.namespace_manager.functions[key].local_vars[va].is_init)
				
				
			print '\n\n\n'
			print self.namespace_manager.functions[key].generate_head()
			
			print self.namespace_manager.solve_var("a","bar")
			
			print self.namespace_manager.solve_var("value","bar")
			
			print self.namespace_manager.functions[key].generate_foot()
			
			
		print "---------------------------------------"
			
		print len(self.namespace_manager.global_vars)
		
		
		#print self.namespace_manager.global_vars
		'''
		for key in self.namespace_manager.global_vars:
		
			print key
			print self.namespace_manager.global_vars[key].var_type
			
		#'''	
			

		
	 	#print self.def_op_array , self.function_registerer.functions
		return [self.op_array , self.context.labels] , [self.def_op_array , self.def_context.labels , self.function_registerer.functions] , self.namespace_manager














