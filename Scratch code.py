#import io
#import os
import esdclasses
import csv

"""
# Loop through the data read from csv and dump the first bit of it to screen
with open('EOSL.csv', mode='r', newline=None) as csvfile:
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
"""	

"""
Read data from CSV file into dictionary objects

Initilize utility data structures from the dictionary objects

Loop through the data read from csv and write it as JSON to file & screen	
"""
with open ('EOSL.csv', mode='r', newline=None) as csvfile:
	field_names = esdclasses.DataPoint.getfieldnames()
	reader = csv.DictReader(csvfile, dialect='excel', fieldnames=field_names)
	writer = csv.DictWriter(csvfile, fieldnames=field_names)
	
	alldata = esdclasses.EMCSupportDates()
	alldata.setlastupdatetonow()
	
	with open ('emcsupportdata.json', mode='w') as jsonfile:
		i=0
		
		#begin supportdates
		for row in reader:
			i += 1
			
			# skip the first one because it will be the header row
			if i > 1:
				#begin datapoint
				thisone = esdclasses.DataPoint(row)
				alldata.push(thisone)
				"""
				#experimental JSON library code -- never worked
				#json.dump('"datapoint": ', jsonfile, indent="\t\t")
				#json.dump(row, jsonfile, indent="\t\t\t")
				#json.dump('"product":' row['Product'], jsonfile, indent="\t\t\t")		
				#json.dump('\n', jsonfile)
				"""
				#end datapoint
		#end supportdates

		#io.TextIOWrapper(jsonfile).write(alldata.toJSON(0))
		jsonfile.write(alldata.toJSON(0))
		print(alldata.toJSON(0))
		
		jsonfile.close()
	
	csvfile.close()