#import io
#import os
import esdclasses
import csv
import UserDict
import query_util
import os

with open('EOSL-HW-docu47424.csv', mode='rU') as csvfile:  #mode U is deprecated in Python 3.6
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
	
	
with open ('EOSL-HW-docu47424.csv', mode='rU') as csvfile:  #mode U is deprecated in Python 3.6
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
	alldata.rebuildproductslist() #only to test the code path (not needed)
	alldata.rebuildmodelslist() #only to test the code path (not needed)
	
	
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

 	productsstring = 'Products: \n'
 	pi = 0
        for p in alldata.getproductslist():
                if pi == 0:
                        productsstring = productsstring + p
                else:
                        productsstring = productsstring + "\n" + p
                pi += 1
                
        print(productsstring + "\n\n")

        modelsstring = "Models: "
        pm = 0
	for m in alldata.getmodelslist():
                if pm == 0:
                        modelsstring = modelsstring + m
                else:
                        modelsstring = modelsstring + ", " + m
                pm += 1
        print(modelsstring + "\n")


        #test the get by product_model pathway
        print("\n\n -----get-by-product-model-----\n\n")
        prod_mod_result = query_util.find_matches_by_product_model(alldata, "Symmetrix", "VMAXe")
        print(prod_mod_result.toSimpleString() + "\n\n")
                
        #test the get by product pathway
        print("\n\n -----get-by-product-----\n\n")
        prod_result = query_util.find_matches_by_product(alldata, "Clariion CX")
        print(prod_result.toSimpleString() + "\n\n")
                
        #test the get by model pathway
        print("\n\n -----get-by-model-----\n\n")
        mod_result = query_util.find_matches_by_model(alldata, "Gen1")
        print(mod_result.toSimpleString() + "\n\n")


# test reading environment variables from local file in directory
# and setting variables from within python. To test you must have
# a file containing the variable values other than header row.
#
# the primary use of this file is to supply credentials for AWS.
#
# this local file may be empty in command line instances where AWS
# credentials will come from profile in ~/.aws/credentials.
with open('EnvironmentVariables.csv', mode='rU') as csvfile:  #mode U is deprecated in Python 3.6
        reader = csv.DictReader(csvfile, dialect='excel')
        i=0
        for row in reader:
                i+=1
                try:
                    print("Setting env variable " + row['VariableName'] + "="
                          + row['VariableValue'])
                    os.environ[row['VariableName']] = row['VariableValue']
                    print("Set env variable " + row['VariableName'] + "="
                          + os.environ[row['VariableName']])
                except KeyError:
                    print("Unable to lookup value " + "{:d}".format(i) +
                          " in row of dict. Failed to set environment variable.")
        csvfile.close()

