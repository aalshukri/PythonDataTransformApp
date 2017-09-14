#
# DataTransform
#
# @created 2017-05-10 11:56:12 
# @version 0.01 (beta)
# @author 
# @email 
#
# PythonDataTransformApp
#	Converts long-form data to wide-form data
#
# 	Assumes that input is sorted by idColumn.
#		This assumption allows for large data sets to be processed
#		without loading entire file into memory for sorting.
#		[Could use indexing as pre-processing step]
#
# How does this application work?
"""

"""
#
# How to run:
# > python DataTransform.py
#

import csv
import os

class DataTransform(object):	
	'Data Transform App'
	pass


	"""
	" Constructor
	"""
	#def __init__(self):
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
			* longFormFileName - the csv filename of the long form data file
			* 

		     How this function works?
			
			The algorithm transformaiton algorithm has two important elements in the main loop.


			
		"""

		print("transformLongToWideForm("+longFormFileName+")")


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
		print("maxColumnLength="+str(maxColumnLength))


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
			print("idvalue="+idValue)
			

			if idValue != currentId:
				print(" new person")

				# write current row data (if not empty)
				if rowData != []:
					print(" Write previous persons data "+str(currentIteration))
					print(rowData)
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
				print(" not new person")
				currentIteration=currentIteration+1

			# Part 2 
			# Checking for ignore or static columns to exclude.
			# if not, then append to the current row data.
			#
			for i in range(0,len(row)):

				# check if we should ignore this row
				#
				if i == idColumn:
					print("  dont output "+str(i))
				elif i in staticColumns:
					print("  dont output "+str(i))
				elif i in ignoreColumns:
					print("  dont output "+str(i))	
				else:					
					# append item to current row
					print("  printing "+str(i))				
					rowData.append(row[i])



		# write last persons row data (if not empty)
		if rowData != []:
			print(" Write LAST persons data "+str(currentIteration))
			print(rowData)
			write.writerow(rowData)
		
		infile.close()		
		outfile.close()

	
		# create headers
		wideFormHeaders = self.createHeaders(fileHeaders,maxIteration,idColumn,staticColumns,ignoreColumns)

		wideFormHeadersString=''
		#for value,item in wideFormHeaders:
		for key,value in enumerate(wideFormHeaders):
			print("key="+str(key))			
			print("value="+value)
			print("len(wideFormHeaders)="+str(len(wideFormHeaders)))
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

		print("createHeaders()")
		print(fileHeaders)
		
		

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


		print(itemsToRemove)
		itemsToRemove.sort(reverse=True)
		print(itemsToRemove)


		# Get remaining elements
		elements = range(0,len(fileHeaders))
		print(elements)

		#remove 
		for k in itemsToRemove:
			elements.remove(k)
		print(elements)

		print("maxIteration= "+str(maxIteration))
		for x in range(1,maxIteration+1):
			print(x)
			
			for y in elements:
				hValue = ''+fileHeaders[y]+'_'+str(x)+''
				rowData.append(hValue)
			
		# final row headers
		print(rowData)

		return rowData

	#/createHeaders()





"""
" Runs this class
"
"""
if __name__ == '__main__':
	dt = DataTransform()

	#filename
#	longFormFileName = 'testdata/testdata1.csv'
#	wideFormFileName = 'testdata/testdata1_wide.csv'	

	# id column
#	idColumn=0

	# staticColumns
#	staticColumns=[2,3,4]

	# ignoreColumns
#	ignoreColumns=[1]



	#filename
	longFormFileName = 'data/Cohort_Emis-Opt_v2_2016-08-26.csv'
	wideFormFileName = 'data/Cohort_Emis-Opt_v2_2016-08-26_wide.csv'	

	# id column
	idColumn=0

	# staticColumns
	staticColumns=[1,2,3,4,5,6]

	# ignoreColumns
	ignoreColumns=[]

	dt.transformLongToWideForm(longFormFileName,wideFormFileName,idColumn,staticColumns,ignoreColumns)


