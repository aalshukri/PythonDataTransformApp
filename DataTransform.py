#
# Data Transform Application
#
# @created 2017-05-10 11:56:12 
# @version 0.01 (beta)
# @author aalshukri
# @email -
#
"""
PythonDataTransformApp

Converts long-form data to wide-form data

Assumes that input is sorted by idColumn.
This assumption allows for large data sets to be processed
without loading entire file into memory for sorting.


python DataTransform.py --help
usage: DataTransform.py [-h] -l LONGFORMFILENAME -w WIDEFORMFILENAME -u
                        UNIQUEIDCOLUMN [-s STATICCOLUMNS [STATICCOLUMNS ...]]
                        [-i IGNORECOLUMNS [IGNORECOLUMNS ...]] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -l LONGFORMFILENAME, --longFormFileName LONGFORMFILENAME
                        Name of the long form data input file
  -w WIDEFORMFILENAME, --wideFormFileName WIDEFORMFILENAME
                        Name of the wide form data output file
  -u UNIQUEIDCOLUMN, --uniqueIdColumn UNIQUEIDCOLUMN
                        Column number that contains the unique id to identify
                        rows
  -s STATICCOLUMNS [STATICCOLUMNS ...], --staticColumns STATICCOLUMNS [STATICCOLUMNS ...]
                        List of static columns. ie 2 4 5 6
  -i IGNORECOLUMNS [IGNORECOLUMNS ...], --ignoreColumns IGNORECOLUMNS [IGNORECOLUMNS ...]
                        List of columns to ignore. ie 2 4 5 6
  -v, --verbose         Set output verbosity to true


Example
> python DataTransform.py -l testdata/testdata1.csv -w testdata/testdata1_wide.csv -u 0 -s 2 3 4 -i 1


"""

import csv
import os

import argparse

class DataTransform(object):	
	'Data Transform App'
	pass

	

	"""
	" Constructor
	"""
	def __init__(self,verboseFlag):
		self.verbose=verboseFlag
	#/contructor


	"""
	" test method
	"""
	def test(self):
		'test method'
		print("test")



	"""
	" transformLongToWideForm
	"""
	def transformLongToWideForm(self, longFormFileName,wideFormFileName,idColumn,staticColumns,ignoreColumns):
		""" transformLongToWideForm()

   		     This function takes the long-form csv file, and outputs to a wide-form file.

		     params
			* longFormFileName - the csv filename of the long form data file.
			* wideFormFileName - the csv filename of the output wide form data file.
			* idColumn	   - column which contains the id to segments users.	
			* staticColumns	   - colunms which stays the same for each row.
			* ignoreColumns	   - columns to ignore when transforming to wide form.
			
		"""

		if self.verbose: print("transformLongToWideForm("+longFormFileName+")")


		#output file writer
		outfile = open(wideFormFileName, "w")
		write = csv.writer(outfile, delimiter=',')


		#input file writer
		infile = open(longFormFileName, "r")
		read = csv.reader(infile)

		# get file headers
		fileHeaders = next(read)


		#num columns in long format file
		maxColumnLength = len(fileHeaders)
		if self.verbose: print("maxColumnLength="+str(maxColumnLength))


		currentIteration=1
		currentId=0
		rowData=[]
	
		maxIteration=0


		#For each row
		for row in read:			

			# Part 1 - 
			# Check if current row is for the same person id as previously,
			# if no (ie, idValue != currentId is true)
			#   then, 
			#    - write the current row data to file it is not empty
			#    - reset the current row data
			#    - update maxiterations by comparing the currentIterations. This is to know what the max number of possible columns are going to be in the wide format. Which is essentiall determined by the max number of rows for all patients.
			#    - Adppend the current values for the start of the next persons wide form data. This includes addeding the id value, and any static values.
			#
			# if yes (ie, idValue != currentId is false)
			#   then, increment the current iteration, and move onto part 2. 


			#For each column
			idValue = row[idColumn]
			if self.verbose: print("idvalue="+idValue)
			

			if idValue != currentId:
				if self.verbose: print(" new person")

				# write current row data (if not empty)
				if rowData != []:
					if self.verbose: print(" Write previous persons data "+str(currentIteration))
					if self.verbose: print(rowData)
					write.writerow(rowData)

				# reset row data
				rowData=[]	

				# update max iterations if more
				if currentIteration > maxIteration:
					maxIteration=currentIteration
				
				# reset iteration count
				currentIteration=1

				# set current id value
				currentId=idValue
				
				# write new row details

				# (1) write id
				rowData.append(idValue)

				# (2) write static columns
				for staticItem in staticColumns:
					#print(staticItem)
					rowData.append(row[staticItem])
			else:
				if self.verbose: print(" not new person")
				currentIteration=currentIteration+1

			# Part 2 
			# Checking for ignore or static columns to exclude.
			# if not, then append to the current row data.
			#
			for i in range(0,len(row)):

				# check if we should ignore this row
				#
				if i == idColumn:
					if self.verbose: print("  dont output "+str(i))
				elif i in staticColumns:
					if self.verbose: print("  dont output "+str(i))
				elif i in ignoreColumns:
					if self.verbose: print("  dont output "+str(i))	
				else:					
					# append item to current row
					if self.verbose: print("  printing "+str(i))				
					rowData.append(row[i])



		# write last persons row data (if not empty)
		if rowData != []:
			if self.verbose: print(" Write LAST persons data "+str(currentIteration))
			if self.verbose: print(rowData)
			write.writerow(rowData)
		
		infile.close()		
		outfile.close()

	
		# create headers
		wideFormHeaders = self.createHeaders(fileHeaders,maxIteration,idColumn,staticColumns,ignoreColumns)

		wideFormHeadersString=''
		#for value,item in wideFormHeaders:
		for key,value in enumerate(wideFormHeaders):
			if self.verbose: print("key="+str(key))			
			if self.verbose: print("value="+value)
			if self.verbose: print("len(wideFormHeaders)="+str(len(wideFormHeaders)))
			if key < (len(wideFormHeaders)-1):				
				wideFormHeadersString = wideFormHeadersString + value + ','
			else:
				wideFormHeadersString = wideFormHeadersString + value + '\n'



		# add headers to top of file
		self.insertLineAtBeginingOfFile(wideFormFileName,wideFormHeadersString)

	#/transformLongToWideForm()


	def insertLineAtBeginingOfFile(self,originalfile,string):
		TMP_FILE_NAME = 'tmp.csv'
    		with open(originalfile,'r') as f:
        		with open(TMP_FILE_NAME,'w') as f2: 
				f2.write(string)
				#f2.writerow(string)
				f2.write(f.read())
		os.rename(TMP_FILE_NAME,originalfile)


	"""
	" createHeaders
	"""
	def createHeaders(self, fileHeaders,maxIteration,idColumn,staticColumns,ignoreColumns):
		""" createHeaders()"""

		if self.verbose: print("createHeaders()")
		if self.verbose: print(fileHeaders)
		
		

		rowData=[]

		rowData.append(fileHeaders[idColumn])

		for staticItem in staticColumns:			
			rowData.append(fileHeaders[staticItem])
			
		

		# generate items to remove
		itemsToRemove=[]
		 
		itemsToRemove.append(idColumn)
		
		for i in staticColumns:
			itemsToRemove.append(i)

		for j in ignoreColumns:
			itemsToRemove.append(j)


		if self.verbose: print(itemsToRemove)
		itemsToRemove.sort(reverse=True)
		if self.verbose: print(itemsToRemove)

		# Get remaining elements
		elements = range(0,len(fileHeaders))
		if self.verbose: print(elements)


		#remove 
		for k in itemsToRemove:
			elements.remove(k)
		if self.verbose: print(elements)


		if self.verbose: print("maxIteration= "+str(maxIteration))
		for x in range(1,maxIteration+1):
						
			for y in elements:
				hValue = ''+fileHeaders[y]+'_'+str(x)+''
				rowData.append(hValue)
			
		# final row headers
		if self.verbose: print(rowData)

		return rowData

	#/createHeaders()





"""
" Runs this class
"
"""
if __name__ == '__main__':
		
	# Command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--longFormFileName", help="Name of the long form data input file", required=True)
	parser.add_argument("-w", "--wideFormFileName", help="Name of the wide form data output file", required=True)
	parser.add_argument("-u", "--uniqueIdColumn", help="Column number that contains the unique id to identify rows", type=int, required=True)

	parser.add_argument('-s','--staticColumns', nargs='+', help='List of static columns. ie 2 4 5 6', type=int, default=[])
	parser.add_argument('-i','--ignoreColumns', nargs='+', help='List of columns to ignore. ie 2 4 5 6', type=int, default=[])

	parser.add_argument("-v", "--verbose", help="Set output verbosity to true", action="store_true")
	args = parser.parse_args()

	verbose=False
	if args.verbose: verbose=True
	    
	#filename
	longFormFileName = args.longFormFileName
	wideFormFileName = args.wideFormFileName	

	# id column
	idColumn = args.uniqueIdColumn

	# staticColumns
	staticColumns = args.staticColumns

	# ignoreColumns
	ignoreColumns = args.ignoreColumns

	#print(args.staticColumns)
	

	
	if verbose:
		print("Verbosity turned on")
		print(" # filename")
		print("  longFormFileName = "+ longFormFileName)
		print("  wideFormFileName = "+ wideFormFileName)
		print(" # id column")
		print("  idColumn = "+ str(idColumn))
		print(" # staticColumns")
		print(staticColumns)
		print(" # ignoreColumns")
		print(ignoreColumns)
		print("")
		print("")

	dt = DataTransform(verbose)
	dt.transformLongToWideForm(longFormFileName,wideFormFileName,idColumn,staticColumns,ignoreColumns)


