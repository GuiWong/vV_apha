
import vV.VM_Opcode as OP
#import Cleaner.Var_Solver

#import WErrors

class Parser:

	lines= 0
	current=0
	
	is_done=False
	
	
	in_bracket=0
	in_quotes=0
	mode=0
	
	var_def_state=0
	def_state=0
	


	def __init__(self,raw):
	
		self.lines = raw
		self.current = ''
		self.is_done=False
		
		self.in_quotes=0
		self.in_bracket=0
		self.mode = 0
		
		self.var_def_state = 0
		self.def_state = 0
		
		self.token_array=[]
		
	def default(self,path):
	
		with open(path,"r") as file:
		
			self.raw_lines = file.readlines()
			
		self.lines = self.raw_lines
		#print self.lines[0][1]
		
		
	def next_char(self,cc,ll):
	
		c = cc
		l = ll
		#print  l , c
		r = self.lines[l][c]
		#print r
		done = False
		
		
		if r in OP.comment and self.in_quotes == 0:
				
			
				
			if self.mode == 0:
					
				c=-1
				l+=1
						#continue
						
			elif self.mode == 1:
				
				mode = 0
				c=-1
				l+=1
						
			if l >= len(self.lines):
					
				self.is_done = True
				
		elif r in OP.quotes.keys():
				
			if self.in_quotes != 0 and OP.quotes[r] == self.in_quotes:
				
				#print "End Quote:"
				self.in_quotes = 0
				self.current += r
					
			elif self.in_quotes == 0 and self.mode == 0:
				
				#print "Start Quote:"
				self.in_quotes = OP.quotes[r]
				self.current += r
						
			else:
				#print "Inside Quote:"	
				self.current += r
					
						#raise WErrors.ParserError('Misplaced Quote', self.context.build_location())
						
		elif r in OP.start_brack and self.in_quotes == 0:
				
			self.in_bracket += 1
			self.current += r
					
		elif r in OP.end_brack  and self.in_quotes == 0:
				
			self.in_bracket -= 1
			self.current += r
				
		elif r in OP.separator and self.in_quotes == 0:
				
			if self.mode == 0:
				

				pass
						
			elif self.in_bracket > 0:
					
				self.current +=r
						
			else:
				

				self.mode = 0	
				done = True
				
		else:
		
			
			self.mode = 1
			self.current +=r	
			
				
		c += 1
		if l >= len(self.lines):
					
			self.is_done = True
			return [done , c , l ]
				
		while c >= len(self.lines[l]):
			c = 0
			l += 1
			if l >= len(self.lines):
					
				self.is_done = True
				return [done , c , l ]
		
		return [done , c , l ]
		
	def check_token(self,token):
	
	
		if token in OP.define.keys():
						
						
			assert self.var_def_state == 0 , " RAISE UNFINISHED VAR DEFINITION" + token

			if self.def_state == 3 and OP.define[token] == OP.ENDEF:
							
							
				self.def_state = 4
								
				self.token_array.append(token)
						
			elif self.def_state == 0 and OP.define[token] == OP.DEF:
							
				self.token_array.append(token)
				self.def_state = 1
								
			else:
							
				assert False,"Definition Boundary Mismatch : " + token
						
		elif token in OP.var_define:
						
			assert self.var_def_state == 0 , "ILLEGAL LOCATION FOR SCOPE KEYWORD "+ str(self.context.build_location())
			
			
			self.var_def_state = 1
			self.token_array.append(token)	
								
			
		
		
		if self.var_def_state == 1:
			self.var_def_state = 2
				
		elif self.var_def_state == 2:
			

			self.var_def_state = 3
			self.token_array.append(token)

				
		elif self.var_def_state == 3:
			
			#print'vaarname'
			self.var_def_state = 0
				
			self.token_array.append(token)

				
				
				
		elif self.def_state == 1:
			self.def_state = 2
		elif self.def_state == 2:
			self.token_array.append(token)
			self.def_state = 3
		elif self.def_state == 3 or self.def_state == 0:
			self.token_array.append(token)
		elif self.def_state == 4:
			self.def_state = 0
				
			
				
				
			#var_def_state = 0
			#def_state = 0
			
							
		
	def first_pass(self):
	
	
		c=0
		l=0
		
		self.is_done = False
		
		while len(self.lines[l])==0:
			l+=1
		
		while not self.is_done:
		
			r =self.next_char(c,l)
			#print self.current 
			#print r
			if r[0]:
				
				print str(l) +'-'+str(c)
				self.check_token(self.current)
				#print self.current , self.token_array[-1]
				self.current = ''
				
				
			else:
				pass
				
			c = r[1]
			l = r[2]
				
				
		return self.token_array
		
			
