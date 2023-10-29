



class Label_Manager:


	labels = {}
	def_labels={}
	counter = 0
	
	
	def __init__(self):
	
		self.labels={}
		self.def_labels={}
		self.counter = 0
		
	def add_main_label(self,adr):
	
		self.labels[adr] = self.counter
		self.counter += 1
		
	def add_def_label(self,adr):
	
		self.def_labels[adr] = self.counter
		self.counter += 1
		
		
		
	




