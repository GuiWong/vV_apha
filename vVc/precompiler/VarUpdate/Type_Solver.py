
import vV.VM_Opcode as OP

class Type_Solver:

	

	def solve_var_type(self,buff):

		current_var_type=0
						
	
						
		if buff[0] == OP.ref_op[OP.RNDBRACKETL] and buff[-1] == OP.index_op[OP.SQRBRACKETR]:	#array of Ref
					
					
			parts = buff.split(")")
	#		print parts
						
			pointed_type = 0
						
					
			if parts[0][1:] in OP.var_type:
						
							
				pointed_type = vV_Var.build_type(OP.var_type[parts[0][1:]])
			#	print pointed_type
			#	print pointed_type.__class__
							
							
			else:
							
							
					
				decoded = self.symbol_solver.decode(parts[0][1:])

				assert decoded[0] , "Error While Trying to decode Potential Var: " + parts[0][1:] +" at: "+ str(self.context.build_location())
						
				valu = []
					
				for c in decoded[2]:
					
					
				if len(c) == 0:
							
					print "empty bracket"
					valu.append("pop")
							
							
				else:
				
					#assert False , ' Invalid for ref passing'
					assert c.isdigit() , "Error, non numeric index ("+c+") at: "+ str(self.context.build_location())
						
					valu.append(int(c))
						
							valu.reverse()
							print decoded
							print valu
						
						
				pointed_type = vV_Var.vV_Array_Type(vV_Var.build_type(OP.var_type[decoded[1]]),len(decoded[2]),valu )
			
							print pointed_type
							
							
							
							
							
						decoded = self.symbol_solver.decode(parts[1])
						
						print decoded

						assert decoded[0] , "Error While Trying to decode Potential Var: " + parts[0][1:] +" at: "+ str(self.context.build_location())
						
						valu = []
					
						for c in decoded[2]:
					
					
							if len(c) == 0:
							
								print "empty bracket"
								valu.append("pop")
							
							
							else:
								assert c.isdigit() , "Error, non numeric index ("+c+") at: "+ str(self.context.build_location())
						
								valu.append(int(c))
						
						valu.reverse()
						print decoded
						print valu
						
						
						
						current_pointer_type = vV_Var.vV_Ref_Type(pointed_type)
						
						current_var_type = vV_Var.vV_Array_Type(current_pointer_type,len(decoded[2]),valu )
						
						print current_pointer_type
						
						print current_var_type
						
						
						#current_var_value =tmp_val
						#current_var_init = tmp_is_init
							
					
						#assert False, "Unimplemented yet"
						
						
					elif buff[-1] == OP.index_op[OP.SQRBRACKETR]:
					
					
						decoded = self.symbol_solver.decode(buff)
						
						
						tmp_type = 0
						tmp_val = []
						tmp_size = []
						tmp_dim = 0
						tmp_is_def = False
						tmp_is_init = False
						
						
		#				print decoded
						assert decoded[0] , "Error While Trying to decode Type: " + buff +" at: "+ str(self.context.build_location())
						
						
						if decoded[1] in OP.var_type:
						
						
						
						
							
							tmp_type = vV_Var.build_type(OP.var_type[decoded[1]])
							
							
							for dim in decoded[2]:
							
								assert len(dim) >= 1 , "Array need a fixed size ("+buff+") "+str(self.context.build_location())
								assert dim.isdigit() , "NOT a numeric value in indexing operation ("+decoded[2][0]+") : " +str(self.context.build_location())
								
								tmp_size.append(int(dim))
								tmp_dim += 1
								
		#					print"\n\n--------------------------\n\n"	
		#					print tmp_size
		#					print decoded[2]
							
		#					print"\n\n--------------------------\n\n"
							
							
							tmp_is_def = True
							tmp_is_init = False
						
							
						elif decoded[1] == "None":	#TODO: define a return value for only brackets
						
						
						
							assert False , "inimplemented array initialisation  : " +str(self.context.build_location())
						
						
							
						else:
						
						
							assert False , "Unrecognised type ("+decoded[1]+") : " +str(self.context.build_location())
						
						
						
						
		#				print current_var_type
		#				print tmp_dim
		#				print tmp_size
						
						current_var_type = vV_Var.vV_Array_Type(tmp_type,tmp_dim,tmp_size )
						current_var_value =tmp_val
						current_var_init = tmp_is_init
							
							
					#	else:
						
					#		assert False , "NOT IMPLEMENTED (probably trying a multi dimentionnal array at "+str(self.context.build_location())+")"
							
						
		#				print current_var_type
						
		#				print current_var_type.calc_size()
						
					
						#assert False , "NEED TO IMPLEMENT BRACKET DECODING"
						

					
					else:
					
						assert False , "RAISE UNKNOWN VALUE TYPE : "+buff+ " "+  str(self.context.build_location())
					
					
				var_def_state = 3	#scoped, typed, has value
					
					
				continue
				
			
