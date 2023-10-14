


class Location:

	

	def __init__(self,path,filen,line,col):
	
		self.path = path
		self.file = filen
		self.line = line
		self.col = col
		
	def __str__(self):
	
		if path !=0:
			return path + self.file + '::'+str(self.line) +':'+str(self.col)
		else:
			return ''
	

class W_ERROR(Exception):

	def __init__(self,message,location):
	
		super(W_ERROR, self).__init__(message)
		
	def __str__(self):
	
		return 'Unspecified Error during compilation process'
		
		
class UnimplementedError(W_ERROR):

	def __init__(self,message,location):
	
		super(W_ERROR, self).__init__(message,location)
		
	def __str__(self):
	
		return 'This Part is unimplemented '
		
class ContextError(W_ERROR):

	def __init__(self,message,location):
	
		super(W_ERROR, self).__init__(message,location)
		
	def __str__(self):
	
		return 'Error during Context resolution'
		
class DuplicateSourceError(ContextError):

	def __init__(self,message,location):
	
		super(W_ERROR, self).__init__(message,location)
		
	def __str__(self):
	
		return 'Trying to set more than 1 MAIN file '+location
		
		
class ParserError(W_ERROR):

	def __init__(self,message,location):
	
		super(ParserError, self).__init__(message,location)
		
		
class InvalidSymbol(ParserError):

	def __init__(self,message,location,symbol):
	
		super(ParserError, self).__init__(message,location)
		
	def __str__(self):
	
		return 'Invalid Symbol '+symbol+' encountered during parsing: \n'+location


		
		
		
class BlockError(ParserError):

	def __init__(self,message,location,symbol):
	
		super(ParserError, self).__init__(message,location)
		
	def __str__(self):
	
		return  self.message + "at :"+ location
		
		
		
		
		
		
		
		
		
		
		
		
