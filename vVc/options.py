

VERBOSE = 8
PREPROCESS_ONLY = 16


	
class Format:

	RAW = 1	# compatible: 	-p (text of bytecode)
			#		-a (.asm)
					
	#HEX = 2	
	




argflag = {


#	'-v' : VERBOSE			#more output during compile time
	'-p' : PREPROCESS_ONLY		#st
#	'-a' : ASSEMBLE_ONLY
	
	


}




OUTPUT_FILE = 17
FORMAT = 18


argarg = {

	'-o' : OUTPUT_FILE	,	#name of output file
	'-f' : FORMAT			#format of output:

}

outformat = {

	"raw" : Format.RAW,
	"RAW" : Format.RAW,

}
