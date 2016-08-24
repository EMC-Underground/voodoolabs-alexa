#import io
#import os
import esdclasses
import csv
import UserDict

with open('EOSL.csv', mode='rU') as csvfile:  #mode U is deprecated in Python 3.6
	reader = csv.DictReader(csvfile, dialect='excel')
	i=0
	#begin supportdates
	print('[')
	print("\t\"emcsupportdates\": {")
	for row in reader:
		i += 1
		if i <= 4:
		#begin datapoint
			print("\t\t\"datapoint\": {")
			print("\t\t\t\"product\": \"", row['Product'], "\",")
			print("\t\t\t\"model\": \"", row['Model'], "\",")
			print("\t\t\t\"ga_date\": \"", row['GA Date'], "\",")
			print("\t\t\t\"eol_date\": \"", row['EOL Date'], "\",")
			print("\t\t\t\"eops_date\": \"", row['EOPS Date'], "\",")
			print("\t\t\t\"eosl_date\": \"", row['EOSL Date'], "\",")
			print("\t\t\t\"ga_updated\": \"", row['GA Updated?'], "\",")
			print("\t\t\t\"eol_updated\": \"", row['EOL Updated?'], "\",")
			print("\t\t\t\"eops_updated\": \"", row['EOPS Updated?'], "\",")
			print("\t\t\t\"eosl_updated\": \"", row['EOSL Updated?'], "\",")
			print("\t\t},")
		#end datapoint
	print(']')
	#end supportdates
	csvfile.close()
	
	
with open ('EOSL.csv', mode='rU') as csvfile:  #mode U is deprecated in Python 3.6
        dictobj = UserDict.IterableUserDict( {'Product' : ' ', 'Model' : ' ',
                        'GA Date' : ' ', 'EOL Date' : ' ', 'EOPS Date' : ' ',
                        'EOSL Date' : ' ',
                        'GA Updated?' : ' ', 'EOL Updated?' : ' ',
                        'EOPS Updated?' : ' ', 'EOSL Updated?' : ' '} )
        dpo = esdclasses.DataPoint(dictobj)
	field_names = dpo.getfieldnames
	reader = csv.DictReader(csvfile, dialect='excel')
	
	alldata = esdclasses.EMCSupportDates()
	alldata.setlastupdatetonow()
	
	with open ('emcsupportdata.json', mode='w') as jsonfile: #mode U is deprecated in Python 3.6
		i=0
		
		#begin supportdates
		for row in reader:
			i += 1
			
			# skip the first one because it will be the header row
			if i > 1:
				thisone = esdclasses.DataPoint(row)
				alldata.push(thisone)
		

		#end supportdates

		jsonfile.write(alldata.toJSON(0))
		print(alldata.toJSON(0))
		
		jsonfile.close()
	
	csvfile.close()
