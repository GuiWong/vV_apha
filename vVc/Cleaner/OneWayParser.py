

import precompiler.VarUpdate.Code_Namespace as Namespace
import vV.VM_Opcode as OP

import precompiler.VarUpdate.vV_Variable as vV_Var

import Cleaner.Syn_Parser as Syntaxer
import Cleaner.Label_Manager as Labl
import Cleaner.Block_Manager as Block_Manager
import Cleaner.Recursive_Type_Checker as T_Check

import precompiler.Opcode as Opcode




class One_Way_Parser:

	
	def_op = []
	main_op = []
	
	current_func = ''
	func_loca = {}
	
	def_state = 0
	var_def_state = 0
	
	current_block = []
	current_block_type = []
	current_block_members = []
	
	tokens = []
	
	pc = 0
	f_pc = 0
	
	current = 0
	
	
	current_var_type = 0
	current_var_scope = 0
	current_var_value = 0
	current_var_isinit = False
	
	
	
	
	
	def __init__(self,tokens):
	
		self.tokens = tokens
	
		self.name_space = Namespace.NameSpace_Manager()
		
		self.current_func = ''
	
		self.def_state = 0
		self.var_def_state = 0
		
		self.pc = 0
		self.f_pc = 0
		
		self.label_manager = Labl.Label_Manager()
		self.block_manager = Block_Manager.Block_Manager()
		
	def solve_next_token(self):
	
		
		pass
		
	def check_forbidden(self,tok):
	
		for c in tok:
		
			assert c not in OP.forbiden_chars
		
	def register_function(self,data):
	
		args = {}
		if type(data) == str:
		
			name = data
		
		else:
			name = data[0]
			args = {}
			for a in data[1]:
			
				varo = vV_Var.vV_Variable(a[1],OP.PASSED,a[0],False,0)
			
				args[a[1]] = varo
				
				
		print name
		print args
		
		self.name_space.define_function(name,args)
		
		self.func_loca[len(self.def_op)] = name
		
		self.current_func = name
		
	def register_variable(self,name):
	
		varo = vV_Var.vV_Variable(name,self.current_var_scope,self.current_var_type,self.current_var_isinit,self.current_var_value)
		if self.current_var_scope == OP.GLOBAL:
		
			self.name_space.define_global(varo)
			
		elif  self.current_var_scope == OP.LOCAL:
		
			self.name_space.functions[self.current_func].add_local_var(varo)
			
		else:
		
			assert False, 'Unimplemented'
			
	def check_scope(self,var_name):
	
		ret = []	# bool: valid 
								# int : scope [1:global 2:local 3:argu] Notneeded for typecheck
				# vV_Type : Type
		

		scope = None
		if self.def_state == 3:
		
			scope = self.current_func
			
		data = self.name_space.solve_var([var_name],scope)
		
		print data
		
		
		if not data[0]:
		

			print 'Couldnt find var '+var_name
			print self.name_space.global_vars
			print self.name_space.functions[self.current_func].local_vars
			if var_name in self.name_space.functions.keys():
			
				print 'function call found'
				
				ret.append(False)
				ret.append( var_name)
				if len(self.name_space.functions[var_name].referenced_vars) > 0:
					ret.append(False)
					
					#for argus in self.name_space.functions[var_name].referenced_vars:
					
						
					#assert False, 'test'
					#ret.append()
				else:
					ret.append(True)
		else:
		
			ret.append( data[0])
			ret.append(data[3])
		
		print '--:'
		print ret
		return ret
		
			
			
	def start_function(self):
	
		pass
		
	def end_function(self):
	
		opc = Opcode.Opcode()
		opc.value = OP.ENDEF
		opc.arg = 0
				
		opc.adress = len(self.def_op)		#(will be needed for rets)
				
		self.store_opcode(opc)
		
	def make_label(self,adress):
	
		if self.def_state == 3:
		
			self.label_manager.add_def_label(adress)
			
		else:
		
			self.label_manager.add_main_label(adress)
		
		
	def close_block(self,block_list):
	
		superblock_end = block_list[0].arg_adress
		
		print 'closing blocks : '
		for b in block_list:
			print b
		
		if self.def_state == 3:
		
			op_l = self.def_op
			
		else:
		
			op_l = self.main_op
		
		for b in block_list:
			
			if b.b_type in [ OP.Block_Type.IF , OP.Block_Type.ELSE ]:
			
				#assert len(b.sub_blocks) == 0 , 'Unimplemeted Subblock : '+ str(b)
				
			
				op_l[b.adress].arg = b.arg_adress
				
				self.make_label(b.arg_adress)
				
				for a in b.sub_blocks:
				
					op_l[a].arg = superblock_end
			
				#assert False , 'Ifs ad elses unimplemented : ' + str(b)
				
			elif b.b_type == OP.Block_Type.END:
			
			
				assert False , "Is it reachable??"
				assert len(b.sub_blocks) == 0 , 'Unimplemeted Subblock : '+ str(b)
				
			
				op_l[b.adress].arg = b.arg_adress
			
				assert False , 'End unimplemented : ' + str(b)
				
			elif b.b_type == OP.Block_Type.DO:
			
			
				op_l[b.arg_adress].arg = b.adress
				
				#print 'labal made at : ' +str(b.adress)
				self.make_label(b.adress)
				self.make_label(superblock_end + 1)
				#assert False , 'DO unimplemented : ' + str(b)
				for a in b.sub_blocks:
				
					op_l[a].arg = superblock_end + 1
					
				for a in b.sub_blocks_inverted:
				
					op_l[a].arg = b.adress
					
			elif b.b_type == OP.Block_Type.LOOP:
			
				op_l[b.arg_adress].arg = [b.adress + 1,superblock_end + 1]
				self.make_label(b.adress+1)
				
				self.make_label(superblock_end + 1)
				for a in b.sub_blocks:
				
					op_l[a].arg = superblock_end + 1
					
				for a in b.sub_blocks_inverted:
				
					op_l[a].arg = b.adress
				
		
	def fetch(self):
	
		
		tkn = self.tokens[self.current]
		self.current += 1
		return tkn
	
	def next_token(self):
		
		tok = self.fetch()
		
		#print tok
		
		if tok in OP.define:
		
			if OP.define[tok] == OP.DEF and self.def_state == 0:
			
				self.def_state = 1
				
			elif OP.define[tok] == OP.ENDEF and self.def_state == 3:
		
		
				self.end_function()
				self.def_state = 0
				
			#TODO: Need to store a retOpcode, may need to do it elsewhere
				
				
				
				
			else:
			
				assert False, 'Def Boundary Mismatch'
				
		elif tok in OP.var_define:	
		
			assert self.var_def_state == 0 , "Misplaced Scope descriptor"
			self.var_def_state = 1					#scoped, untyped
			
			if OP.var_define[tok] == OP.IMPLICIT:
							
				if self.def_state == 0:
								
					self.current_var_scope = OP.GLOBAL
									
				elif self.def_state == 3:
								
					self.current_var_scope = OP.GLOBAL
									
				else:
								
					assert False , "UNABLE TO define variable scope "
					
			else:
			
				print tok + ' : '
				print OP.var_define[tok]
				self.current_var_scope = OP.var_define[tok]
				
				
		elif self.def_state == 1:
		
			#solved = Syntaxer.solve_var(tok)
			print 'func decode:	*#*#*#*#\n'
			print tok
			solved = Syntaxer.solve_func(tok)
			print solved
			self.def_state = 3
			
			if len(solved)>1 and type(solved)!=str:
			
				print 'func with args'
				#argdict = {}
				#for argss in solved[1]:
					#print argss
				#	argdict[argss[1]] = vV_Var.vV_Variable(argss[1],OP.PASSED,argss[0])
				
				self.register_function(solved)
				
				#print self.name_space.functions[self.current_func].referenced_vars
				#assert False , 'unimplemented'
				
			else:
			
				self.register_function(solved)
			
			
			
			
			print "Function Definition Found: "# + str(solved)

			
			
		elif self.var_def_state == 1:
		
			
			is_val = Syntaxer.check_numeric_format(tok)
			
			if is_val[0]:
			
				
				self.current_var_type = vV_Var.vV_Int_Type()
				self.current_var_value = is_val[1]
				
				self.var_def_state = 3
				self.current_var_isinit = True
				
			else:
			
				self.current_var_type = Syntaxer.solve_type(tok)
				self.var_def_state = 2
				
			print self.current_var_type
				
		elif self.var_def_state >= 2:
		
			
			is_val = Syntaxer.check_numeric_format(tok)
			
			if is_val[0] and self.var_def_state == 2:		#No Value
			

				self.current_var_value = is_val[1]
				self.current_var_isinit = True
				
				self.var_def_state = 3
				
				
			else:
			
				var_solved = Syntaxer.solve_var(tok)
				
				
				
				self.check_forbidden(var_solved)
				
				print "var def found: " + str(var_solved)
				
				print '	'+str(self.current_var_scope)
				
				self.register_variable(var_solved)
				
				rec_t = self.current_var_type
				
				self.current_var_value = 0
				self.current_var_isinit = False
				self.current_var_type = 0
				self.current_var_scope = 0
				
				print self.current_var_type
				
				
				
				while not isinstance(rec_t,vV_Var.vV_Int_Type):
				
					rec_t = rec_t.content
					print '	'+str(rec_t)
					
				#print '	'+str(rec_t)
	
				self.var_def_state = 0
				
		
		
		else:
		
			assert self.def_state == 0 or self.def_state == 3 , "Uncomplete Function Definition"
			
			assert self.var_def_state == 0 , "Uncomplete Var Definition"
			
			
			
			
			op , info = self.create_opcode(tok)
			
			if self.def_state == 3:
			
				adre = len(self.def_op)
				
			else:
			
				adre = len(self.main_op)
				
			
			
			op.adress=adre
			
			
			#TODO:	check op size
			
			if op.value not in [OP.END_BLOCK]:
			
				print ' Opcode '+str(adre) +' - '+ str(op)
				self.store_opcode(op)
			
			
			
			if info != 0:
			
				tmp = self.block_manager.manage_block(adre,info)
				if len(tmp) > 0:	#need managing
					self.close_block(tmp)
				#assert False, 'Block Unimplemented : ' + str(op.value) + '  -  ' + str(info)
				
			else:
			
				#self.store_opcode(op)
				pass
				
			if op.value in [OP.ENDLOOP]:
			
				#print ' Opcode '+str(adre+1) +' - '+ str(o)
				print 'endloop found :'
				tmp_opc = Opcode.Opcode()
				tmp_opc.value = OP.CLEANUP_LOOP
				self.store_opcode(tmp_opc)
			
			if len(self.main_op)>=1:
				print self.main_op[-1]
				
			
			
	
	#def 			
		
		
	def store_opcode(self,opc):
	
	
		#TODO: Check Op size? Or just dont call store...
	
		if self.def_state == 3:
		
			self.def_op.append(opc)
			
		else:
		
			self.main_op.append(opc)						
			
	def create_opcode(self,tok):
	
		opcode = Opcode.Opcode()
		info = 0
		
		valu= Syntaxer.check_numeric_format(tok)
		
		
		if tok in OP.direct_op.values():
		
		
			opcode.value = OP.get_dir_opcode_by_string(tok)
			
		elif tok in OP.block_op.values():
		
			#assert False, 'Blocks to Come... Not Implemented Yet'
			opcode.value= OP.block_op.keys()[OP.block_op.values().index(tok)]
			info= OP.block_type[opcode.value]
			
			print str(info)  + ' - ' + str(opcode.value) + ' - ' + str(opcode)
			
			
		elif valu[0]:
		
			opcode.value=OP.PUSH
			opcode.arg = valu[1]	
			
			
		elif tok[0].isdigit() and tok[1:] in OP.int_prefixed.values():
			
			opcode.value = OP.get_virual_opcode_by_string(tok[1:])
			opcode.arg = int(tok[0])
			
		elif tok[0] in OP.format_prefixes.keys() and tok[1:] in OP.format_prefixed.values():
			

			opcode.value = OP.get_virual_opcode_by_string(tok[1:])	#ERROR WAS HERE(NEED AND FOR COND)
			opcode.arg = OP.format_prefixes[tok[0]]
			
		else:
		
			if tok[-1] in OP.ref_suffix:				#Pop Or var_Assign
			
				datt = Syntaxer.solve_var(tok[:-1])
				valid = False
				scp = []
				print datt
				if type(datt[0]) == str and tok[0] == OP.index_op[OP.SQRBRACKETL]:			#Pop Case
				
					print 'simple var pop'
					src_arg = []
					scp = self.check_scope(datt[0])
					if scp[0]:
						
						
						eff_t = T_Check.calc_effective_type(scp[1],datt[1])
						print eff_t
						valid = T_Check.check_valid(eff_t,vV_Var.vV_Int_Type())

					assert valid, 'Type Error!'
					
					
					if len(datt) == 2:
				
						for a in datt[1]:
					
							if a == '':
						
								src_arg.append('pop')
						
							else:
						
								src_arg.append(a)
								
						src_arg.reverse()
					
					opcode.value = OP.ASSIGN
					opcode.arg = [datt[0],src_arg]
					
				elif type(datt) == str:
				
					opcode.value = OP.ASSIGN
					opcode.arg = [datt,[]]
					
				else:
				
					print 'var assignement'
					
					if type(datt) == str:
						assert False , "Shouldn't be reachable "
					else:
						if type(datt[0]) == str:
							src = self.check_scope(datt[0])
							src_arg = []
						else:
							src = self.check_scope(datt[0][0])
							src_arg = datt[0][1]
						
						
						if type(datt[1]) == str:
							dst = self.check_scope(datt[1])
							dst_arg = []
						else:
							dst = self.check_scope(datt[1][0])
							dst_arg = datt[1][1]
						
					print src , src_arg
					print dst,dst_arg
					
					if dst[0] and src[0]:
					
						src_type = T_Check.calc_effective_type(src[1],src_arg)
						dst_type = T_Check.calc_effective_type(dst[1],dst_arg)
						
						valid = T_Check.check_valid(src_type,dst_type)
						
					assert valid , 'Type Error!'
					
					
					
					print '\n\n----\n	Argument of Assign:'
					print datt[0] 
					print datt[1]
					print '\n\n----\n'
					
					src_arg=[]
					dst_arg=[]
					
					src_name = datt[0]
					dst_name = datt[1]
					
					
					if len(datt[0]) == 2:
						src_name=datt[0][0]
						for a in datt[0][1]:
					
							if a == '':
						
								src_arg.append('pop')
						
							else:
						
								src_arg.append(a)
						
						src_arg.reverse()
						
								
					if len(datt[1]) == 2:
						dst_name=datt[1][0]
				
						for a in datt[1][1]:
					
							if a == '':
						
								dst_arg.append('pop')
						
							else:
						
								dst_arg.append(a)
								
						dst_arg.reverse()
					
					
					
					
					opcode.value = OP.REF_ASSIGN
					opcode.arg = [ [dst_name ,dst_arg] ,  [src_name,src_arg] ]
					
					
				
				print valid
				#valid = T_Check.check_valid()
				#print T_check.check_valid()
				#assert False, 'Var assignement not Implemented Yet'
			else:
			
				print '-*-*-*-*'
				print tok
				datt = Syntaxer.solve_var(tok)
				print datt
				src_arg = []
				
				src_name = ''
				
				if type(datt) == str:
				
					src = self.check_scope(datt)
					print src
					src_arg = []
					src_name = datt
				
				elif type(datt[0]) == str:
				
					src = self.check_scope(datt[0])
					print src
					src_arg = []
					
					src_name = datt[0]
				
				else:
				
					assert False, 'Not Implemented Yet'
				
				print '\n\n-------\n	Arg Solving:'
				if len(datt) == 2:
				
					for a in datt[1]:
					
						if a == '':
						
							src_arg.append('pop')
						
						else:
						
							src_arg.append(a)
							
					src_arg.reverse()
					
				if src[0]:
					opcode.value = OP.PUSH_VAR
					opcode.arg = [src_name,src_arg]
				elif len(src)>=3:
				
					callarg = [src_name,[]]
					
					for aaa in src_arg:
					
						ab = Syntaxer.solve_var(aaa)
						if type(ab)==str:
						
							callarg[1].append([ab,[]])
							
						else:
						
							callarg[1].append(ab)
				
					if src[2]:
						opcode.value = OP.CALL
						opcode.arg = [src[1]]
					else:
						opcode.value = OP.CALL_W_ARG
						print callarg
						#assert False
						opcode.arg = callarg
				else:
					assert False, 'not a var, nor a function'
				
				
			
			
		print [ opcode.value , opcode.arg]	
		return opcode , info
		
				
				
				
				
		
	
