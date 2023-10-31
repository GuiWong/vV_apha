
import vV.VM_Opcode as OP

import precompiler.VarUpdate.vV_Variable as vV_Var


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
	
def solve_array_dims(txt):

	dims = txt.split('[')
	print dims
	sizes =[]
	for d in dims:
	
		if len(d) > 0:
			sizes.append(solve_index(d[:-1]))
		
		
	print sizes
	return [len(sizes) , sizes]
	



def solve_type(txt):


	if txt[0] ==  OP.ref_op[OP.RNDBRACKETL] and txt[-1] ==  OP.ref_op[OP.RNDBRACKETR]:
		
		return vV_Var.vV_Ref_Type( solve_type(txt[1:-1]) )
		
	elif txt[0] ==  OP.ref_op[OP.RNDBRACKETL] and txt[-1] ==  OP.index_op[OP.SQRBRACKETR]:
	
		separ = txt.split(')')

		print "----------"			
		print separ
		
		if len(separ) > 2:
			content = ')'.join(separ[:-1])
		else:
			content = separ[0]
			
			
		print content
			
			
		content = content + ')'

		print content
			
		argus = solve_array_dims(separ[-1])
		
		
		
		return vV_Var.vV_Array_Type( solve_type(content) , argus[0] , argus[1] )
		
	elif txt in OP.var_type:
	
		return vV_Var.build_type(OP.var_type[txt])
		
	elif txt[-1] ==  OP.index_op[OP.SQRBRACKETR]:
	
		separ = txt.split('[')
		
		arg = '['.join(separ[1:])
		
		print arg
		
		argus = solve_array_dims(arg)
		
		return vV_Var.vV_Array_Type( solve_type(separ[0]) , argus[0] , argus[1] )
		
		
	else:
	
		assert False , "Error defining type : " + str(txt)



def solve_index(txt):

	if len(txt) >= 1:

		tmp = check_numeric_format(txt)
	
		if tmp[0]:
	
			#return vV_Var.vV_Int_Type()
			return tmp[1]
		
		else:
	
			return solve_var(txt)
	
	else:
	
		return ''
		
		
def create_argument_reference(v_type):

	return vV_Var.vV_Ref_Type(v_type)
		
def solve_func_args(txt):


	argu = txt.split(' ')
	cleaned=[]
	
	for arg in argu:
	
		if len(arg) > 0:
			cleaned.append(arg)
			
	print cleaned
			
	return [create_argument_reference(solve_type(cleaned[0]) ), solve_var(cleaned[1])]
		
def solve_func(txt,is_arg=False):
	
	if txt[0] ==  OP.ref_op[OP.RNDBRACKETL] and not is_arg:
	
		tmp = txt.split(')')
		
		argu = ')'.join(tmp[:-1])
		
		print argu
		
		return [solve_var(tmp[-1]) , solve_func(argu[1:],True) ]
		
	if ',' in txt:
	
		tmp = txt.split(',')
		b = []
		
		for t in tmp:
		
			b.append(solve_func_args(t))
			
		b.reverse()	
		return b
		
	elif is_arg:
	
		return solve_func_args(txt)
		
	else:
		
		return txt
		

def solve_var(txt):


	#print "solving var : " +txt
	#print txt[0]
	if txt[0] ==  OP.ref_op[OP.RNDBRACKETL]:
	
		tmp = txt.split(')')
		
		argu = ')'.join(tmp[:-1])
		
		
		return [solve_var(tmp[-1]) , solve_var(argu[1:]) ]
		
	if ',' in txt:
	
		tmp = txt.split(',')
		b = []
		
		for t in tmp:
		
			dat = t
			while dat[0] == ' ':
				dat = dat[1:]
			while dat[-1] == ' ':
				dat = dat[:-1]
			
			print t
			b.append(solve_var(dat))
			
		return b
			
	if txt[0] ==  OP.index_op[OP.SQRBRACKETL]:
	
		tmp = txt.split(']')
		
		b = [tmp[-1]]
		b.append([])
		
		for a in tmp[:-1]:
		
			assert a[0] == OP.index_op[OP.SQRBRACKETL] , "Error, notmatching brackets"
			b[1].append(solve_index(a[1:]))
			
		return b
		
	else:
	
		return txt
		
