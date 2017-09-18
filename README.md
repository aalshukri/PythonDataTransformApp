# PythonDataTransformApp


This application can be used to transform long-form files into wide-form.

The basic functionality behind the transformation process
is to take all entries for a patient in long format, which are expressed
as multiple rows, and produce a single row for a patient. 
Each of the values which are in rows in long form, 
will now be expressed as columns in wide format.

Functionality to transform to different forms might be added during the development of the application.

## Running Instructions

Example

> python DataTransform.py -l testdata/testdata1.csv -w testdata/testdata1_wide.csv -u 0 -s 2 3 4 -i 1

The command above translates to:

	# filename
	longFormFileName = 'testdata/testdata1.csv'
	wideFormFileName = 'testdata/testdata1_wide.csv'	

	# id column
	idColumn=0

	# staticColumns
	staticColumns=[2,3,4]

	# ignoreColumns
	ignoreColumns=[1]


## Todo

* Make verbose output more user friendly
* Add a number range function for entry of large column ranges for static and ignore



