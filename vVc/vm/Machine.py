
import w.VM_Opcode as OP
import precompiler.Opcode as Opcode
import Program



class Emul:



	def __init__(self,prog):
	
		self.stack = [0 for i in range(64)]
		
		self.program = prog
		
		
		self.pc = 0
		self.sp = 0#64
		
		self.current_op = 0
		
	def fetch(self):
	
		self.current_op = self.program.code[self.pc]
		self.pc += 1
		
	def push(self,v):
	
		self.stack.append(v)		
		self.sp+= 1
		
	def pop(self):
	
				
		self.sp -= 1
		return self.stack.pop()
		
	def step_exec(self):
	
	
		self.fetch()
		self.execute_opcode()
		
		
		
	def show_stack(self):
	
		print self.stack[60:]
		
	
	def debug_info(self):
	
		print ' PC: '+str(self.pc)
		print ' SP: '+str(self.sp)
		print ' Current Opcode: ' +str(self.current_op.value) + ' with arg : ' +str(self.current_op.arg)
		print'\n\n'
		
		
	def jmp(self,adr):
	
		self.pc = adr
		
		
	def execute_opcode(self):
	
	
		op = self.current_op.value
		arg = self.current_op.arg
		tmp = 0
		
		if op == OP.PUSH:
		
			self.push(arg)
			
		elif op == OP.SWAP:
		
			tmp = self.stack[-1]
			self.stack[-1] = self.stack[-2]
			self.stack[-2] = tmp
			
		elif op == OP.DROP:
		
			self.pop()
			
		elif op == OP.DUP:
		
			if arg == 0:
				self.push(self.stack[-1])
			else:
				for i in range(arg):
					self.push(self.stack[-1 * arg])
					
					
		elif op == OP.OUT:
		
			a = self.pop()
			if a >=10:
			
				print (chr(a + 55 ))
				
			else:
			
				print (chr(a + 48 ))
			
		elif op == OP.OUT:
		
			 print (int(self.pop()))

				
			
		elif op == OP.ADD:
		
			self.stack[-1] = self.stack[-2] + self.pop()
			
		elif op == OP.SUB:
		
			self.stack[-1] = self.stack[-2] - self.pop()
			
		elif op == OP.MUL:
		
			self.stack[-1] = self.stack[-2] * self.pop()
			
		elif op == OP.DIV:
		
			self.stack[-1] = self.stack[-2] / self.pop()
			
		elif op == OP.NEG:
		
			self.stack[-1] = self.stack[-1] * -1
			
		elif op == OP.MOD:
		
			self.stack[-1] = self.stack[-2] %  self.pop()
			
		
		
		elif op == OP.LSH:
		
			self.stack[-1] = self.stack[-1] << 1
			
		elif op == OP.RSH:
		
			self.stack[-1] = self.stack[-1] >> 1
		
		elif op == OP.NOT:
		
			self.stack[-1] = ~self.stack[-1]
			
		elif op == OP.OR:
		
			self.stack[-1] = self.stack[-2] | self.pop()
			
		elif op == OP.AND:
		
			self.stack[-1] = self.stack[-2] & self.pop()
			
		elif op == OP.XOR:
		
			self.stack[-1] = self.stack[-2] ^ self.pop()
			
			
		elif op == OP.LESS:
		
			b =  self.pop()
			a =  self.pop()
			if a < b:
				self.push(-1)
			else:
				self.push(0)
				
		elif op == OP.MORE:
		
			b =  self.pop()
			a =  self.pop()
			if a > b:
				self.push(-1)
			else:
				self.push(0)
			
			
		elif op == OP.EQUAL:
		
			b =  self.pop()
			a =  self.pop()
			if a == b:
				self.push(-1)
			else:
				self.push(0)
				
				
		elif op == OP.IF:		#Becomes a jump
		
			a = self.pop()
			if a == 0:
				self.jmp(arg)
			else:
				pass
				
				
		elif op in [ OP.ELSE]:		#Becomes a jump
		
			self.jmp(arg)
			
		elif op == OP.WHILE:
		
			a = self.pop()
			
			if a == 0:
				pass
			else:
				self.jmp(arg)
			


