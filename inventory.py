import sys
import argparse
import collections
from operator import itemgetter
from sys import stdin,stderr,exit
import fileinput
from itertools import imap

parser = argparse.ArgumentParser(description='Inventory Management')
parser.add_argument('-f', metavar="File", type=str)
parser.add_argument("actionFile", metavar='FILE', nargs="*", help="File name to read action from")
args = parser.parse_args()

arr=[]
i = 0

def try_int(val):
	try:
		return int(val)
	except ValueError:
		return val

def write_funct(arr):
    myfile = open(args.f,'w')
    myfile.write('PartID         Description      Footprint        Quantity         \n')
    
    for x in arr:
            part = str(x['PartID'])
	    description = str(x['Description'])
	    footprint =  str(x['Footprint'])
	    Quantity = str(x['Quantity'])
	    tab = '\t\t'
	    value = part + tab + description + tab + footprint + tab + Quantity +'\n'
	    
	    myfile.write(value)

	    


with open(args.f,'r+') as f:
	for line in f:
	   
	 	if i>0:
	 		d = collections.OrderedDict()
			value = line.split()
		
			d['PartID'] = value[0]
			d['Description'] = value[1]
			d['Footprint'] = int(value[2])
			d['Quantity'] = int(value[3])
			
			arr.append(d)
			
		i=i+1

for line in imap(str.strip, fileinput.input(args.actionFile)):
        wrds = line.split()
    
#Check if remove
# format remove Quantity 5
	if wrds[0]=='remove':
		try:
			newA = []
			i=0
		 	for x in arr:
		 		if x[wrds[1]] != wrds[2]:
					newA.insert(i,x)
		 			
				i=i+1
			print "<Item sucessfully removed>"
			write_funct(newA)
			
					 	 	
		except KeyError:
		 	print "That field does not exist!"
		 	#continue
		 	
#i=0
#		 	for i in xrange(len(arr)):
#		 		if arr[i][str(wrds[1])] == str(wrds[2]):
#		 			print "\n <Item removed from database>"
#		 			arr.pop(i)
		 			#continue
#code can be implementer here to throw an error if value does not exist DB		 			
		 	        #i=i+1
                        write_funct(arr)        
#Check if set
# set Quantity 5 for PartID R67817
	elif wrds[0]=='set':
		try:
		 	for x in arr:
		 		if x[wrds[4]] == wrds[5]:
		 			x[wrds[1]] = wrds[2]
		 			print "Database updated!"
		 			#continue
		 	write_funct(arr)		 			
		except KeyError:
		 	print "Not a valid field name!"
		 	#continue	
		
#This will be executed if the command is list
# list all with Quantity 10 
# list all sort by Quantity
	elif wrds[0]=='list':
	
		try:
			if wrds[2]=='with':
				for x in arr:
					sortBy = str(wrds[4])
					if wrds[3] == 'Quantity' or wrds[3] == 'Footprint':
						sortBy = int(wrds[4])
				
		 			if x[wrds[3]] == sortBy:
		 				print '\nPartID \t \t','Description\t \t   ','Footprint\t \t','Quantity\t \t'
		 				print x['PartID'],'\t \t', x['Description'],'\t', x['Footprint'],'\t \t', x['Quantity']
		 				
		 	elif wrds[2]=='sort':
				newlist = arr
				print '\n'
				newlist = sorted(arr, key=lambda k: k[wrds[4]])
			
				for x in newlist:
					print '\nPartID \t \t','Description\t \t   ','Footprint\t \t','Quantity\t \t'
		 			print x['PartID'],'\t \t', x['Description'],'\t', x['Footprint'],'\t \t', x['Quantity']
		 	
		except KeyError:
		 	print "Not a valid field name!"
		 	#continue
# list all goes here		
		except IndexError:
			for x in arr:
				print '\nPartID \t \t','Description\t \t   ','Footprint\t \t','Quantity\t \t'
		 		print x['PartID'],'\t \t', x['Description'],'\t', x['Footprint'],'\t \t', x['Quantity']
		 		print '\n'
		 		#continue
		 	
		 	
#Check if sort
#sort by Quantity
	elif wrds[0]=='sort':
			newlist = arr
			newlist = sorted(arr, key=lambda k: k[wrds[2]])
			arr=newlist
			write_funct(arr)
			
			print newlist
			
# add PartID R4700 Description RES,50OHM,1/4W,1%,SMD Footprint 1206 Quantity 5
	elif wrds[0]=='add':
		    d = collections.OrderedDict()		
		    d['PartID'] = wrds[2]
		    d['Description'] = wrds[4]
		    d['Footprint'] = int(wrds[6])
		    d['Quantity'] = int(wrds[8])			
		    arr.append(d)
		    write_funct(arr)
		    print "\n <The item has been succesfully added to the database>"

