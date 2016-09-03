import argparse
import loader_util
import esdclasses


parser = argparse.ArgumentParser(description='Utility to generate model and product slot lists')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--model', action='store_true',
		   help='print list of all unique models, one per line')
group.add_argument('--product', action='store_true',
		   help='print list of all unique products, one per line')
parser.add_argument('--from_local_directory', action='store_true',
		   help='use a EOSL-HW-docu47424.csv file in the current directory instead of pulling from S3')
parser.add_argument('--count', action='store_true',
		   help='count the number of objects rather than print them')

args = parser.parse_args()

if args.from_local_directory == False:
    alldata = loader_util.load_data_from_s3()
else:
    alldata = loader_util.load_data()


def get_models():
        modelstring = ""
        i = 0
	for m in alldata.getmodelslist():
                if m.strip() == "":
                        m = "(blank)"
                        
                if i == 0:
                        modelstring = modelstring + m
                else:
                        modelstring = modelstring + "\n" + m
                i += 1
        if args.count == False:
                print modelstring
        else:
                print ("There are {:d} unique models".format(i))

def get_products():
        productstring = ""
        i = 0
	for p in alldata.getproductslist():
                if p.strip() == "":
                        p = "(blank)"
                        
                if i == 0:
                        productstring = productstring + p
                else:
                        productstring = productstring + "\n" + p
                i += 1
        if args.count == False:
                print productstring
        else:
                print ("There are {:d} unique products".format(i))



if args.model == True:
        get_models()
elif args.product == True:
        get_products()

