

import precompiler.VarUpdate.Code_Namespace as Namespace
import vV.VM_Opcode as OP

import precompiler.VarUpdate.vV_Variable as vV_Var

import Cleaner.Syn_Parser as Syntaxer
import Cleaner.Label_Manager as Labl
import Cleaner.Block_Manager as Block_Manager
import Cleaner.Recursive_Type_Checker as T_Check

import Cleaner.Global_Namespace as G_NS

import Cleaner.Value_Checker as Val_Check

import precompiler.Opcode as Opcode

import os
import sys
home_path = os.path.expanduser('~') 

sys.path.append(home_path+'/.local/share/vVCompiler/utilities/')

import Logger






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
	current_import_src = ''
	
	
	
	
	
	def __init__(self,tokens,namespace):
	
		self.tokens = tokens
		
		
	
		self.name_space = namespace#Namespace.NameSpace_Manager()
		
		#self.global_name_space = G_NS.Global_Namespace(self.name_space)
		
		self.current_func = ''
	
		self.def_state = 0
		self.var_def_state = 0
		self.import_state = 0
		
		self.pc = 0
		self.f_pc = 0
		
		self.def_op = []
		self.main_op = []
	

		self.func_loca = {}
		
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
			
			Logger.log( data , 10 , Logger.Type.DEBUG , Logger.Flag.DATA)
			
			
			for a in data[1]:
				
				print a
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
			
	def check_scope(self,var_name,namespacer = None):
	
		ret = []	# bool: valid 
								# int : scope [1:global 2:local 3:argu] Notneeded for typecheck
				# vV_Type : Type
		
		
		deref_count = 0

		scope = None
		if self.def_state == 3:
		
			scope = self.current_func
			
		eff_var_name = var_name	
		while eff_var_name[0] in OP.ref_prefix:
		
			eff_var_name = eff_var_name[1:]
			deref_count+=1
			
		for c in eff_var_name:
		
			assert c not in OP.forbiden_chars, "Forbiden char in var invocation: "+c+' in '+var_name
			
		eff_name = ''
		namespace = None
			
		if '.' in eff_var_name:
			tmp = eff_var_name.split('.')
			assert len(tmp) == 2, 'Unimplemented multi-ref-to-namespace'
			eff_name= tmp[0]
			namespace = tmp[1]
			
		else:
		
			eff_name = eff_var_name
			namespace = None
			
			
		data = self.name_space.solve_var([eff_name],scope,namespace)
		
		print data


		#if eff_name == 'I':
		
		#	assert False, 'Breakpoint'
		
		
		if not data[0]:
		

			print 'Couldnt find var '+var_name
			print eff_name
			print namespace
			#print self.name_space.global_vars
			#print self.name_space.functions[self.current_func].local_vars
			#if var_name in self.name_space.functions.keys():
			if self.name_space.is_a_func(eff_name,namespace):
			
				print 'function call found'
				
				ret.append(False)
				ret.append( var_name)
				if len(self.name_space.get_function(eff_name,namespace).referenced_vars) > 0:
					ret.append(False)
					
					#for argus in self.name_space.functions[var_name].referenced_vars:
					
						
					#assert False, 'test'
					#ret.append()
				else:
					ret.append(True)
					
				ret.append(eff_name)
				
			
			else:
			
				assert False , 'unreachable'
				
			
		else:
		
			ret.append( data[0])
			ret.append(data[3])
			ret.append(eff_name)
			
			#if deref_count > 0:
			ret.append(deref_count)
			
			
		if len(data) > 4:
		
			ret.append(data[4])
		
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
				
				
	#---------------------------------------------------------------------------------
	
		elif tok in OP.import_statement:
				
			if self.import_state == 0:
				self.import_state = 1
			elif self.import_state == 2:
				
				if OP.import_statement[tok]==OP.AS:
				
					self.import_state = 3
					
				else:
				
					self.import_state = 1
					src_path = self.current_import_src
					self.current_import_src = ''
					return [src_path , None]
			
			
		elif self.import_state == 1:
		
			self.import_state = 2
			self.current_import_src = tok
			#return tok
			
		elif self.import_state == 3:
		
			self.import_state = 0
			src_path = self.current_import_src
			self.current_import_src = ''
			return [src_path , tok]
			
		elif self.import_state == 2:
		
			self.import_state = 0
			src_path = self.current_import_src
			self.current_import_src = ''
			self.current -= 1
			return [src_path , None]
			
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
				
				
				if type(solved[1][0]) == list:
				
				
					self.register_function(solved)
					
				else:
				
					self.register_function([solved[0],[solved[1]]])
				
				#print self.name_space.functions[self.current_func].referenced_vars
				#assert False , 'unimplemented'
				
			else:
			
				self.register_function(solved)
			
			
			
			
			print "Function Definition Found: "# + str(solved)

			
			
		elif self.var_def_state == 1:
		
			
			#is_val = Syntaxer.check_numeric_format(tok)
			is_val = Val_Check.check_for_valid_value(tok)
			
			if is_val[0]:
			
				
				self.current_var_type = is_val[2]#vV_Var.vV_Int_Type()
				self.current_var_value = is_val[1]
				
				self.var_def_state = 3
				self.current_var_isinit = True
				
			else:
			
				self.current_var_type = Syntaxer.solve_type(tok)
				self.var_def_state = 2
				
			print self.current_var_type
				
		elif self.var_def_state >= 2:
		
			
			#is_val = Syntaxer.check_numeric_format(tok)
			
			Logger.log(tok)
			
			is_val = Val_Check.check_for_valid_value(tok,self.current_var_type)
			
			Logger.log(tok)
			
			if is_val[0] and self.var_def_state == 2:		#No Value
			

				self.current_var_value = is_val[1]
				self.current_var_isinit = True
				
				self.var_def_state = 3
				
				
			else:
			
				Logger.log(tok)
				var_solved = Syntaxer.solve_var(tok)
				Logger.log(var_solved)
				
				
				self.check_forbidden(var_solved)
				
				print "var def found: " + str(var_solved)
				
				print '	'+str(self.current_var_scope)
				
				
				if isinstance(self.current_var_type,vV_Var.vV_Array_Type):
				
					for s in self.current_var_type.size:
					
						if s == '':
						
							assert False , 'Array have no size'
				
				self.register_variable(var_solved)
				
				rec_t = self.current_var_type
				
				self.current_var_value = 0
				self.current_var_isinit = False
				self.current_var_type = 0
				self.current_var_scope = 0
				
				print self.current_var_type
				
				
				
				#while not isinstance(rec_t,vV_Var.vV_Int_Type):
				
				#	rec_t = rec_t.content
				#	print '	'+str(rec_t)
					
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
		
		valu = Syntaxer.check_numeric_format(tok)
		
		
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
						
						referencing = isinstance(dst[1] , vV_Var.vV_Ref_Type)
						
						print src_type
						print dst_type
						
						valid = T_Check.check_valid(src_type,dst_type,referencing)
						
					assert valid , 'Type Error!'
					
					
					
					print '\n\n----\n	Argument of Assign:'
					print datt[0] 
					print datt[1]
					print '\n\n----\n'
					
					src_arg=[]
					dst_arg=[]
					
					src_name = datt[0]
					dst_name = datt[1]
					
					
					if len(datt[0]) == 2 and type(datt[0]) != str:
						src_name=datt[0][0]
						for a in datt[0][1]:
					
							if a == '':
						
								src_arg.append('pop')
						
							else:
						
								src_arg.append(a)
						
						src_arg.reverse()
						
								
					if len(datt[1]) == 2 and type(datt[1]) != str:
						dst_name=datt[1][0]
				
						for a in datt[1][1]:
					
							if a == '':
						
								dst_arg.append('pop')
						
							else:
						
								dst_arg.append(a)
								
						dst_arg.reverse()
					
					
					if src[3] >0:
					
						opcode.value = OP.DEREF_ASSIGN
						opcode.arg = [ [dst_name ,dst_arg] ,  [src[2],src_arg] , src[3]]
					else:
						opcode.value = OP.REF_ASSIGN
						opcode.arg = [ [dst_name ,dst_arg] ,  [src_name,src_arg] ]
					
					
						
					
					
				
				print valid
				#valid = T_Check.check_valid()
				#print T_check.check_valid()
				#assert False, 'Var assignement not Implemented Yet'
				
			elif tok[-1] in OP.deref_suffix:
			
			
				datt = Syntaxer.solve_var(tok[:-1])
				
				Logger.log(datt , 8 , Logger.Type.DEBUG , Logger.Flag.DATA)
				
				if type(datt) == str:
					src = self.check_scope(datt)
					src_name = src[2]
					tmp_arg = []
				else:
					src = self.check_scope(datt[0])
					src_name = src[2]
					tmp_arg = datt[1]
					
				Logger.log(src , 8 , Logger.Type.DEBUG , Logger.Flag.DATA)

					
				if type(datt) != str:
				
					pass
					#assert False , 'unimplemented deref of not simple var op'
					
				src_arg = []
				
				if type(tmp_arg) == str:
				
					tmp_arg = [tmp_arg]
				
				
				for a in tmp_arg:
				
					if a == '':
						
						src_arg.append('pop')
						
					else:
						
						src_arg.append(a)
							
				src_arg.reverse()
				
				

					
				
				
				
				Logger.log(str(src[1]) , 8 , Logger.Type.DEBUG , Logger.Flag.DATA)
				Logger.log(str(src_arg) , 8 , Logger.Type.DEBUG , Logger.Flag.DATA)
				
				eff_t = T_Check.calc_eff_type_2(src[1],src_arg)
				
				Logger.log(str(eff_t) , 8 , Logger.Type.DEBUG , Logger.Flag.DATA)
				if not isinstance(eff_t,vV_Var.vV_Ref_Type):
				
					assert False , 'cant deref a non ref var'
				
				
				
				opcode.value = OP.DEREF_PUSH
				opcode.arg = [src_name,src_arg,src[3] ]
				
				#if src[3] > 0:
				
				#	print '\n' + str(src)
				#	assert False , 'unimplemented deref of deref op'					
				#assert False , 'unimplemented deref op'
			
			else:
			
				print '-*-*-*-*'
				print tok
				datt = Syntaxer.solve_var(tok)
				print datt
				src_arg = []
				tmp_arg = []
				
				src_name = ''
				
				if type(datt) == str:
				
					src = self.check_scope(datt)
					print src
					tmp_arg = []
					src_name = datt
				
				elif type(datt[0]) == str:
				
					src = self.check_scope(datt[0])
					print src
					tmp_arg = datt[1]
					
					src_name = datt[0]
				
				else:
				
					assert False, 'Not Implemented Yet'
				
				print src_name
				print tmp_arg
				print src
				
				if type(tmp_arg) == str:
				
					tmp_arg = [tmp_arg]
					
				print tmp_arg
				
				print '\n\n-------\n	Arg Solving:'
				
				
				for a in tmp_arg:
				
					print a
					if a == '':
						
						src_arg.append('pop')
						
					else:
						
						src_arg.append(a)
							
				src_arg.reverse()
				
				print src_arg
				'''
				if len(datt) == 2:
				
					for a in datt[1]:
					
						if a == '':
						
							src_arg.append('pop')
						
						else:
						
							src_arg.append(a)
							
					src_arg.reverse()
				'''	
				
				
				
					
				
				if src[0]:
				
					if len(src)>=5:
					
						print src_name
						print src_arg
						print src
						#assert False , 'Breakpoint' 
						
						if src_name == 'I':
						
							if len(src_arg) == 0:
								arg_val = 0
							else:
								arg_val = int(src_arg[0])
							assert arg_val < self.block_manager.loop_level , 'Trying to access loop Iterator outside of a loop '
							opcode.value = OP.PUSH_VAR
							opcode.arg = [src_name,src_arg]
							print 'Push var found with arg: \n'
							print src_arg
							
						else:
							assert False , 'Unimplemented System var'
					else:
					
						if len(src)>=4:
						
							print src_name
							print src_arg
							print src[3]
							print src
							
							if src[3] > 0 or src_name[0]=='@':
								print 'deref'
								assert False , 'Breakpoint' 
						
								
						opcode.value = OP.PUSH_VAR
						opcode.arg = [src_name,src_arg]
						print 'Push var found with arg: \n'
						print src_arg
						
				elif len(src)>=4:
				
					callarg = [src_name,[]]
					
					for aaa in src_arg:
					
						print aaa
						ab = Syntaxer.solve_var(aaa)
						if type(ab)==str:
						
							callarg[1].append([ab,[]])
							
						else:
						
							callarg[1].append(ab)
				
					if src[2]:
						opcode.value = OP.CALL
						opcode.arg = [src_name]
					else:
						opcode.value = OP.CALL_W_ARG
						print callarg
						#assert False
						opcode.arg = callarg
				else:
					assert False, 'not a var, nor a function'
				
				
			
			
		#print [ opcode.value , opcode.arg]	
		return opcode , info
		
				
				
				
				
		
	
