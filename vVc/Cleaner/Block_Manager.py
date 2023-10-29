
import vV.VM_Opcode as OP

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
		
		
	def __str__(self):
	
	
		return str(self.adress) +' - '+ str( self.arg_adress) +' - '+ str( self.b_type) +' - '+  str(self.sub_blocks)
		


	
class Block_Manager:

	blocks = []
	level = 0
	
	def __init__(self):
	
		self.blocks = []
		self.level = 0
		
	
		
	def manage_block(self,op_adr,b_type,filepos = 'noPos'):
	
		actual = Block(op_adr,b_type,filepos)
		
		if actual.b_type == OP.Block_Type.IF:
		
			self.start_block(actual)
			return []
		
		elif actual.b_type == OP.Block_Type.DO:
		
			self.start_block(actual)
			return []
			
		elif actual.b_type == OP.Block_Type.BREAK:	
		
		
			print 'break found'
			rec = 1
			while self.blocks[0-rec].b_type != OP.Block_Type.DO:
			
				rec += 1
				
			self.blocks[0-rec].sub_blocks.append(actual.adress)
			
			return []
		
		
		elif actual.b_type == OP.Block_Type.LOOP:
		
			self.start_block(actual)
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
				
		
		elif actual.b_type == OP.Block_Type.ENDLOOP:
		
			assert self.blocks[-1].b_type in [OP.Block_Type.LOOP] , "Block Mismatch"
			
			self.blocks[-1].arg_adress = actual.adress 
			
			return [self.end_block()]		
				
		
	def start_block(self,block):
	
		self.blocks.append(block)
		self.level +=1
		
	def end_block(self):
			
		b = self.blocks.pop()
		self.level-=1
		return b






